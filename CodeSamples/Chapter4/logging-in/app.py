# logging-in.py
import os
from quart import Quart, request, render_template, redirect, url_for
from quart_auth import (
    AuthManager,
    login_required,
    logout_user,
    login_user,
    AuthUser,
    Unauthorized,
)
import aiohttp
import secrets

app = Quart(__name__)
AuthManager(app)
app.secret_key = secrets.token_urlsafe(16)


@app.route("/")
@login_required
async def welcome_page():
    return await render_template("welcome.html")


@app.route("/slack_login")
async def slack_login():
    client_id = os.environ["SLACK_CLIENT_ID"]
    return await render_template("login.html", client_id=client_id)


@app.route("/logout")
async def logout():
    logout_user()


@app.errorhandler(Unauthorized)
async def redirect_to_login(_):
    return redirect(url_for("slack_login"))


@app.route("/slack/callback")
async def oauth2_slack_callback():
    code = request.args["code"]
    client_id = os.environ["SLACK_CLIENT_ID"]
    client_secret = os.environ["SLACK_CLIENT_SECRET"]
    access_url = f"https://slack.com/api/oauth.v2.access?client_id={client_id}&client_secret={client_secret}&code={code}"
    async with aiohttp.ClientSession() as session:
        async with session.get(access_url) as resp:
            access_data = await resp.json()
            if access_data["ok"] is True:
                authed_user = access_data["authed_user"]["id"]
                login_user(AuthUser(authed_user))
                return redirect(url_for("welcome_page"))
    return redirect(url_for("slack_login"))


if __name__ == "__main__":
    app.run()
