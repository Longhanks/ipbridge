# -*- coding: utf-8 -*-
bind = '127.0.0.1:12136'
logger_class = 'asabridge.gunicorn_isolog.IsoLogger'
loglevel = 'debug'
workers = 1
worker_class = 'eventlet'
