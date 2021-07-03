# quart_etag.py
from datetime import datetime

from quart import Quart, Response, abort, jsonify, request

app = Quart(__name__)


def _time2etag():
    return datetime.now().isoformat()


_USERS = {"1": {"name": "Simon", "modified": _time2etag()}}


@app.route("/api/user/<user_id>")
async def get_user(user_id):
    if user_id not in _USERS:
        return abort(404)
    user = _USERS[user_id]

    # returning 304 if If-None-Match matches
    if user["modified"] in request.if_none_match:
        return Response("Not modified", status=304)

    resp = jsonify(user)

    # setting the ETag
    resp.set_etag(user["modified"])
    return resp


if __name__ == "__main__":
    app.run()
