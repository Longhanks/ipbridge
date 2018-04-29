# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template

blueprint = Blueprint('login', __name__, static_folder='../static')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('Loggin in...')
    return render_template('login/login.html')
