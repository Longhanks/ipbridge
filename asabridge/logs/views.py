# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, Response, stream_with_context, current_app
from flask_login import login_required

from pathlib import Path
import subprocess

LOG_FILE_PATH = Path('/Users/aschulz/Projects/asabridge/log/asabridge.log')

blueprint = Blueprint('logs', __name__, static_folder='../static')


@blueprint.route('/logstream', methods=['GET'])
@login_required
def stream():
    def event_stream():
        current_app.logger.info('Log live stream started.')
        popen = subprocess.Popen(['/usr/bin/tail', '-n', '200', '-F', LOG_FILE_PATH],
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True)
        while True:
            try:
                stdout_line = popen.stdout.readline()
                yield f'data: {stdout_line}\n'
            except GeneratorExit as generator_exit:
                current_app.logger.info('Log live stream exited.')
                popen.stdout.close()
                popen.kill()
                raise generator_exit
            except subprocess.CalledProcessError as tail_error:
                yield f'data: {tail_error}\n\n'

    return Response(stream_with_context(event_stream()), mimetype='text/event-stream')


@blueprint.route('/logs', methods=['GET'])
@login_required
def logs():
    return render_template('logs/logs.html')
