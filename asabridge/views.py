# system imports.
import simplepam
import humanize
import datetime
from dateutil import tz
import urllib

# flask imports.
from flask import request, jsonify, redirect, url_for, render_template, abort

from asabridge.app import app, auth
from asabridge import readinglist
from asabridge import validators

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('Loggin in...')
    return render_template('login.html')


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
        abort(400, error.message)
    readinglist.add_readinglist_item(url)
    return redirect(url_for('front_get_readinglist_items'))


@app.route('/front/readinglist/delete', methods=['POST'])
@auth.login_required
def front_delete_readinglist_item():
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
    return redirect(url_for('front_get_readinglist_items'))


@app.route('/front/readinglist', methods=['GET'])
@auth.login_required
def front_get_readinglist_items():
    entries = readinglist.get_readinglist()
    for entry in entries:
        date = datetime.datetime.now(tz.tzlocal()) - entry['DateAdded']
        entry['DateAdded'] = humanize.naturaltime(date)
    return render_template('readinglist.html', entries=entries)
