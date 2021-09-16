import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """This adds to the existing Flask Config"""
    TITLE = "Data Science"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_SECONDS = 3600

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'quiz_dev_db.db')
    # Notifys of db changes - Adds a lot of overhead when True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

    # Notifys of db changes - Adds a lot of overhead when True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
