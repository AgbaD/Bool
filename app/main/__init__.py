#!/usr/bin/python
# Author:   @BlankGodd_

from flask import Blueprint

main = Blueprint('main', __name__)

from . import mainapp
