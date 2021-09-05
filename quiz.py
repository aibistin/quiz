# from app import create_app, cli, db
from app import create_app, db, cli
from app.models import User, Question, Option, File


app = create_app()
# Use some functions from app/cli.py
cli.register(app)

# For using the flask_shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Question': Question, 'Option': Option, 'File': File, 'UserQuestion': UserQuestion}
