# -*- coding: utf-8 -*-
import simplepam
from flask import Flask

from asabridge import login, readinglist
from asabridge.extensions import cache, auth


def create_app():
    app = Flask(__name__.split('.')[0])
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
