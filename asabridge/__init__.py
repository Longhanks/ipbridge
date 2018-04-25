#!/usr/bin/env python3

from __future__ import print_function

import sys

if sys.version_info[0] < 3 or (sys.version_info[0] and sys.version_info[1] < 3):
    print('Requires Python >= 3.4.')
    sys.exit(1)

# System imports.
from pathlib import Path
import simplepam
import humanize
import datetime
from dateutil import tz

# Flask imports.
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth

# asabridge imports.
if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from asabridge import readinglist
from asabridge import validators

# Create SSL context.
certs = Path(__file__).resolve().parent / 'certs'
if certs.exists() and certs.is_dir():
    ssl_context = (str(certs / 'fullchain.pem'), str(certs / 'privkey.pem'))
else:
    ssl_context = None

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    return simplepam.authenticate(username, password)

@app.route('/readinglist', methods=['GET', 'POST'])
@auth.login_required
def get_readinglist_items():
    if request.method == 'GET':
        return jsonify(readinglist.get_readinglist())
    else:
        validator = validators.URLValidator()
        url = request.args.get('url') or ''
        try:
            validator(url)
        except validators.ValidationError as error:
            return jsonify(error.message)
        readinglist.add_readinglist_item(url)
        return jsonify(url)

@app.route('/front/readinglist/add', methods=['POST'])
@auth.login_required
def front_add_readinglist_item():
    url = request.form['url'] or ''
    validator = validators.URLValidator()
    try:
        validator(url)
    except validators.ValidationError as error:
        return jsonify(error.message)
    readinglist.add_readinglist_item(url)
    return redirect(url_for('front_get_readinglist_items'))

@app.route('/front/readinglist', methods=['GET'])
@auth.login_required
def front_get_readinglist_items():
    entries = readinglist.get_readinglist()
    for entry in entries:
        human_date = humanize.naturaltime(datetime.datetime.now(tz.tzlocal()) - entry['DateAdded'])
        entry['DateAdded'] = human_date
    return render_template('readinglist.html', entries=entries)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12137, debug=False, ssl_context=ssl_context)

