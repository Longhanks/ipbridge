# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, redirect, url_for
from flask_login import login_required


blueprint = Blueprint('logs', __name__, static_folder='../static')


@blueprint.route('/logs', methods=['GET'])
@login_required
def logs():
    logs_abs_url = str(url_for('logs.logs', _external=True))
    root_url = logs_abs_url[:-len('/logs')]
    rtail_url = root_url.replace('12137', '12139')
    current_app.logger.debug(f'constructed {rtail_url}')
    return redirect(rtail_url)
