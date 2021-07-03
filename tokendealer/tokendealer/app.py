import os

from quart import Quart

from pathlib import Path
import yaml


from tokendealer.views import blueprints

_HERE = Path(__file__).parent
_SETTINGS = _HERE / "settings.yml"


def create_app(name=__name__, blueprints=None, settings=None):
    app = Quart(name)

    # load configuration
    settings = os.environ.get("QUART_SETTINGS", settings)
    if settings is not None:
        app.config.from_file(settings, yaml.safe_load)
        # app.config.from_pyfile(settings)

    # register blueprints
    if blueprints is not None:
        for bp in blueprints:
            app.register_blueprint(bp)

    return app


app = create_app(blueprints=blueprints, settings=_SETTINGS)
