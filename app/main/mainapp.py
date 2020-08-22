#!/usr/bin/python
# Author:   @BlankGodd_

from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user, logout_user
from . import main
from .. import db
from ..models import Coin_account, Cash_account,User
from ..generator import *

@main.route('/')
def index():
    return render_template('index.html')


"""Authentication"""
@main.route('/login', methods=['GET','POST'])
def login():
    if method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and validate_pass(user, password):
            return redirect(url_for('.home'))
        flash('Invalid Username or Password!')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))

@main.route('/register/cash', methods=['GET','POST'])
def register_cash():
        if method == 'POST':
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            password = request.form.get('password')
            cpassword = request.form.get('cpassword')
            phone = request.form.get('phone')
            location = request.form.get('location')

            if User.query.filter_by(email=email).first():
                flash("Email already registered!")
            elif password != cpassword:
                flash("Passwords do not match!")
            elif not re.fullmatch(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", email):
                flash('Enter valid email')
            # check if phone is valid
            else:
                password = password_gen(password)
                
                
