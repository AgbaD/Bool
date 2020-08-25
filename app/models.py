#!/usr/bin/python
# Author:   @BlankGodd_

from datetime import datetime
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class Account(db.Model, UserMixin):
    __tablename__ = 'account'
    _id = db.Column(db.Integer, primary_key=True)
    _amount = db.Column(db.Float)

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)
        self._amount = 3.00

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, default=False)
    fullname = db.Column(db.String(64))
    location = db.Column(db.String(64))
    acc_id = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean, default=False)
    account_name = db.Column(db.String(64))
    account_number = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email == current_app.config['BOOL_ADMIN']:
            self.is_admin = True

    def __repr__(self):
        return '<User %r>' % self.email

class Plans(UserMixin, db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64))
    title = db.Column(db.String(64))
    rate = db.Column(db.Integer)
    total = db.Column(db.Integer)

class Savings(UserMixin, db.Model):
    __tablename__ = 'savings'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, default=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))