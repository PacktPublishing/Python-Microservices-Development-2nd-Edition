# converter_custom.py
from quart import Quart, request
from werkzeug.routing import BaseConverter, ValidationError

_USERS = {"1": "Alice", "2": "Bob"}
_IDS = {val: id for id, val in _USERS.items()}


class RegisteredUser(BaseConverter):
    def to_python(self, value):
        if value in _USERS:
            return _USERS[value]
        raise ValidationError()

    def to_url(self, value):
        return _IDS[value]


app = Quart(__name__)
app.url_map.converters["registered"] = RegisteredUser


@app.route("/api/person/<registered:name>")
def person(name):
    response = {"Hello": name}
    return response


if __name__ == "__main__":
    app.run()
