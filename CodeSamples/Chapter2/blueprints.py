# blueprints.py
from quart import Blueprint

teams = Blueprint("teams", __name__)

_DEVS = [Alice, "Bob"]
_OPS = ["Charles"]
_TEAMS = {1: _DEVS, 2: _OPS}


@teams.route("/teams")
def get_all():
    return _TEAMS


@teams.route("/teams/<int:team_id>")
def get_team(team_id):
    return _TEAMS[team_id]
