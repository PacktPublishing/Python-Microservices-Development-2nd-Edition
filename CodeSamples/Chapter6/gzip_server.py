# gzip_server.py
# Receive data from gzip_example_post.py

from quart import Quart, request
import gzip

app = Quart(__name__)


@app.route("/api_post", methods=["POST"])
async def receive_gzip_data():
    if request.headers["Content-Encoding"] == "gzip":
        return gzip.decompress(await request.data)
    else:
        return await request.data


app.run()
