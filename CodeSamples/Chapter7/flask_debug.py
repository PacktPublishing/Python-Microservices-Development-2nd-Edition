# flask_debug.py for vulnerability checking.
# Uses unsafe setting for production
from flask import Flask

app = Flask(__name__)


@app.route("/api")
def my_microservice():
    return {"Hello": "World!"}


if __name__ == "__main__":
    app.run(debug=True)
