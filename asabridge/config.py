# -*- coding: utf-8 -*-
bind = '127.0.0.1:12136'
logger_class = 'asabridge.gunicorn_isolog.IsoLogger'
loglevel = 'debug'
workers = 1
worker_class = 'eventlet'


class Config(object):
    ERROR_FMT = r'[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s'
    SECRET_KEY = b'Z\xb2\xb7S\xd9D\xe7\x05\xc7\r\xf2dR\xd9\xe9n'  # Change me!


class ProductionConfig(Config):
    SERVER_NAME = '<YOUR_HOSTNAME>'
    PREFERRED_URL_SCHEME = 'https'


class DevelopmentConfig(Config):
    SERVER_NAME = None
