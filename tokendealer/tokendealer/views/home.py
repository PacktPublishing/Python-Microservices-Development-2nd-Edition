import time
from hmac import compare_digest

import jwt
from quart import Blueprint, abort, current_app, request, jsonify
from werkzeug.exceptions import HTTPException

home = Blueprint("home", __name__)


_SECRETS = {"worker1": "f0fdeb1f1584fd5431c4250b2e859457"}


def _400(desc):
    exc = HTTPException()
    exc.code = 400
    exc.description = desc
    return error_handling(exc)


def error_handling(error):
    if isinstance(error, HTTPException):
        result = {
            "code": error.code,
            "description": error.description,
            "message": str(error),
        }
    else:
        description = abort.mapping[500].description
        result = {"code": 500, "description": description, "message": str(error)}

    resp = jsonify(result)
    resp.status_code = result["code"]
    return resp


@home.route("/.well-known/jwks.json")
async def _jwks():
    """Returns the public key in the Json Web Key (JWK) format"""
    with open(current_app.config["PUBLIC_KEY"]) as f:
        key = f.read()
    key = {
        "alg": "RS512",
        "e": "AQAB",
        "n": key,
        "kty": "RSA",
        "use": "sig",
    }

    return jsonify([key])


def is_authorized_app(client_id, client_secret):
    return compare_digest(_SECRETS.get(client_id), client_secret)


@home.route("/oauth/token", methods=["POST"])
async def create_token():
    with open(current_app.config["PRIVATE_KEY"]) as f:
        key = f.read()
    try:
        data = await request.form
        if data.get("grant_type") != "client_credentials":
            return _400(f"Wrong grant_type {data.get('grant_type')}")

        client_id = data.get("client_id")
        client_secret = data.get("client_secret")
        aud = data.get("audience", "")

        if not is_authorized_app(client_id, client_secret):
            return abort(401)

        now = int(time.time())

        token = {
            "iss": "https://tokendealer.example.com",
            "aud": aud,
            "iat": now,
            "exp": now + 3600 * 24,
        }
        token = jwt.encode(token, key, algorithm="RS512")
        return {"access_token": token}
    except Exception as e:
        return _400(str(e))


@home.route("/verify_token", methods=["POST"])
async def verify_token():
    with open(current_app.config["PUBLIC_KEY"]) as f:
        key = f.read()
    try:
        json_body = await request.form
        token = json_body["access_token"]
        audience = json_body.get("audience", "")
        print(token, audience)
        return jwt.decode(token, key, algorithms=["RS512"], audience=audience)
    except Exception as e:
        return _400(str(e))
