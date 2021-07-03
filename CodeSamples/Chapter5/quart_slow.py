# quart_metrics.py
import asyncio
from random import randint

from aioprometheus import Gauge, Registry, Summary, inprogress, render, timer
from quart import Quart, request

app = Quart(__name__)
app.registry = Registry()
app.api_requests_gauge = Gauge(
    "quart_active_requests", "Number of active requests per endpoint"
)
app.request_timer = Summary(
    "request_processing_seconds", "Time spent processing request"
)
app.registry.register(app.api_requests_gauge)
app.registry.register(app.request_timer)


@app.route("/")
@timer(app.request_timer, labels={"path": "/"})
@inprogress(app.api_requests_gauge, labels={"path": "/"})
async def index_handler():
    await asyncio.sleep(1.0)
    return "index"


@app.route("/endpoint1")
@timer(app.request_timer, labels={"path": "/endpoint1"})
@inprogress(app.api_requests_gauge, labels={"path": "/endpoint1"})
async def endpoint1_handler():
    await asyncio.sleep(randint(1000, 1500) / 1000.0)
    return "endpoint1"


@app.route("/endpoint2")
@timer(app.request_timer, labels={"path": "/endpoint2"})
@inprogress(app.api_requests_gauge, labels={"path": "/endpoint2"})
async def endpoint2_handler():
    await asyncio.sleep(randint(2000, 2500) / 1000.0)
    return "endpoint2"


@app.route("/metrics")
async def handle_metrics():
    return render(app.registry, request.headers.getlist("accept"))


app.run(host="192.168.1.100")
