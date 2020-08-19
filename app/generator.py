#!/usr/bin/python
# Author:   @BlankGodd_

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .models import User

def password_gen(password):
    pass

def password_verify(password):
    pass