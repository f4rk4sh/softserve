from app import create_app, db, cli
from app.models import User, Interview, Set, Question, Grade

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Interview': Interview,
            'Set': Set, 'Question': Question, 'Grade': Grade}
