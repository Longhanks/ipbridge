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
        pythonic_readinglist_item = {}
        pythonic_readinglist_item['title'] = item['URIDictionary']['title']
        pythonic_readinglist_item['URLString'] = item['URLString']
        pythonic_readinglist_item['imageURL'] = item.get('imageURL')
        pythonic_readinglist_item['DateAdded'] = item['ReadingList']['DateAdded'].replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
        pythonic_readinglist_item['PreviewText'] = item['ReadingList'].get('PreviewText') or pythonic_readinglist_item['title']
        pythonic_readinglist.append(pythonic_readinglist_item)
    return pythonic_readinglist


def add_readinglist_item(url):
    if get_debug_flag():
        return
    js_call = 'Application("Safari").addReadingListItem("' + url + '")'
    osascript_call = ['osascript', '-l', 'JavaScript', '-e', js_call]
    subprocess.check_call(osascript_call)
    time.sleep(3)


def delete_readinglist_item(index):
    if get_debug_flag():
        return
    osascript_call = ['osascript', '-l', 'JavaScript', current_app.root_path + '/static/remove_readinglist.js', str(index)]
    subprocess.check_call(osascript_call)
    time.sleep(3)
