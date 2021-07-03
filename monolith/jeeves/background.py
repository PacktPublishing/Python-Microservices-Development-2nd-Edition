import asyncio

from asgiref.sync import async_to_sync
from celery import Celery

from jeeves.actions.weather import fetch_weather
from jeeves.app import SETTINGS, blueprints, create_app
from jeeves.database import User, db
from jeeves.outgoing.slack import post_to_slack

celery_app = Celery("tasks", backend="rpc://", broker="amqp://localhost")

loop = asyncio.get_event_loop()
quart_app = loop.run_until_complete(
    create_app(blueprints=blueprints, settings=SETTINGS)
)
quart_app.app_context().push()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, do_weather_alerts, name="add every 10", expires=30)


async def weather_alerts_async():
    async with quart_app.app_context():
        q = (
            db.session.query(User)
            .filter(User.location.isnot(None))
            .filter(User.slack_id.isnot(None))
        )
        for user in q:
            weather_message = await fetch_weather(user.location)
            username = user.slack_id
            if not username.startswith("@"):
                username = "@" + username
            post_to_slack(weather_message, {"channel": username})


@celery_app.task
def do_weather_alerts():
    async_to_sync(weather_alerts_async)()
