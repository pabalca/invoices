import click

from ruler import app
from ruler.models import User, Rule, db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Rule=Rule, User=User)


@app.cli.command()
@click.option("--drop", is_flag=True, help="Create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")

    u = User(username="admin", pwd="admin")
    db.session.add(u)
    db.session.commit()
    click.echo("Admin user created.")


@app.cli.command()
@click.option("-p", "--pwd", prompt="Rule", help="Create new user.")
def createuser(pwd):
    u = User(pwd)
    db.session.add(u)
    db.session.commit()
    click.echo(f"{u.id} user created.")

