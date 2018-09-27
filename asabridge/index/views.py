# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask_login import login_required


blueprint = Blueprint('index', __name__, static_folder='../static')


@blueprint.route('/old-index', methods=['GET'])
@login_required
def index():
    return render_template('index/index.html')
