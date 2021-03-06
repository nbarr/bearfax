# -*- coding: utf-8 -*-

import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler

from flask import Flask

from application.routes import configure_routes
from application.common import filters, json_enc
from application.extensions import csrf, mail, security, socketio, recaptcha
from application.database.datastore import RawSQLAUserDatastore
from application.database.engine import session
from application.models import User, Role


def init(name):
    app = Flask(name)

    configure_app(app)
    configure_logging(app)
    configure_extensions(app)
    configure_routes(app)

    return app


def configure_app(app):
    app.config.from_object('application.config.flask_settings')

    app.jinja_env.globals['url_for_static'] = filters.url_for_static

    # Define useful filters
    app.jinja_env.filters['app_settings_item'] = filters.app_settings_item
    app.jinja_env.filters['to_json'] = filters.to_json
    app.jinja_env.filters['date'] = filters.as_date

    app.json_encoder = json_enc.ExtendedJSONEncoder


def configure_logging(app):
    handler = RotatingFileHandler('logs/flask.log', maxBytes=2 * 1024 * 1024, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(Formatter('%(asctime)s | %(levelname)7s | %(module)s:%(funcName)s:%(lineno)4s | %(message)s'))
    app.logger.addHandler(handler)


def configure_extensions(app):
    datastore = RawSQLAUserDatastore(session, User, Role)
    security.init_app(app, datastore)
    csrf.init_app(app)
    mail.init_app(app)
    recaptcha.init_app(app)

    socketio_kwargs = {
        'engineio_logger': app.config['DEBUG'],
        'json': json_enc
    }

    if app.config['REDIS_URI']:
        socketio_kwargs['message_queue'] = app.config['REDIS_URI']

    socketio.init_app(app, **socketio_kwargs)

flask_app = init(__name__)
