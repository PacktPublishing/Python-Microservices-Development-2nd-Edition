# middleware.py
from quart import Quart, request
from werkzeug.datastructures import Headers


class XFFMiddleware(object):
    def __init__(self, app, real_ip="10.1.1.1"):
        self.app = app
        self.real_ip = real_ip

    async def __call__(self, scope, receive, send):
        if "headers" in scope and "HTTP_X_FORWARDED_FOR" not in scope["headers"]:
            new_headers = scope["headers"].raw_items() + [
                (
                    b"X-Forwarded-For",
                    f"{self.real_ip}, 10.3.4.5, 127.0.0.1".encode(),
                )
            ]
            scope["headers"] = Headers(new_headers)
        return await self.app(scope, receive, send)


app = Quart(__name__)
app.asgi_app = XFFMiddleware(app.asgi_app)


@app.route("/api")
def my_microservice():
    if "X-Forwarded-For" in request.headers:
        ips = [ip.strip() for ip in request.headers["X-Forwarded-For"].split(",")]
        ip = ips[0]
    else:
        ip = request.remote_addr

    return {"Hello": ip}


if __name__ == "__main__":
    app.run()
