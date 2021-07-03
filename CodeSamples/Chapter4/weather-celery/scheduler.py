# weather_worker.py
import asyncio

from asgiref.sync import async_to_sync
from celery import Celery
from weather_worker import do_weather_alerts

celery_app = Celery("tasks", broker="amqp://localhost")


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, do_weather_alerts, name="add every 10", expires=30)
