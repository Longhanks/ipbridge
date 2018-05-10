# -*- coding: utf-8 -*-

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = str(id)

    def __repr__(self):
        return self.id
