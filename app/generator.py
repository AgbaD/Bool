#!/usr/bin/python
# Author:   @BlankGodd_

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .models import User

def password_gen(password):
    password_hash = generate_password_hash(password)
    return password_hash

def validate_pass(user, password):
    return check_password_hash(user.password_hash, password)

def gen_cash_id():
    pass

def gen_coin_id():
    pass