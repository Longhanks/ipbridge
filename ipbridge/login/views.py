# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, request, abort
from flask_login import login_user, current_user, logout_user
import simplepam

from ipbridge.user import User


blueprint = Blueprint('login', __name__)


@blueprint.route('/api/authenticated', methods=['GET'])
def authenticated():
    if current_user.is_authenticated:
        return '', 204
    else:
        abort(401)


@blueprint.route('/api/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return '', 204
    payload = request.get_json()
    if payload is None:
        abort(401)
    username = payload.get('username', '')
    password = payload.get('password', '')
    remember_me = payload.get('rememberMe', '')
    current_app.logger.info(f'Login attempt, username={username}, remember={remember_me}')
    if not simplepam.authenticate(username, password):
        abort(401)
    login_user(User(username), remember=remember_me)
    return '', 204


@blueprint.route('/api/logout', methods=['POST'])
def logout():
    logout_user()
    return '', 204
