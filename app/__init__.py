#!/usr/bin/python
# Author:   @BlankGodd_

from flask import *
from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import 
from config import config

mail = Mail()
