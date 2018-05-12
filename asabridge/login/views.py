# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, current_app, request, abort, url_for, redirect, session
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse, urljoin
import simplepam

from asabridge.user import User


blueprint = Blueprint('login', __name__, static_folder='../static')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@blueprint.route('/isAuth', methods=['GET'])
def isAuth():
    if current_user.is_authenticated:
        return '', 204
    else:
        abort(401)


@blueprint.route('/logs', methods=['GET'])
@login_required
def logs():
    logs_abs_url = str(url_for('login.logs', _external=True))
    root_url = logs_abs_url[:-len('/logs')]
    rtail_url = root_url.replace('12137', '12139')
    current_app.logger.debug('constructed ' + rtail_url)
    return redirect(rtail_url)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    if request.method == 'GET':
        response = render_template('login/login.html')
        session.pop('failed_login_attempt', None)
        return response
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next = request.args.get('next')
        current_app.logger.debug('Trying to log in as ' + username + '...')
        current_app.logger.debug('next: ' + str(next))
        if not simplepam.authenticate(username, password):
            current_app.logger.debug('Login attempt for ' + username + ' failed.')
            session['failed_login_attempt'] = True
            return redirect(url_for('login.login', next=next))
        login_user(User(username))
        if not is_safe_url(next):
            return url_for('index.index')
        return redirect(next or url_for('index.index'))
    else:
        abort(400)

@blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login.login'))
