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

def gen_cash_id(user_id):
    cash_id = []
    while len(cash_id) < 10:
        hashh = generate_password_hash(user_id)
        for i in hashh:
            if isinstance(i,int):
                cash_id.append(i)
    return ''.join(cash_id)

def gen_coin_id(user_id):
    return generate_password_hash(user_id)

def gen_confirm_token(user):
    s = Serializer(current_app.config['SECRET_KEY'], expiration=3600)
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

