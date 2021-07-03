import os
from authservice.views import blueprints
from quart import Quart
import asyncio

_HERE = os.path.dirname(__file__)
SETTINGS = os.path.join(_HERE, "settings.py")


async def create_app(name=__name__, blueprints=None, settings=None):
    app = Quart(name)

    # load configuration
    settings = os.environ.get("QUART_SETTINGS", settings)
    if settings is not None:
        app.config.from_pyfile(settings)

    # register blueprints
    if blueprints is not None:
        for bp in blueprints:
            app.register_blueprint(bp)

    return app


app = None

loop = asyncio.get_event_loop()
app = loop.run_until_complete(create_app(blueprints=blueprints, settings=SETTINGS))
