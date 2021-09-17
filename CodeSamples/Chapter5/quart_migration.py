# quart_metrics.py
import asyncio
from random import randint

from aioprometheus import Gauge, Registry, Summary, inprogress, render, timer, Counter
from quart import Quart, request
import random

app = Quart(__name__)
app.config["NEW_WORKER_PERCENTAGE"] = 90
app.registry = Registry()
app.api_requests_gauge = Gauge(
    "quart_active_requests", "Number of active requests per endpoint"
)
app.worker_usage = Counter("workers_used", "Number of active workers")
app.request_timer = Summary(
    "request_processing_seconds", "Time spent processing request"
)
app.registry.register(app.api_requests_gauge)
app.registry.register(app.worker_usage)
app.registry.register(app.request_timer)


# @inprogress(app.worker_usage, labels={"func": "original_worker"})
async def original_worker():
    app.worker_usage.inc({"func": "original_worker"})
    asyncio.sleep(2.0)
    return "data"


# @inprogress(app.worker_usage, labels={"func": "new_worker"})
async def new_worker():
    app.worker_usage.inc({"func": "new_worker"})
    asyncio.sleep(1.0)
    return "data"


@app.route("/migrating_gradually")
@timer(app.request_timer, labels={"path": "/migrating_gradually"})
@inprogress(app.api_requests_gauge, labels={"path": "/migrating_gradually"})
async def migrating_gradually_example():
    percentage_split = app.config.get("NEW_WORKER_PERCENTAGE")
    if percentage_split and random.randint(1, 100) <= percentage_split:
        return await new_worker()
    else:
        return await original_worker()


@app.route("/metrics")
async def handle_metrics():
    return render(app.registry, request.headers.getlist("accept"))


app.run(host="REPLACE WITH YOUR IP ADDRESS")
