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
    for x in range(10):
        c = Company(name=f"Company {x}", kvk=x, address=f"Road {x}")
        db.session.add(c)
        db.session.commit()
        click.echo(f"{c.id} company created.")
