# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, current_app, request, abort, url_for, redirect, session
from flask_login import login_user, current_user, logout_user
from urllib.parse import urlparse, urljoin
import simplepam

from asabridge.user import User


blueprint = Blueprint('login', __name__, static_folder='../static')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@blueprint.route('/isAuth', methods=['GET'])
def is_logged_in():
    if current_user.is_authenticated:
        return '', 204
    else:
        abort(401)


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
        remember_me = request.form.get('remember_me') == 'on' or False
        next_link = request.args.get('next')
        current_app.logger.debug(f'Login attempt, username={username}, remember={remember_me}, next={next_link}')
        if not simplepam.authenticate(username, password):
            current_app.logger.debug(f'Login attempt for {username} failed.')
            session['failed_login_attempt'] = True
            return redirect(url_for('login.login', next=next_link))
        current_app.logger.debug(f'Login for {username} succeeded.')
        login_user(User(username), remember=remember_me)
        if not is_safe_url(next_link):
            return url_for('index.index')
        return redirect(next_link or url_for('index.index'))
    else:
        abort(400)


@blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login.login'))
