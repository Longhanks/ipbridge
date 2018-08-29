# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess

from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

LOG_FILE_PATH = Path('/Users/aschulz/Projects/asabridge/log/asabridge.log')

socketio = SocketIO(message_queue='redis://localhost:6379')
popen = subprocess.Popen(['/usr/bin/tail', '-n', '0', '-F', LOG_FILE_PATH], stdout=subprocess.PIPE,
                         universal_newlines=True)
while True:
    try:
        stdout_line = popen.stdout.readline()
        stdout_line = stdout_line[:len(stdout_line) - 1]
        socketio.emit('new-log-line', {'data': stdout_line}, namespace='/logstream')
    except subprocess.CalledProcessError as tail_error:
        socketio.emit('new-log-line', {'data': str(tail_error)}, namespace='/logstream')
