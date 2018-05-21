# -*- coding: utf-8 -*-
import datetime
from dateutil import tz
from flask import Blueprint, redirect, url_for
from flask_login import login_required

from asabridge.extensions import cache

blueprint = Blueprint('debug', __name__, static_folder='../static')


@blueprint.route('/resetDebugData', methods=['GET'])
@login_required
def index():
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
    cache.set(key='DEBUGDATA', value=sample_data, timeout=-1)
    return redirect(url_for('index.index'))
