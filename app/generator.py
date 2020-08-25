#!/usr/bin/python
# Author:   @BlankGodd_

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .models import User
from flask import current_app

def password_gen(password):
    password_hash = generate_password_hash(password)
    return password_hash

def validate_pass(user, password):
    return check_password_hash(user.password_hash, password)

def gen_acc_id(user_id):
    acc_id = []
    user_id = str.encode(str(user_id))
    while len(cash_id) < 5:
        hashh = generate_password_hash(user_id)
        v = len(hashh)
        u = v-15
        for j in range(u,v):
            try:
                acc_id.append(int(hashh[j]))
            except:
                pass
    if len(acc_id) > 5:
        a = len(acc_id) - 5
        for g in range(a):
            del acc_id[-g]
    acc_id = [str(i) for i in acc_id]
    return ''.join(acc_id)

def gen_confirm_token(user):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    return s.dumps({'confirm': user.id})

def confirm_token(user, token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return False
    if data.get('confirm') != user.id:
        return False
    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    return True

