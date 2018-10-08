# -*- coding: utf-8 -*-
import datetime
import hashlib
import plistlib
from pathlib import Path
import subprocess
import threading
from dateutil import tz
from typing import Optional, List

from flask import current_app
from flask.helpers import get_debug_flag

from ipbridge.extensions import cache
from .readinglist_item import ReadinglistItem


def get_cached_image(image_url: Optional[str]) -> Optional[str]:
    if image_url is None:
        return None
    file_name = hashlib.sha512(image_url.encode()).hexdigest()
    image_cache_path = Path(current_app.config['IMAGE_CACHE_PATH'])
    if not image_cache_path.exists():
        image_cache_path.mkdir(parents=True)
    abs_path = image_cache_path / file_name
    if not abs_path.exists():
        current_app.logger.info(f'No cached image found for {image_url}.')
        current_app.logger.info(f'Downloading {image_url} to serve it cached.')
        try:
            subprocess.check_call(['/usr/bin/curl', '-L', image_url, '-o', abs_path])
        except subprocess.CalledProcessError as e:
            current_app.logger.info(f'Downloading {image_url} failed! Error: {e}')
            return None
    abs_url = '/imagecache/' + file_name
    current_app.logger.info(f'Serving from cache: {image_url}')
    return abs_url


def get_readinglist() -> List[ReadinglistItem]:
    if get_debug_flag():
        return cache.get('DEBUGDATA') or []

    plist = Path.home() / 'Library' / 'Safari' / 'Bookmarks.plist'
    with open(plist, 'rb') as plist_f:
        data = plistlib.load(plist_f)['Children']

    readinglist = [e for e in data if e.get('Title') == 'com.apple.ReadingList'][0]
    readinglist_elements = readinglist.get('Children') or []
    pythonic_readinglist: List[ReadinglistItem] = []
    for item in readinglist_elements:
        title = item['URIDictionary']['title']
        url = item['URLString']
        image_url = get_cached_image(item.get('imageURL'))
        date: datetime = item['ReadingList']['DateAdded'].replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
        preview = item['ReadingList'].get('PreviewText')
        rl_item = ReadinglistItem(title=title, url=url, image_url=image_url, date=date, preview=preview)
        pythonic_readinglist.append(rl_item)

    # The cache of unsaved readinglist items.
    unsaved: List[ReadinglistItem] = cache.get(current_app.config['READING_LIST_UNSAVED_KEY']) or []

    # First, check if unsaved items are now part of the readinglist and remove them from the unsaved list, if so.
    for rl_item in pythonic_readinglist:
        unsaved_index = None
        for index, item in enumerate(unsaved):
            delta = abs((rl_item.date - item.date).total_seconds())
            if rl_item.url in (item.url, item.url + '/') and delta <= 1.5:
                unsaved_index = index
                break
        if unsaved_index is not None:
            unsaved.pop(unsaved_index)

    # Save cache updates.
    cache.set(key=current_app.config['READING_LIST_UNSAVED_KEY'], value=unsaved, timeout=120)

    # Now add the remaining items from the unsaved list to the readinglist.
    pythonic_readinglist += unsaved
    pythonic_readinglist.sort(key=lambda rl_item: rl_item.date, reverse=True)

    # Now remove the items that are marked as deleted.
    deleted: List[ReadinglistItem] = cache.get(current_app.config['READING_LIST_DELETED_KEY']) or []
    deletion_finished_indices = []
    for deleted_item_index, deleted_item in enumerate(deleted):
        rl_index = None
        for index, rl_item in enumerate(pythonic_readinglist):
            delta = abs((rl_item.date - deleted_item.date).total_seconds())
            if rl_item.url in (deleted_item.url, deleted_item.url + '/') and delta <= 1.5:
                rl_index = index
                break
        if rl_index is not None:
            pythonic_readinglist.pop(rl_index)
        else:
            deletion_finished_indices.append(deleted_item_index)

    # Remove the deleted items form the list that the readinglist finished deleting.
    for index in deletion_finished_indices:
        deleted.pop(index)

    # Save cache updates.
    cache.set(key=current_app.config['READING_LIST_DELETED_KEY'], value=deleted, timeout=120)

    return pythonic_readinglist


def add_readinglist_item(url: str):
    date_added = datetime.datetime.now().replace(tzinfo=tz.tzlocal())
    rl_item = ReadinglistItem(title=url, url=url, image_url=None, date=date_added, preview=url)
    current_app.logger.info(
        f'New readinglist item: {{ "URLString ": "{url}", "DateAdded": "{date_added.isoformat()}" }}')

    if get_debug_flag():
        data: List[ReadinglistItem] = cache.get('DEBUGDATA') or []
        data.append(rl_item)
        data.sort(key=lambda rl_item: rl_item.date, reverse=True)
        cache.set(key='DEBUGDATA', value=data, timeout=-1)
        return

    js_call = 'Application("Safari").addReadingListItem("' + url + '")'
    osascript_call = ['osascript', '-l', 'JavaScript', '-e', js_call]
    subprocess.check_call(osascript_call)
    unsaved: List[ReadinglistItem] = cache.get(key=current_app.config['READING_LIST_UNSAVED_KEY']) or []
    unsaved.append(rl_item)
    cache.set(key=current_app.config['READING_LIST_UNSAVED_KEY'], value=unsaved, timeout=120)


def delete_readinglist_item(index: int):
    current_app.logger.info(f'Attempting to delete item at index {index}')
    if get_debug_flag():
        data: List[ReadinglistItem] = cache.get('DEBUGDATA') or []
        data.pop(index)
        cache.set(key='DEBUGDATA', value=data, timeout=-1)
        return

    item: ReadinglistItem = get_readinglist()[index]
    js_src_path = current_app.root_path + '/readinglist/remove_item.js'
    osascript_call = ['osascript', '-l', 'JavaScript', js_src_path, str(index)]
    thread = threading.Thread(target=subprocess.check_call, args=(osascript_call,))
    thread.start()
    deleted: List[ReadinglistItem] = cache.get(key=current_app.config['READING_LIST_UNSAVED_KEY']) or []
    deleted.append(item)
    cache.set(key=current_app.config['READING_LIST_DELETED_KEY'], value=deleted, timeout=120)
