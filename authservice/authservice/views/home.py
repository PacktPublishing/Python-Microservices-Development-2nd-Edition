from quart import Blueprint, jsonify, render_template


home = Blueprint("home", __name__)


@home.route("/")
async def index():
    """Home view.

    This view will return an empty JSON mapping.
    """
    return await render_template("index.html")
