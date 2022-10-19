from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired


class NewInvoiceForm(FlaskForm):
    company = SelectField("Company", choices=[], validators=[DataRequired()])
    amount = StringField("Amount", validators=[DataRequired()])
    side = StringField("Side", validators=[DataRequired()])
    submit = SubmitField("Save")


class EditInvoiceForm(FlaskForm):
    company = SelectField("Company", choices=[], validators=[DataRequired()])
    amount = StringField("Amount", validators=[DataRequired()])
    side = StringField("Side", validators=[DataRequired()])
    created_at = StringField("Created", validators=[DataRequired()])
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
