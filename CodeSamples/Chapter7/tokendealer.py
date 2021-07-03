import time
from hmac import compare_digest

import jwt
from quart import Quart, abort, current_app, request, jsonify
from werkzeug.exceptions import HTTPException

app = Quart(__name__)

app.config["TOKENDEALER_URL"] = "https://tokendealer.example.com"

_SECRETS = {"worker1": "f0fdeb1f1584fd5431c4250b2e859457"}


def bad_request(desc):
    exc = HTTPException()
    exc.code = 400
    exc.description = desc
    return error_handling(exc)


def error_handling(error):
    error_result = {
        "code": error.code,
        "description": error.description,
        "message": str(error),
    }
    resp = jsonify(error_result)
    resp.status_code = error_result["code"]
    return resp


@app.route("/.well-known/jwks.json")
async def _jwks():
    """Returns the public key in the Json Web Key Set (JWKS) format"""
    with open(current_app.config["PUBLIC_KEY_PATH"]) as f:
        key = f.read().strip()
    data = {
        "alg": "RS512",
        "e": "AQAB",
        "n": key,
        "kty": "RSA",
        "use": "sig",
    }

    return jsonify({"keys": [data]})


def is_authorized_app(client_id, client_secret):
    return compare_digest(_SECRETS.get(client_id), client_secret)


@app.route("/oauth/token", methods=["POST"])
async def create_token():
    with open(current_app.config["PRIVATE_KEY_PATH"]) as f:
        key = f.read().strip()
    try:
        data = await request.form
        if data.get("grant_type") != "client_credentials":
            return bad_request(f"Wrong grant_type {data.get('grant_type')}")

        client_id = data.get("client_id")
        client_secret = data.get("client_secret")
        aud = data.get("audience", "")

        if not is_authorized_app(client_id, client_secret):
            return abort(401)

        now = int(time.time())

        token = {
            "iss": current_app.config["TOKENDEALER_URL"],
            "aud": aud,
            "iat": now,
            "exp": now + 3600 * 24,
        }
        token = jwt.encode(token, key, algorithm="RS512")
        return {"access_token": token}
    except Exception as e:
        return bad_request("Unable to create a token")


@app.route("/verify_token", methods=["POST"])
async def verify_token():
    with open(current_app.config["PUBLIC_KEY_PATH"]) as f:
        key = f.read()
    try:
        input_data = await request.form
        token = input_data["access_token"]
        audience = input_data.get("audience", "")
        print(token, audience)
        return jwt.decode(token, key, algorithms=["RS512"], audience=audience)
    except Exception as e:
        return bad_request("Unable to verify the token")
