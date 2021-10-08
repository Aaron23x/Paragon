from Iconic import app
from flask import render_template, session, redirect, url_for, flash
from Iconic.forms import RegisterForm, LoginForm
from Iconic.models import User
from Iconic import db
from flask_login import login_user, logout_user, login_required
from Iconic import models


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/profile")
@login_required  # User has to be logged in to see the profile page
def profile():
    return render_template("profile.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(first_name=form.first_name.data, last_name=form.last_name.data,
                              username=form.username.data, email_address=form.email_address.data, password=form.password1.data)

        db.create_all()
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(
            f"Account Created Successfully! You are currently logged in as {user_to_create.username}", category="success")

        return redirect(url_for("profile"))

    if form.errors != {}:  # If there are no errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error creating a user: {err_msg}', category="danger")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(
                f"Success! You are currently logged in as: {attempted_user.username}", category="success")
            return redirect(url_for("profile"))
        else:
            flash(
                "Username and password are not a match! Please try again.", category="danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You've been logged out!", category="info")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
