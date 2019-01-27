# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from flask_login import login_required
from flask.helpers import get_debug_flag


blueprint = Blueprint('contacts', __name__)


@blueprint.route('/api/contacts', methods=['GET'])
@login_required
def get_contacts():
    if not get_debug_flag():
        from . import contacts

        return jsonify(
            [
                {**contact.serialize(), 'display_str': str(contact)}
                for contact in contacts.get_contacts()
            ]
        )

    contacts = []
    for i in range(5):
        contacts.append(
            {
                'given_name': f'Testy #{i}',
                'family_name': 'McTestFace',
                'nick_name': 'Tester',
                'phone_numbers': [
                    {'country_code': 'CH', 'value': '+41 44 668 18 00'}
                ],
                'email_addresses': 'testy@tester.com',
                'image_data': None,
                'display_str': f'Tester (Testy #{i} McTestFace): '
                '+41 44 668 18 00, testy@tester.com',
            }
        )
    return jsonify(contacts)
