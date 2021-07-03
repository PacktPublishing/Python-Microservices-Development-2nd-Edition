# catch_all_errors.py
from quart import Quart, jsonify, abort
from quart.exceptions import HTTPException, default_exceptions


def JsonApp(app):
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

    for code in default_exceptions.keys():
        app.register_error_handler(code, error_handling)

    return app


app = JsonApp(Quart(__name__))


@app.route("/api")
def my_microservice():
    raise TypeError("Some Exception")


if __name__ == "__main__":
    app.run()
