#!/usr/bin/python
# Author:   @BlankGodd_

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sFDEd/sdsd/x/wsd-000/x343d?dsfsdf/sdsdsdsd\\sSJLD34sd'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[Bool]'
    BOOL_MAIL_SENDER = 'Bool Admin <admin@bool.com>'
    BOOL_ADMIN = os.environ.get('BOOL_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SSL_DISABLE = True
    

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    DEBUG = True


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    TESTING = True


class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class Heroku(Production):
    @classmethod
    def init_app(cls, app):
        Production.init_app(app)
        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))
        
config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development,
    'heroku': Heroku
}
