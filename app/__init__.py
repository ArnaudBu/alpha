from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import environ

db = SQLAlchemy()
login_manager = LoginManager()

from app.back.models.user import User
from app.front.dash.dashboard import init_dashboard


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('front', 'back'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()
        user = User.query.filter_by(email=environ.get('ADMIN_EMAIL', 'osef')).first()
        if not user:
            user_data = User(
                email=environ.get('ADMIN_EMAIL', 'osef'),
                username=environ.get('ADMIN_USER', 'osef'),
                password=environ.get('ADMIN_PASSWORD', 'osef'),
                admin=True
            )
            db.session.add(user_data)
            db.session.commit()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

    # Prevent accessing dash without authentication
    @app.before_request
    def before_request_func():
        if not current_user.is_authenticated and request.endpoint.startswith(r"/dash/"):
            return redirect(url_for('front_blueprint.login')), 403

def configure_logs(app):
    basicConfig(filename='error.log', level=DEBUG)
    logger = getLogger()
    logger.addHandler(StreamHandler())


def create_app(config):
    app = Flask(__name__, static_folder='front/static')
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    configure_logs(app)
    app = init_dashboard(app)
    return app
