# -*- coding: utf-8 -*-
import simplepam
import logging
from flask import Flask
from flask.helpers import get_debug_flag

from asabridge import login, readinglist
from asabridge.extensions import cache, auth


def create_app():
    app = Flask(__name__.split('.')[0])
    if __name__ != '__main__' and not get_debug_flag():
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    cache.init_app(app)
    @auth.verify_password
    def login(username, password):
        return simplepam.authenticate(username, password)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(login.views.blueprint)
    app.register_blueprint(readinglist.views.blueprint)
