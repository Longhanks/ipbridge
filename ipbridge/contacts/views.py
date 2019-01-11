# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_login import login_required

from . import contacts

blueprint = Blueprint('contacts', __name__)


@blueprint.route('/api/contacts', methods=['GET'])
@login_required
def get_contacts():
    return jsonify(
        [
            {**contact.serialize(), 'display_str': str(contact)}
            for contact in contacts.get_contacts()
        ]
    )
