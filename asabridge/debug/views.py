# -*- coding: utf-8 -*-
import datetime
from dateutil import tz
from flask import Blueprint
from flask_login import login_required
from typing import List

from asabridge.extensions import cache
from asabridge.readinglist.readinglist_item import ReadinglistItem

blueprint = Blueprint('debug', __name__)


@blueprint.route('/api/resetDebugData', methods=['GET'])
@login_required
def index():
    sample_data: List[ReadinglistItem] = []

    item_1 = ReadinglistItem(title='Google', url='https://www.google.com/', image_url=None,
                             date=datetime.datetime(2018, 4, 29, 0, 46, 15, 247691, tzinfo=tz.tzlocal()),
                             preview='Google+ Suche Bilder Maps Play YouTube News Gmail Mehr Andreas Schulz Erweiterte Suche Sprachoptionen Google angeboten in: English Werben mit GoogleUnternehmensangebote+GoogleÜber GoogleGoogle.de © 2018 - Daten')
    item_2 = ReadinglistItem(title='reddit: the front page of the internet',
                             url='https://www.reddit.com/r/cpp/comments/8drshx/c_templates_revised_nicolai_josuttis_accu_2018/',
                             image_url='https://i.ytimg.com/vi/9PFMllbyaLM/hqdefault.jpg',
                             date=datetime.datetime(2018, 4, 21, 12, 44, 33, 650619, tzinfo=tz.tzlocal()),
                             preview='Cookies help us deliver our Services. By using our Services, you agree to our use of cookies.Learn More r/cppyoutube C++ Templates Revised - Nicolai Josuttis [ACCU 2018] u/vormestrand 4 Comments14 Top Write a comment Ob')
    sample_data.append(item_1)
    sample_data.append(item_2)
    cache.set(key='DEBUGDATA', value=sample_data, timeout=-1)
    return '', 204
