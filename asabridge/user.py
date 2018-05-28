# -*- coding: utf-8 -*-

from flask_login import UserMixin


class User(UserMixin):
    id: str

    def __init__(self, _id: str):
        self.id = _id
        self.name = id

    def __repr__(self):
        return self.id
