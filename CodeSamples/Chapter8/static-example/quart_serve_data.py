# quart_serve_data.py
from quart import Quart, render_template, jsonify

app = Quart(__name__)


@app.route("/users")
async def show_users_page():
    return await render_template("person_example.html")


@app.route("/api/users")
async def serve_pretend_userdata():
    return jsonify([{"name": "Alice", "email": "alice@example.com"}])


if __name__ == "__main__":
    app.run()
