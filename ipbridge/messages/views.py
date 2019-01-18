# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_login import login_required

from . import messages

blueprint = Blueprint('messages', __name__)


@blueprint.route('/api/chats', methods=['GET'])
@login_required
def get_chats():
    return jsonify(messages.get_chats())
