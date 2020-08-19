#!/usr/bin/python
# Author:   @BlankGodd_

from datetime import datetime
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class Account(db.Model, UserMixin):
    _id = db.Column(db.String(128), primary_key=True)
    _cash = db.Column(db.Float)
    _bitcoin = db.Column(db.Float)

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)
        self._bitcoin = 0.00001
        self._cash = 130.00

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    cash_id = db.Column(db.Integer)
    coin_id = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email = current_app.config['BOOL_ADMIN']:
            self.is_admin = True

    def __repr__(self):
        return '<User %r>' % self.username