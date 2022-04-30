from app import cli, create_app, db
from app.models import Grade, Interview, Question, Set, User

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Interview": Interview,
        "Set": Set,
        "Question": Question,
        "Grade": Grade,
    }
