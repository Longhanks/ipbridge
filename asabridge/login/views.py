# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, current_app, request, abort, url_for, redirect
from flask_login import login_user, current_user, logout_user
from urllib.parse import urlparse, urljoin
import simplepam

from asabridge.user import User


blueprint = Blueprint('login', __name__, static_folder='../static')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next = request.args.get('next')
        current_app.logger.debug('Trying to log in as ' + username + '...')
        current_app.logger.debug('next: ' + str(next))
        if not simplepam.authenticate(username, password):
            current_app.logger.debug('Login attempt for ' + username + ' failed.')
            return redirect(url_for('login.login', next=next))
        login_user(User(username))
        if not is_safe_url(next):
            return url_for('index.index')
        return redirect(next or url_for('index.index'))
    return render_template('login/login.html')

@blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login.login'))
