# -*- coding: utf-8 -*-
import logging
import os
from flask import Flask
from flask.helpers import get_debug_flag

from asabridge import debug, index, login, logs, readinglist
from asabridge.extensions import cache, cache_config, login_manager, socketio
from asabridge.isoformatter import IsoFormatter
from asabridge.user import User

ERROR_FMT = r'%(asctime)s [%(process)d] [%(levelname)s] %(message)s)'


def create_app() -> Flask:
    app = Flask(__name__.split('.')[0])
    is_werkzeug = os.environ.get("WERKZEUG_RUN_MAIN") == "true"

    if is_werkzeug:
        for handler in app.logger.handlers:
            handler.setFormatter(IsoFormatter(ERROR_FMT))

    if __name__ != '__main__' and not get_debug_flag() and not is_werkzeug:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    # Change me!
    app.secret_key = b'Z\xb2\xb7S\xd9D\xe7\x05\xc7\r\xf2dR\xd9\xe9n'
    register_extensions(app)
    register_blueprints(app)
    app.logger.info('Finished app initialization.')
    return app


def register_extensions(app):
    """Register Flask extensions."""
    if app.debug:
        app.logger.debug('Using CACHE_KEY_PREFIX=debug:adabridge-cache:')
        cache_config['CACHE_KEY_PREFIX'] = 'debug:adabridge-cache:'
    cache.init_app(app, config=cache_config)
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'
    login_manager.login_message = None
    login_manager.user_loader(lambda _id: User(_id))
    socketio.init_app(app, message_queue='redis://')


def register_blueprints(app):
    """Register Flask blueprints."""
    if app.debug:
        app.register_blueprint(debug.views.blueprint)
    app.register_blueprint(index.views.blueprint)
    app.register_blueprint(login.views.blueprint)
    app.register_blueprint(logs.views.blueprint)
    app.register_blueprint(readinglist.views.blueprint)
