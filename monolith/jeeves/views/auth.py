import quart.flask_patch
from flask_login import current_user, login_required, login_user, logout_user
from quart import Blueprint, redirect, render_template, request

from jeeves.database import User, db
from jeeves.forms import LoginForm

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data["email"], form.data["password"]
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        if user is not None and user.authenticate(password):
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect("/")
