from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired


class NewInvoiceForm(FlaskForm):
    company = SelectField("Company", choices=[], validators=[DataRequired()])
    amount = StringField("Amount", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Save")


class EditInvoiceForm(FlaskForm):
    amount = StringField("Amount", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Save")


class DeleteInvoiceForm(FlaskForm):
    submit = SubmitField("Delete")


class SearchForm(FlaskForm):
    search = StringField("Search")
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    challenge = PasswordField("Challenge")
    submit = SubmitField("Submit")


class NewCompanyForm(FlaskForm):
    name = StringField("Company name", validators=[DataRequired()])
    kvk = IntegerField("KVK number", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Save")

class DeleteCompanyForm(FlaskForm):
    submit = SubmitField("Yes, delete")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    avatar = StringField("Avatar", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Save")
