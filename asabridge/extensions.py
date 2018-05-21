# -*- coding: utf-8 -*-
from flask_caching import Cache
from flask_login import LoginManager

cache_config = {
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'adabridge-cache:',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://localhost:6379'
}

cache = Cache()
login_manager = LoginManager()
