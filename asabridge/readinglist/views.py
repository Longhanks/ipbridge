# -*- coding: utf-8 -*-
import humanize
import datetime
from dateutil import tz

from flask import Blueprint, request, redirect, url_for, render_template, abort
from flask_login import login_required

from asabridge import validators

from . import readinglist

blueprint = Blueprint('readinglist', __name__, static_folder='../static')


@blueprint.route('/readinglist/add', methods=['POST'])
@login_required
def add_readinglist_item():
    url = request.form['url'] or ''
    validator = validators.URLValidator()
    try:
        validator(url)
    except validators.ValidationError as error:
        abort(400, error.message)
    readinglist.add_readinglist_item(url)
    return redirect(url_for('readinglist.get_readinglist_items'))


@blueprint.route('/readinglist/delete', methods=['POST'])
@login_required
def delete_readinglist_item():
    index = request.form['index'] or -1
    readinglist.delete_readinglist_item(index)
    return redirect(url_for('readinglist.get_readinglist_items'))


@blueprint.route('/readinglist', methods=['GET'])
@login_required
def get_readinglist_items():
    entries = readinglist.get_readinglist()
    for entry in entries:
        date = datetime.datetime.now(tz.tzlocal()) - entry['DateAdded']
        entry['DateAdded'] = humanize.naturaltime(date)
    return render_template('readinglist/readinglist.html', entries=entries)
