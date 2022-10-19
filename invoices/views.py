from flask import abort, flash, redirect, render_template, session, url_for
from sqlalchemy import or_

from invoices import app
from invoices.decorators import login_required
from invoices.forms import (
    DeleteInvoiceForm,
    DeleteCompanyForm,
    EditInvoiceForm,
    LoginForm,
    NewInvoiceForm,
    NewCompanyForm,
    SearchForm,
    RegisterForm,
)
from invoices.models import Invoice, User, Company, db


@app.route("/login/", methods=["GET", "POST"])
def login():
    session["logged_in"] = False
    form = LoginForm()
    if form.validate_on_submit():
        challenge = form.challenge.data
        users = User.query.all()
        for user in users:
            if user.verify_invoice(challenge):
                session["logged_in"] = True
                session["user"] = user.id
                return redirect(url_for("index"))
    return render_template("login.html", form=form, session=session)


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    invoices = Invoice.query.filter(Invoice.user == session.get("user")).order_by(
        Invoice.created_at.desc()
    )
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search.data
        invoices = invoices.filter(
            or_(
                Invoice.amount.contains(search),
            )
        )
    invoices = invoices.all()
    return render_template("index.html", invoices=invoices, form=form)


@app.route("/new", methods=["GET", "POST"])
@login_required
def new_invoice():
    form = NewInvoiceForm()
    companies = [
        (company.id, company.name)
        for company in Company.query.order_by(Company.name.asc()).all()
    ]
    form.company.choices = companies
    if form.validate_on_submit():
        user = session.get("user")
        company_id = form.company.data
        amount = form.amount.data
        side = form.side.data
        i = Invoice(user=user, company_id=company_id, amount=amount, side=side)
        db.session.add(i)
        db.session.commit()
        flash("Your invoice is saved.")
        return redirect(url_for("index"))
    return render_template("new_invoice.html", form=form)


@app.route("/edit/<invoice_id>", methods=["GET", "POST"])
@login_required
def edit_invoice(invoice_id):
    form = EditInvoiceForm()
    companies = [
        (company.id, f"{company.name} : {company.kvk}")
        for company in Company.query.order_by(Company.name.asc()).all()
    ]
    invoice = Invoice.query.get(invoice_id)
    if form.validate_on_submit():
        invoice.company = form.company.data
        invoice.amount = form.amount.data
        invoice.side = form.side.data
        db.session.commit()
        flash("Your invoice is updated.")
        return redirect(url_for("index"))

    form.company.choices = companies
    # form.company.data = invoice.company  # preset form input's value
    form.amount.data = invoice.amount
    form.side.data = invoice.side
    form.created_at.data = invoice.created_at
    return render_template("edit_invoice.html", form=form)


@app.route("/delete/<invoice_id>", methods=["POST"])
@login_required
def delete_invoice(invoice_id):
    form = DeleteInvoiceForm()
    if form.validate_on_submit():
        invoice = Invoice.query.get(invoice_id)
        db.session.delete(invoice)
        db.session.commit()
        flash(f"Your invoice <{invoice_id}> is deleted.")
    else:
        abort(400)
    return redirect(url_for("index"))


@app.route("/companies", methods=["GET"])
@login_required
def companies():
    companies = (
        Company.query.filter(Company.name is not None)
        .order_by(Company.name.asc())
        .all()
    )
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search.data
        invoices = companies.filter(
            or_(
                Company.name.contains(search),
            )
        )
    return render_template("companies.html", companies=companies, form=form)


@app.route("/company/new", methods=["GET", "POST"])
@login_required
def new_company():
    form = NewCompanyForm()
    if form.validate_on_submit():
        name = form.name.data
        kvk = form.kvk.data
        address = form.address.data
        c = Company(name=name, kvk=kvk, address=address)
        db.session.add(c)
        db.session.commit()
        flash("Your company is saved.")
        return redirect(url_for("companies"))
    return render_template("new_company.html", form=form)


@app.route("/company/delete/<company_id>", methods=["GET", "POST"])
@login_required
def delete_company(company_id):
    form = DeleteCompanyForm()
    company = Company.query.filter(Company.id == company_id).first()
    if form.validate_on_submit():
        company = Company.query.get(company_id)
        db.session.delete(company)
        db.session.commit()
        flash(f"Your company <{company_id}> is deleted.")
        return redirect(url_for("companies"))
    return render_template("delete_company.html", form=form, company=company)


@app.route("/export/<invoice_id>", methods=["GET", "POST"])
@login_required
def export_invoice(invoice_id):
    invoice = Invoice.query.filter(Invoice.id == invoice_id).first()
    if not invoice:
        flash(f"Not found.")
        return redirect(url_for("index"))
    return render_template("export_invoice.html", invoice=invoice)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        avatar = form.avatar.data
        address = form.address.data
        password = form.password.data
        u = User(username=username, avatar=avatar, address=address, pwd=password)
        db.session.add(u)
        db.session.commit()
        flash(f"Your user <{username} is saved.")        
        return redirect(url_for("register"))
    return render_template("register.html", form=form)

