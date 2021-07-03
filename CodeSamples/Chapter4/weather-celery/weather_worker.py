# weather_worker.py
import asyncio

from asgiref.sync import async_to_sync
from celery import Celery
from database import user_dal

celery_app = Celery("tasks", broker="amqp://localhost")


async def fetch_weather(location):
    return "This is where we would call the weather service"


async def post_to_slack(message, options):
    print(f"This is where we would post {message}")


async def weather_alerts_async():
    async with user_dal() as ud:
        query_results = await ud.get_users_with_locations()
        for user in query_results:
            user = user[0]  # the database returns a tuple
            weather_message = await fetch_weather(user.location)
            username = user.slack_id
            if not username.startswith("@"):
                username = "@" + username
            await post_to_slack(weather_message, {"channel": username})


@celery_app.task
def do_weather_alerts():
    async_to_sync(weather_alerts_async)()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10.0, do_weather_alerts, name="fetch the weather", expires=30
    )
