# quart_details.py
from quart import Quart, request, jsonify

app = Quart(__name__)


@app.route("/api", provide_automatic_options=False)
async def my_microservice():
    print(dir(request))
    response = jsonify({"Hello": "World!"})
    print(response)
    print(await response.get_data())
    return response


if __name__ == "__main__":
    print(app.url_map)
    app.run()
