# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_login import login_required

from . import icloudtabs


blueprint = Blueprint('icloudtabs', __name__)


@blueprint.route('/api/icloudtabs', methods=['GET'])
@login_required
def get_icloud_tabs():
    return jsonify(icloudtabs.get_icloud_tabs())
