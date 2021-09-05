import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """This adds to the existing Flask Config"""
    TITLE = "Data Science"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_SECONDS = 3600
    # Database Stuff
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Notifys of db changes
    SQLALCHEMY_TRACK_MODIFICATIONS = False
