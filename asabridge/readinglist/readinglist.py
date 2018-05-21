# -*- coding: utf-8 -*-
# system imports.
import datetime
import plistlib
from pathlib import Path
import subprocess
import time
from dateutil import tz

from flask import current_app
from flask.helpers import get_debug_flag

from asabridge.extensions import cache

UNSAVED_KEY = 'readinglist:unsaved'
DELETED_KEY = 'readinglist:deleted'


def get_readinglist():
    if get_debug_flag():
        sample_data = [{
            'title': 'Google',
            'URLString': 'https://www.google.com/',
            'imageURL': None,
            'DateAdded': datetime.datetime(2018, 4, 29, 0, 46, 15, 247691, tzinfo=tz.tzlocal()),
            'PreviewText': 'Google+ Suche Bilder Maps Play YouTube News Gmail Mehr Andreas Schulz Erweiterte Suche Sprachoptionen Google angeboten in: English Werben mit GoogleUnternehmensangebote+GoogleÜber GoogleGoogle.de © 2018 - Daten'
            }, {
            'title': 'reddit: the front page of the internet',
            'URLString': 'https://www.reddit.com/r/cpp/comments/8drshx/c_templates_revised_nicolai_josuttis_accu_2018/',
            'imageURL': 'https://i.ytimg.com/vi/9PFMllbyaLM/hqdefault.jpg',
            'DateAdded': datetime.datetime(2018, 4, 21, 12, 44, 33, 650619, tzinfo=tz.tzlocal()),
            'PreviewText': 'Cookies help us deliver our Services. By using our Services, you agree to our use of cookies.Learn More r/cppyoutube C++ Templates Revised - Nicolai Josuttis [ACCU 2018] u/vormestrand 4 Comments14 Top Write a comment Ob'
            }]
        return sample_data
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

    return pythonic_readinglist


def add_readinglist_item(url):
    if get_debug_flag():
        return
    js_call = 'Application("Safari").addReadingListItem("' + url + '")'
    osascript_call = ['osascript', '-l', 'JavaScript', '-e', js_call]
    subprocess.check_call(osascript_call)
    date_added = datetime.datetime.now().replace(tzinfo=tz.tzlocal())
    current_app.logger.debug('New readinglist item: { \"URLString\": \"' + url + '\", \"DateAdded\": \"' + date_added.isoformat() + '\" }')
    rl_item = {
        'URLString': url,
        'DateAdded': date_added
    }
    unsaved = cache.get(key=UNSAVED_KEY) or []
    unsaved.append(rl_item)
    cache.set(key=UNSAVED_KEY, value=unsaved, timeout=120)


def delete_readinglist_item(index):
    if get_debug_flag():
        return
    osascript_call = ['osascript', '-l', 'JavaScript', current_app.root_path + '/static/remove_readinglist.js', str(index)]
    subprocess.check_call(osascript_call)
    time.sleep(3)
