import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    pwd_hash = db.Column(db.String)

    def __init__(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    def __repr__(self):
        return f"<User> {self.id}"

    def verify_invoice(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)


class Company(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String)
    kvk = db.Column(db.Integer)
    address = db.Column(db.String)

    def __repr__(self):
        return f"<Company> {self.name} {self.kvk}"


class Invoice(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    company_id = db.Column(db.String, db.ForeignKey(Company.id))
    company = db.relationship(Company, backref='companies')
    amount = db.Column(db.Integer)
    side = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<Invoice {self.company}:{self.side}:{self.amount}>"
