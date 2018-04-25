# system imports.
import datetime
import plistlib
from pathlib import Path
import subprocess
import time
from dateutil import tz

from asabridge.app import app


def get_readinglist():
    if app.debug:
        sample_data = [{
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
        pythonic_readinglist_item['PreviewText'] = item['ReadingList'].get('PreviewText')
        pythonic_readinglist.append(pythonic_readinglist_item)
    return pythonic_readinglist


def add_readinglist_item(url):
    if app.debug:
        return
    js_call = 'Application("Safari").addReadingListItem("' + url + '")'
    osascript_call = ['osascript', '-l', 'JavaScript', '-e', js_call]
    subprocess.check_call(osascript_call)
    time.sleep(3)
