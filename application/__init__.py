#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Creaded on 2017/5/6
"""__DOC__"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_moment import Moment
from config import config, MyJSONEncoder
from flask_uploads import UploadSet, configure_uploads, patch_request_class


db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
# login_manager.anonymous_user = MyAnonymousUser

# config flask-uploads set
csvfiles = UploadSet('csvfiles', ('csv',))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # CsrfProtect(app)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    # config flask-uploads
    configure_uploads(app, csvfiles)
    patch_request_class(app)  # set maximum file size, default is 16MB

    # set json_encoder
    app.json_encoder = MyJSONEncoder

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from .invoice import invoice_bp
    app.register_blueprint(invoice_bp, url_prefix="/invoice")

    from .main import main_bp
    app.register_blueprint(main_bp)

    return app

if __name__ == '__main__':
    pass
