import os
from myservice.views import blueprints
from quart import Quart

_HERE = os.path.dirname(__file__)
_SETTINGS = os.path.join(_HERE, "settings.ini")


def create_app(name=__name__, blueprints=None, settings=None):
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


app = create_app(blueprints=blueprints, settings=_SETTINGS)
