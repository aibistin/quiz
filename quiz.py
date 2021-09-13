# from app import create_app, cli, db
import os
from app import create_app, db, cli
from app.models import User, Question, UserQuestion, Option, File


# app = create_app()
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# Use some functions from app/cli.py
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    """For using the flask_shell"""
    return {'db': db, 'User': User, 'Question': Question, 'Option': Option, 'File': File, 'UserQuestion': UserQuestion}


@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
