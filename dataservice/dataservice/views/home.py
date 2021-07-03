from quart import Blueprint, jsonify, render_template

from dataservice.database import User, db

home = Blueprint("home", __name__)


@home.route("/")
async def index():
    """Home view.

    This view will return an empty JSON mapping.
    """
    return {}


@home.route("/api/users")
async def list_all_users():
    users = User.query.all()
    users_list = [u.serialize() for u in users]
    return jsonify(users_list)


@home.route("/api/users/<user_id>", methods=["GET", "POST"])
async def fetch_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    return user.serialize()


@home.route("/views/user")
async def show_user_form():
    return await render_template("index.html")


@home.route("/views/all_people")
async def show_all_people():
    return await render_template("all_people.html")


@home.route("/views/user_snippet")
async def show_user_snippet():
    return await render_template("user_snippet.html")


# Create user

# Fetch / update user

# Fetch myself


# Authentication service
# - get passed a service url, return a micro-UI element for logging in if not already authenticated?
# - Return who's logged in with that token
#
# Refer to:
# Database service
# - Get user details
# - Present edit form. Should this be a microfrontend too? Why not.
