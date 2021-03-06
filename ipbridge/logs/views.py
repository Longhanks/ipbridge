# -*- coding: utf-8 -*-
from flask import Blueprint, current_app
from flask_login import current_user
from flask_socketio import disconnect, emit

import functools
import shlex
import subprocess

from ipbridge.extensions import socketio

blueprint = Blueprint('logs', __name__)


def ws_login_required(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@socketio.on('request-initial-data', namespace='/logstream')
@ws_login_required
def on_request_initial():
    current_app.logger.info('Log stream client wants initial data.')
    try:
        cmd = '/usr/bin/tail -n 200 ' + current_app.config['LOG_FILE_PATH']
        out = subprocess.check_output(
            shlex.split(cmd),
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
        )
        out = out[: len(out) - 1]
    except subprocess.CalledProcessError as e:
        out = str(e)
    emit('initial-data', {'data': out})


@socketio.on('connect', namespace='/logstream')
@ws_login_required
def on_connect():
    current_app.logger.info('Log stream client connected.')


@socketio.on('disconnect', namespace='/logstream')
@ws_login_required
def on_disconnect():
    current_app.logger.info('Log stream client disconnected.')


@socketio.on_error_default
def on_error(e):
    current_app.logger.error('Error during log stream session: ' + str(e))
