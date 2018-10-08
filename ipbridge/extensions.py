# -*- coding: utf-8 -*-
from flask_caching import Cache
from flask_login import LoginManager
from flask_socketio import SocketIO

cache = Cache()
login_manager = LoginManager()
socketio = SocketIO()
