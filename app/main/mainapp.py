#!/usr/bin/python
# Author:   @BlankGodd_

from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Coin_account, Cash_account,User
from ..generator import *

@main.route('/')
def index():
    render_template('index.html')


"""Authentication"""
@main.route('/login', methods=['GET','POST'])
def login():
    if method == 'POST':
        pass
    return render_template('login.html')

