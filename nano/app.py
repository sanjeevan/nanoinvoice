import os

from flask import Flask, request, render_template
from flaskext.babel import Babel, format_date
from flask.ext.assets import Environment, Bundle
from flask.ext.login import current_user

from nano import utils
from nano.models import User
from nano.config import DefaultConfig, APP_NAME
from nano.extensions import db, mail, cache, login_manager

from nano.views import js
from nano.views import account
from nano.views import home
from nano.views import file
from nano.views import client, payment, invoice, invoice_item, settings
from nano.views import portal

# For import *
__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    account,
    home,
    file,
    payment,
    invoice,
    client,
    invoice_item,
    js,
    settings,
    portal
)

def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = APP_NAME
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    # project root path
    proj_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    instance_path = os.path.join(proj_path, 'instance')

    app = Flask(app_name, instance_path=instance_path, instance_relative_config=True)
    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_template_filters(app)
    configure_error_handlers(app)
    configure_assets(app)

    return app


def configure_app(app, config):
    """Configure app from object, parameter and env."""

    app.config.from_object(DefaultConfig)
    if config is not None:
        app.config.from_object(config)

    # Override setting by instance/application.cfg file
    app.config.from_pyfile('application.cfg')


def configure_extensions(app):
    # sqlalchemy
    db.init_app(app)
    # mail
    mail.init_app(app)
    # cache
    cache.init_app(app)

    # babel
    babel = Babel(app)
    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES')
        return request.accept_languages.best_match(accept_languages)

    # login.
    login_manager.login_view = 'account.login'
    login_manager.refresh_view = 'account.reauth'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    login_manager.setup_app(app)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_template_filters(app):
    @app.template_filter()
    def pretty_date(value):
        return utils.pretty_date(value)

    @app.template_filter()
    def format_currency(value):
        return "{:,.2f}".format(value)

    @app.template_filter()
    def fmt_date(value):
        return format_date(value)


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # skip debug and test mode.
        return

    import logging
    from logging.handlers import RotatingFileHandler, SMTPHandler

    # Set info level on logger, which might be overwritten by handers.
    app.logger.setLevel(logging.INFO)

    debug_log = os.path.join(app.root_path, app.config['DEBUG_LOG'])
    file_handler = logging.handlers.RotatingFileHandler(debug_log, maxBytes=100000, backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(file_handler)

def configure_hook(app):
    @app.before_request
    def before_request():
        pass

def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_page(error):
        return render_template("errors/method_not_allowed.html"), 405

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500

def configure_assets(app):
    assets = Environment(app)

    js_lib = Bundle('src/js/lib/underscore.js',
                    'src/js/lib/jquery-1.8.3.js',
                    'src/js/lib/backbone.js',
                    'src/js/lib/backbone-relational.js',
                    'src/js/lib/sprintf-0.7-beta1.js',
                    'src/js/vendor/select2/select2.js',
                    'src/js/vendor/Pikaday/pikaday.js',
                    'src/js/vendor/facebox/facebox.js',
                    'src/js/vendor/highcharts/highcharts.src.js',
                    'src/js/vendor/bootstrap/bootstrap-alert.js',
                    'src/js/vendor/bootstrap/bootstrap-modal.js',
                    'src/js/vendor/bootstrap/bootstrap-modalmanager.js',
                    'src/js/lib/upclick.js',
                    filters='yui_js', output='dist/js/libs.js')

    js_app = Bundle('src/js/app/app.js',
                    'src/js/app/models/all.js',
                    'src/js/app/views/DraftInvoiceView.js',
                    'src/js/app/views/EditInvoiceItemView.js',
                    'src/js/app/views/InvoiceFormView.js',
                    'src/js/app/views/NewInvoiceItemView.js',
                    filters='yui_js', output='dist/js/app.js')

    js_templates = Bundle('src/js/app/templates/*.html', output='dist/js/templates.js',
                          filters='jst')

    css_global = Bundle('src/sass/screen.scss',
                        filters='scss', output='dist/css/screen.css')

    css_pdf = Bundle('src/sass/pdf.scss',
                     filters='scss', output='dist/css/pdf.css')

    assets.register('js_lib', js_lib)
    assets.register('js_app', js_app)
    assets.register('js_templates', js_templates)
    assets.register('css_global', css_global)
    assets.register('css_pdf', css_pdf)


