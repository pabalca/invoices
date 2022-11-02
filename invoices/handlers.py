import click

from invoices import app
from invoices.models import Invoice, User, Company, db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Invoice=Invoice, User=User)


@app.cli.command()
@click.option("--drop", is_flag=True, help="Create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")


@app.cli.command()
@click.option("-p", "--pwd", prompt="Invoice", help="Create new user.")
def createuser(pwd):
    u = User(pwd)
    db.session.add(u)
    db.session.commit()
    click.echo(f"{u.id} user created.")


@app.cli.command()
def scrape():
    u = User(username="admin", avatar="logo.png", address="Metaverse", pwd="admin")
    db.session.add(u)
    for x in ["Pablo", "Leire", "Maria", "Antonio"]:
        c = Company(name=f"{x}", kvk=x, address=f"Amsterdam")
        db.session.add(c)
        click.echo(f"Company {x} created.")
    db.session.commit()
