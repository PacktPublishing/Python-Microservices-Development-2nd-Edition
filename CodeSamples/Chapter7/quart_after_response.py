# quart_after_response.py
from quart import Quart, redirect
from quart.helpers import make_response
from urllib.parse import urlparse

app = Quart(__name__)


@app.route("/api")
async def my_microservice():
    return redirect("https://github.com:443/")


# domain:port
SAFE_DOMAINS = ["github.com:443", "google.com:443"]


@app.after_request
async def check_redirect(response):
    if response.status_code != 302:
        return response
    url = urlparse(response.location)
    netloc = url.netloc
    if netloc not in SAFE_DOMAINS:
        # not using abort() here or it'll break the hook
        return await make_response("Forbidden", 403)
    return response


if __name__ == "__main__":
    app.run(debug=True)
