from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired


class RuleForm(FlaskForm):
    ticker = StringField("Ticker", validators=[DataRequired()])
    action = StringField("Action", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    token = StringField("Token", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AutoTraderForm(FlaskForm):
    name = StringField("Autotrader", validators=[DataRequired()])
    submit = SubmitField("Create")


class SearchForm(FlaskForm):
    search = StringField("Search")
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    challenge = PasswordField("Challenge")
    submit = SubmitField("Submit")
