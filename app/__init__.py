# app/__init__.py
import logging
import os
import rq
from flask import current_app, Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from logging.handlers import RotatingFileHandler

# Attach these modules to the current application
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # Register various services
    ###########################
    # blueprints for the application sub directries
    # The bp import must be first
    # from app.errors import bp as errors_bp
    # app.register_blueprint(errors_bp)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    # API Blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


    if not app.debug:

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/quiz.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Quiz startup')

    return app


# Import models last to prevent circular references
from app import models