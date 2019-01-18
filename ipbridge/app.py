# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path
import subprocess
import threading
import sys
from flask import Flask
from flask.helpers import get_debug_flag

from ipbridge import contacts, debug, login, logs, messages, readinglist
from ipbridge.extensions import cache, login_manager, socketio
from ipbridge.isoformatter import IsoFormatter
from ipbridge.user import User


class ConfigurationError(RuntimeError):
    pass


def create_app() -> Flask:
    app = Flask(__name__.split('.')[0])

    if get_debug_flag():
        app.config.from_object('ipbridge.config.DevelopmentConfig')
    else:
        app.config.from_object('ipbridge.config.ProductionConfig')

    is_werkzeug = os.environ.get("WERKZEUG_RUN_MAIN") == "true"

    if is_werkzeug:
        for handler in app.logger.handlers:
            handler.setFormatter(IsoFormatter(app.config['ERROR_FMT']))

    if __name__ != '__main__' and not get_debug_flag() and not is_werkzeug:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    try:
        check_configuration(app)
    except ConfigurationError as config_error:
        app.logger.error(f'Configuration error: {config_error}')
        sys.exit(1)

    if get_debug_flag():

        @app.after_request
        def after_request(response):
            origin = 'http://localhost:8080'
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = ','.join(
                ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
            )
            response.headers['Access-Control-Allow-Headers'] = ','.join(
                [
                    'accept',
                    'accept-encoding',
                    'authorization',
                    'content-type',
                    'dnt',
                    'origin',
                    'user-agent',
                    'x-csrftoken',
                    'x-requested-with',
                ]
            )
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response

    register_extensions(app)
    register_blueprints(app)

    def start_logstream():
        process = subprocess.Popen(
            [
                sys.executable,
                app.root_path + '/logstream.py',
                app.config['LOG_FILE_PATH'],
                app.config['REDIS_URL'],
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            app.logger.info('Requested log stream.')
            process.wait(timeout=5)
            app.logger.info(
                'Log stream process exited: '
                + 'There is already a running logstream.'
            )
        except subprocess.TimeoutExpired:
            app.logger.info('Keeping log stream up.')

    start_logstream_thread = threading.Thread(target=start_logstream)
    start_logstream_thread.start()
    app.logger.info('Finished app initialization.')
    return app


def check_configuration(app):
    log_file_path = Path(app.config['LOG_FILE_PATH'])
    if log_file_path.is_dir():
        raise ConfigurationError(
            f'LOG_FILE_PATH faulty: {log_file_path} is a directory!'
        )
    if not log_file_path.parent.exists():
        try:
            log_file_path.parent.mkdir(parents=True)
        except PermissionError:
            raise ConfigurationError(
                'LOG_FILE_PATH faulty: '
                + 'Permission denied while ensuring directories for '
                + f'{log_file_path}!'
            )
    try:
        open(log_file_path, 'a').close()
    except PermissionError:
        raise ConfigurationError(
            'LOG_FILE_PATH faulty: '
            + 'Permission denied for opening '
            + f'{log_file_path}!'
        )


def register_extensions(app):
    """Register Flask extensions."""
    cache.init_app(app, config=app.config['CACHE_CONFIG'])
    login_manager.init_app(app)
    login_manager.login_message = None
    login_manager.user_loader(lambda _id: User(_id))
    socketio.init_app(app, message_queue=app.config['REDIS_URL'])


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(contacts.views.blueprint)
    if app.debug:
        app.register_blueprint(debug.views.blueprint)
    app.register_blueprint(login.views.blueprint)
    app.register_blueprint(logs.views.blueprint)
    app.register_blueprint(messages.views.blueprint)
    app.register_blueprint(readinglist.views.blueprint)
