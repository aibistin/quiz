# app/__init__.py
import logging
import os
from flask import current_app, Flask, request
# from config import Config
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging.handlers import RotatingFileHandler

# Attach these modules to the current application
db = SQLAlchemy()
migrate = Migrate()


# def create_app(config_class=Config):
def create_app(config_name):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    # Register various services
    ###########################
    # blueprints for the application sub directries
    # The bp import must be first
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

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