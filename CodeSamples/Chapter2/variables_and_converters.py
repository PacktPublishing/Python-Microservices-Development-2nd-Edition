from quart import Quart, request

app = Quart(__name__)


@app.route("/person/<person_id>")
def person_friendly(person_id):
    return f"Hello {person_id}"


@app.route("/person/<int:person_id>")
def person(person_id):
    return {"Hello": person_id}


@app.route("/decimals/<float:my_number>")
def decimal_example(my_number):
    return f"Hello {my_number}"


@app.route("/many/<some_text>/<other_text>/<int:my_number>")
def path_friendly(some_text, other_text, my_number):
    return (
        f"You sent {some_text} and also {other_text}, as well as a number: {my_number}"
    )


@app.route("/path/<path:some_path>")
def path_friendly(some_path):
    return f"Hello {some_path}"


@app.route("/<any(about, help, contact):page_name>")
def page_friendly(page_name):
    return f"Hello {page_name}"


app.run()
