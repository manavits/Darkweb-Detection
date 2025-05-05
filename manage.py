from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from flask.cli import with_appcontext
import click

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    from app.models import User, DarkWebThreat
    return dict(app=app, db=db, User=User, DarkWebThreat=DarkWebThreat)

@app.cli.command("create-admin")
@with_appcontext
def create_admin():
    import app.create_user
