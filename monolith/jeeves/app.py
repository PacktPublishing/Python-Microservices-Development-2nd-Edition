import asyncio
import os

from quart import Quart

from jeeves.auth import login_manager
from jeeves.database import User, db
from jeeves.views import blueprints

_HERE = os.path.dirname(__file__)

SETTINGS = os.path.join(_HERE, "settings.py")


async def create_app(name=__name__, blueprints=None, settings=None):
    app = Quart(name)
    # TODO instance_relative_config=True

    # load configuration
    settings = os.environ.get("QUARTSETTINGS", settings)
    if settings is not None:
        app.config.from_pyfile(settings)

    app.config["WTF_CSRF_SECRET_KEY"] = "A SECRET KEY"
    app.config["SECRET_KEY"] = "ANOTHER ONE"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/jeeves"

    # register blueprints
    if blueprints is not None:
        for bp in blueprints:
            app.register_blueprint(bp)

    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)

    # create a user
    async with app.app_context():
        q = db.session.query(User).filter(User.email == "simon@flmx.org")
        user = q.first()
        if user is None:
            simon = User()
            simon.email = "simon@flmx.org"
            simon.slack_id = "U136F44A0"
            simon.is_admin = True
            simon.set_password("ok")
            simon.location = "London, UK"
            db.session.add(simon)
            db.session.commit()
    return app


app = None

loop = asyncio.get_event_loop()
app = loop.run_until_complete(create_app(blueprints=blueprints, settings=SETTINGS))
