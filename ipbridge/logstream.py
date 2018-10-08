# -*- coding: utf-8 -*-

"""

logstream.py
Streams the log file content via tail -F to ipbridge.

argv:
1: log file path
2: redis URL

"""

from collections import deque
import subprocess
import sys

from pid import PidFile, PidFileAlreadyLockedError

from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

try:
    with PidFile(pidname='logstream', piddir='/tmp') as pid_file:
        socketio = SocketIO(message_queue=sys.argv[2])

        lines_cache = deque(maxlen=10)

        popen = subprocess.Popen(['/usr/bin/tail', '-n', '10', '-F', sys.argv[1]], stdout=subprocess.PIPE,
                                 universal_newlines=True)
        while True:
            try:
                stdout_line = popen.stdout.readline()
                stdout_line = stdout_line[:len(stdout_line) - 1]
                lines_cache.append(stdout_line)
                socketio.emit('new-log-line', {'data': list(lines_cache)}, namespace='/logstream')
            except subprocess.CalledProcessError as tail_error:
                socketio.emit('new-log-line', {'data': str(tail_error)}, namespace='/logstream')
                sys.exit(1)
except PidFileAlreadyLockedError:
    pass
