import quart.flask_patch
from quart import Blueprint, redirect, render_template, request

from jeeves.auth import admin_required
from jeeves.database import User, db
from jeeves.forms import UserForm

admin = Blueprint("admin", __name__)


@admin.route("/users")
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@admin.route("/create_user", methods=["GET", "POST"])
@admin_required
def create_user():
    form = UserForm()
    if request.method == "POST":

        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/users")

    return render_template("create_user.html", form=form)
