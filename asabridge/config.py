# -*- coding: utf-8 -*-

bind = '127.0.0.1:12136'
logger_class = 'asabridge.gunicorn_isolog.IsoLogger'
loglevel = 'debug'
workers = 1
worker_class = 'eventlet'


class Config(object):
    ERROR_FMT = r'[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s'
    SECRET_KEY = b'Z\xb2\xb7S\xd9D\xe7\x05\xc7\r\xf2dR\xd9\xe9n'  # Change me!
    REDIS_URL = 'redis://localhost:6379'
    CACHE_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_KEY_PREFIX': 'adabridge-cache:',
        'CACHE_REDIS_HOST': 'localhost',
        'CACHE_REDIS_PORT': '6379',
        'CACHE_REDIS_URL': REDIS_URL
    }
    READING_LIST_UNSAVED_KEY = 'readinglist:unsaved'
    READING_LIST_DELETED_KEY = 'readinglist:deleted'
    IMAGE_CACHE_PATH = '/tmp/asabridge/imagecache'


class ProductionConfig(Config):
    PREFERRED_URL_SCHEME = 'https'
    SERVER_NAME = '<YOUR_HOSTNAME>'
    LOG_FILE_PATH = '<YOUR_LOG_FILE>'


class DevelopmentConfig(Config):
    CACHE_CONFIG = {**Config.CACHE_CONFIG, 'CACHE_KEY_PREFIX': 'debug:adabridge-cache:'}
    SERVER_NAME = None
    LOG_FILE_PATH = '/tmp/asabridge/log/asabridge.log'
