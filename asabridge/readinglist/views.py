# -*- coding: utf-8 -*-
import simplepam
import humanize
import datetime
from dateutil import tz
import urllib

from flask import Blueprint, request, redirect, url_for, render_template, abort, current_app

from asabridge import validators
from asabridge.extensions import auth

from . import readinglist

blueprint = Blueprint('readinglist', __name__, static_folder='../static')


@blueprint.route('/readinglist/add', methods=['POST'])
@auth.login_required
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
@auth.login_required
def delete_readinglist_item():
    url = request.form['URLString'] or ''
    validator = validators.URLValidator()
    try:
        validator(url)
    except validators.ValidationError as error:
        abort(400, error.message)
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.hostname
    if host.startswith('www.'):
        host = host[4:]
    previewText = request.form['PreviewText'] or ''
    readinglist.delete_readinglist_item(host, previewText)
    return redirect(url_for('readinglist.get_readinglist_items'))


@blueprint.route('/readinglist', methods=['GET'])
@auth.login_required
def get_readinglist_items():
    entries = readinglist.get_readinglist()
    for entry in entries:
        date = datetime.datetime.now(tz.tzlocal()) - entry['DateAdded']
        entry['DateAdded'] = humanize.naturaltime(date)
    return render_template('readinglist/readinglist.html', entries=entries)
