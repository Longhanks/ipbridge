# -*- coding: utf-8 -*-
# system imports.
import datetime
import plistlib
from pathlib import Path
import subprocess
import threading
from dateutil import tz

from flask import current_app
from flask.helpers import get_debug_flag

from asabridge.extensions import cache

UNSAVED_KEY = 'readinglist:unsaved'
DELETED_KEY = 'readinglist:deleted'


def get_readinglist():
    if get_debug_flag():
        return cache.get('DEBUGDATA') or []

    plist = Path.home() / 'Library' / 'Safari' / 'Bookmarks.plist'
    with open(plist, 'rb') as plist_f:
        data = plistlib.load(plist_f)['Children']

    readinglist = [e for e in data if e.get('Title') == 'com.apple.ReadingList'][0]
    readinglist_elements = readinglist.get('Children') or []
    pythonic_readinglist = []
    for item in readinglist_elements:
        pythonic_readinglist_item = {'title': item['URIDictionary']['title'],
                                     'URLString': item['URLString'],
                                     'imageURL': item.get('imageURL'),
                                     'DateAdded': item['ReadingList']['DateAdded'].replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
                                     }
        pythonic_readinglist_item['PreviewText'] = item['ReadingList'].get('PreviewText') or pythonic_readinglist_item['title']
        pythonic_readinglist.append(pythonic_readinglist_item)

    # The cache of unsaved readinglist items.
    unsaved = cache.get(UNSAVED_KEY) or []

    # First, check if unsaved items are now part of the readinglist and remove them from the unsaved list, if so.
    for rl_item in pythonic_readinglist:
        unsaved_index = None
        for index, item in enumerate(unsaved):
            delta = abs((rl_item['DateAdded'] - item['DateAdded']).total_seconds())
            rl_url = rl_item['URLString']
            my_url = item['URLString']
            if rl_url in (my_url, my_url + '/') and delta <= 1.5:
                unsaved_index = index
                break
        if unsaved_index is not None:
            unsaved.pop(unsaved_index)

    # Save cache updates.
    cache.set(key=UNSAVED_KEY, value=unsaved, timeout=120)

    # Now add the remaining items from the unsaved list to the readinglist.
    for item in unsaved:
        item_dict = {
            'title': item['URLString'],
            'URLString': item['URLString'],
            'imageURL': None,
            'DateAdded': item['DateAdded'],
            'PreviewText': item['URLString']
            }
        pythonic_readinglist.append(item_dict)

    pythonic_readinglist.sort(key=lambda rl_item: rl_item['DateAdded'], reverse=True)

    # Now remove the items that are marked as deleted.
    deleted = cache.get(DELETED_KEY) or []
    deletion_finished_indices = []
    for deleted_item_index, deleted_item in enumerate(deleted):
        rl_index = None
        for index, rl_item in enumerate(pythonic_readinglist):
            delta = abs((rl_item['DateAdded'] - deleted_item['DateAdded']).total_seconds())
            rl_url = rl_item['URLString']
            my_url = deleted_item['URLString']
            if rl_url in (my_url, my_url + '/') and delta <= 1.5:
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
    cache.set(key=DELETED_KEY, value=deleted, timeout=120)

    return pythonic_readinglist


def add_readinglist_item(url):
    date_added = datetime.datetime.now().replace(tzinfo=tz.tzlocal())
    rl_item = {
        'title': url,
        'URLString': url,
        'imageURL': None,
        'DateAdded': date_added,
        'PreviewText': url
    }
    current_app.logger.debug('New readinglist item: { \"URLString\": \"' + url + '\", \"DateAdded\": \"' + date_added.isoformat() + '\" }')

    if get_debug_flag():
        data = cache.get('DEBUGDATA') or []
        data.append(rl_item)
        data.sort(key=lambda rl_item: rl_item['DateAdded'], reverse=True)
        cache.set(key='DEBUGDATA', value=data, timeout=-1)
        return

    js_call = 'Application("Safari").addReadingListItem("' + url + '")'
    osascript_call = ['osascript', '-l', 'JavaScript', '-e', js_call]
    subprocess.check_call(osascript_call)
    unsaved = cache.get(key=UNSAVED_KEY) or []
    unsaved.append(rl_item)
    cache.set(key=UNSAVED_KEY, value=unsaved, timeout=120)


def delete_readinglist_item(index):
    if get_debug_flag():
        data = cache.get('DEBUGDATA') or []
        data.pop(int(index))
        cache.set(key='DEBUGDATA', value=data, timeout=-1)
        return

    item = get_readinglist()[int(index)]
    osascript_call = ['osascript', '-l', 'JavaScript', current_app.root_path + '/static/remove_readinglist.js', str(index)]
    thread = threading.Thread(target=subprocess.check_call, args=(osascript_call,))
    thread.start()
    deleted = cache.get(key=UNSAVED_KEY) or []
    deleted.append(item)
    cache.set(key=DELETED_KEY, value=deleted, timeout=120)
