# -*- coding: utf-8 -*-

APP_NAME = 'nano'

class BaseConfig(object):

    DEBUG = False
    TESTING = False

    SECRET_KEY = '93486af20eeb8f74c4c2af23b79fc739797ff9bb09240d67'

class DefaultConfig(BaseConfig):

    SERVER_NAME = 'nanoinvoice.dev:5000'
    DEBUG = True
    CSRF_ENABLED = True

    SQLALCHEMY_ECHO = False

    # Sqlite
    SQLALCHEMY_DATABASE_URI = None

    # To create log folder.
    # $ sudo mkdir -p /var/log/fbone
    # $ sudo chown $USER /var/log/fbone
    DEBUG_LOG = '/var/log/flask/nanoinvoice-debug.log'

    ACCEPT_LANGUAGES = ['en']
    BABEL_DEFAULT_LOCALE = 'en'

    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Email (Flask-email)
    # https://bitbucket.org/danjac/flask-mail/issue/3/problem-with-gmails-smtp-server
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    DEFAULT_MAIL_SENDER = '%s@gmail.com' % MAIL_USERNAME

    UPLOAD_DIR = '/srv/nanoinvoice.com/files/uploads'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    # web assets
    ASSETS_DEBUG = False
    ASSETS_AUTO_BUILD = True
    JST_COMPILER = '_.template'

    GOCARDLESS_ENVIRONMENT = 'sandbox'

    # these are the test keys
    STRIPE_PUBLIC_KEY = None
    STRIPE_SECRET_KEY = None

class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

