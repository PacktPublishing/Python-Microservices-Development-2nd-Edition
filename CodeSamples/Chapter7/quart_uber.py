from quart import Quart, request, render_template_string

app = Quart(__name__)

SECRET = "oh no!"

_TEMPLATE = """
Hello %s 

Welcome to my API! 
"""


class Extra:
    def __init__(self, data):
        self.data = data


# @app.route('/<user_id>')
@app.route("/")
async def my_microservice():
    user_id = request.args.get("user_id", "Anonymous")
    tmpl = _TEMPLATE % user_id
    return await render_template_string(tmpl, extra=Extra("something"))


app.run()
