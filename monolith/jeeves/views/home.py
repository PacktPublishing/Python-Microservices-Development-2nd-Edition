from quart import Blueprint, render_template

from jeeves.auth import current_user

home = Blueprint("home", __name__)


@home.route("/")
async def index():
    """Home view.

    This view will return an empty JSON mapping.
    """
    return await render_template("index.html", current_user=current_user)
