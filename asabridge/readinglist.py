import plistlib
from pathlib import Path
import subprocess
from dateutil import tz
import time


def get_readinglist():
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
    js_call = 'Application("Safari").addReadingListItem("' + url + '")'
    osascript_call = ['osascript', '-l', 'JavaScript', '-e', js_call]
    subprocess.check_call(osascript_call)
    time.sleep(3)

