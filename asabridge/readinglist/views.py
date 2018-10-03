# -*- coding: utf-8 -*-
import humanize
import datetime
from dateutil import tz

from flask import Blueprint, request, abort, jsonify
from flask_login import login_required

from asabridge import validators

from . import readinglist

blueprint = Blueprint('readinglist', __name__)


@blueprint.route('/api/readinglist/add', methods=['POST'])
@login_required
def add_readinglist_item():
    payload = request.get_json()
    if payload is None:
        abort(400)
    url = payload.get('url', '')
    validator = validators.URLValidator()
    try:
        validator(url)
    except validators.ValidationError as error:
        abort(400, error.message)
    readinglist.add_readinglist_item(url)
    return '', 204


@blueprint.route('/api/readinglist/delete', methods=['POST'])
@login_required
def delete_readinglist_item():
    payload = request.get_json()
    if payload is None:
        abort(400)
    index = payload.get('index', '-1')
    try:
        index = int(index)
        if not index >= 0:
            raise ValueError('Index must be >= 0')
    except (TypeError, ValueError):
        abort(400, f'Invalid index: {index}')
    readinglist.delete_readinglist_item(index)
    return '', 204


@blueprint.route('/api/readinglist', methods=['GET'])
@login_required
def get_readinglist_items():
    entries = readinglist.get_readinglist()
    for entry in entries:
        delta_date = datetime.datetime.now(tz.tzlocal()) - entry.date
        entry.date = humanize.naturaltime(delta_date)
    return jsonify([entry.serialize() for entry in entries])
