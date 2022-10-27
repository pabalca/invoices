from flask import abort, flash, redirect, render_template, session, url_for, request
from sqlalchemy import or_

from ruler import app
from ruler.decorators import login_required
from ruler.models import User, Rule, AutoTrader, db
from ruler.forms import RuleForm, AutoTraderForm, SearchForm
import json


@app.route("/login/", methods=["GET", "POST"])
def login():
    session["logged_in"] = False
    form = LoginForm()
    if form.validate_on_submit():
        challenge = form.challenge.data
        users = User.query.all()
        for user in users:
            if user.verify_password(challenge):
                session["logged_in"] = True
                session["user"] = user.id
                return redirect(url_for("index"))
    return render_template("login.html", form=form, session=session)


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    rules = Rule.query.order_by(Rule.created_at.desc())
    if form.validate_on_submit():
        search = form.search.data
        rules = rules.filter(or_(Rule.ticker.contains(search)))
    rules = rules.all()
    return render_template("index.html", form=form, rules=rules)


@app.route("/rule", methods=["GET", "POST"])
def rule():
    form = RuleForm()
    autotraders = AutoTrader.query.all()
    if form.validate_on_submit():
        user = session.get("user")
        token = session.get("token")
        ticker = form.ticker.data
        action = form.action.data
        price = form.price.data
        token = form.token.data

        whitelist = [a.id for a in AutoTrader.query.all()]
        if token not in whitelist:
            flash("Not a valid token")
            return render_template("rule.html", form=form)

        r = Rule(ticker=ticker, action=action, price=price)
        db.session.add(r)
        db.session.commit()
        flash(f"Your rule <{r.id}> is saved.")
        return redirect(url_for("index"))
    return render_template("rule.html", form=form)


@app.route("/clear/<rule_id>", methods=["GET", "POST"])
def clear(rule_id):
    r = Rule.query.get(rule_id)
    db.session.delete(r)
    db.session.commit()
    flash(f"Your rule <{rule_id}> is deleted.")
    return redirect(url_for("index"))


@app.route("/autotrader", methods=["GET", "POST"])
def autotrader():
    form = AutoTraderForm()
    autotraders = AutoTrader.query.order_by(AutoTrader.created_at.desc())
    if form.validate_on_submit():
        name = form.name.data
        a = AutoTrader(name=name)
        db.session.add(a)
        db.session.commit()
        flash(f"Your autotrader <{a.id}> is saved.")
        return redirect(url_for("autotrader"))
    return render_template("autotrader.html", form=form, autotraders=autotraders)
