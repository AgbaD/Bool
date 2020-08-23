#!/usr/bin/python
# Author:   @BlankGodd_

from flask import *
from flask_login import login_required, current_user
from flask_login import login_user, logout_user
from . import main
from .. import db
from ..models import Coin_account, Cash_account,User
from ..generator import *

import re

@main.route('/')
def index():
    return render_template('index.html')


"""Authentication"""
@main.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and validate_pass(user, password):
            login_user(user, request.form.get('remember_me'))
            return redirect(url_for('.profile'))
        flash('Invalid Username or Password!')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))

@main.route('/create_acc')
def create_acc():
    return render_template('create_acc.html')

@main.route('/register/cash', methods=['GET','POST'])
def register_cash():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        phone = request.form.get('phone')
        location = request.form.get('location')

        #add schema validation here

        if User.query.filter_by(email=email).first():
            flash("Email already registered!")
        elif password != cpassword:
            flash("Passwords do not match!")
        elif not re.fullmatch(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", email):
            flash('Enter valid email')
        # check if phone is valid
        else:
            # hash password
            password = password_gen(password)
            user = User(email=email,password_hash=password,
                    fullname=firstname+" "+lastname,
                    phone=phone, location=location)
            db.session.add(user)
            db.session.commit()
            # open cash account and get id
            cash_id = create_cash_acc(user.id)
            user.cash_id = cash_id
            db.session.add(user)
            db.session.commit()
            
            # create confirmation token
            token = get_confirm_token(user)
            # send email
            flash('Check email to confirm account!')
            return redirect(url_for('.login'))

        return render_template('register.html')
    return render_template('register.html')

@main.route('/register/coin', methods=['GET','POST'])
def register_coin():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        phone = request.form.get('phone')
        location = request.form.get('location')

        #add schema validation here

        if User.query.filter_by(email=email).first():
            flash("Email already registered!")
        elif password != cpassword:
            flash("Passwords do not match!")
        elif not re.fullmatch(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", email):
            flash('Enter valid email')
        # check if phone is valid
        else:
            # hash password
            password = password_gen(password)
            user = User(email=email,password_hash=password,
                    fullname=firstname+" "+lastname,
                    phone=phone, location=location)
            db.session.add(user)
            db.session.commit()
            # open cash account and get id
            coin_id = create_coin_acc(user.id)
            user.coin_id = coin_id
            db.session.add(user)
            db.session.commit()
            
            # create confirmation token
            token = get_confirm_token(user)
            # send email
            flash('Check email to confirm account!')
            return redirect(url_for('.login'))

        return render_template('register.html')
    return render_template('register.html')

def create_cash_acc(user_id):
    # generate cash account id
    acc_id = int(gen_cash_id(user_id))
    # check db to see if its unique
    que = Cash_account.query.filter_by(_id=acc_id).first()
    while que:
        acc_id = int(gen_cash_id(user_id))
        que = Cash_account.query.filter_by(_id=acc_id).first()
    # add account to db if unique
    acc = Cash_account(_id=acc_id)
    db.session.add(acc)
    db.session.commit()
    return acc_id

def create_coin_acc(user_id):
    # generate coin account id
    acc_id = gen_coin_id(user_id)
    # check db to see if its unique
    que = Coin_account.query.filter_by(_id=acc_id).first()
    while que:
        acc_id = gen_coin_id(user_id)
        que = Coin_account.query.filter_by(_id=acc_id).first()
    # add account to db if unique
    acc = Coin_account(_id=acc_id)
    db.session.add(acc)
    db.session.commit()
    return acc_id

@main.route('/confirmtoken/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('.profile'))
    if confirm_token(current_user, token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('.profile'))

# confirm account from profile view func

"""Done with Authentication"""

"""Profiling"""
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)