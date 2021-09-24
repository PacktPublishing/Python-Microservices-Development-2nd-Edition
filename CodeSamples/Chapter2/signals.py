# signals.py
from quart import Quart, request_finished
from quart.signals import signals_available

if not signals_available:
    raise RuntimeError("pip install blinker")

app = Quart(__name__)


def finished(sender, response, **extra):
    print("About to send a Response")
    print(response)


request_finished.connect(finished)


@app.route("/api")
def my_microservice():
    return {"Hello": "World"}


if __name__ == "__main__":
    app.run()
