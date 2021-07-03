# authorization.py
from quart import Quart, request

app = Quart(__name__)


@app.route("/")
def auth():
    print("Flask's Authorization information")
    print(request.authorization)
    return ""


if __name__ == "__main__":
    app.run()
