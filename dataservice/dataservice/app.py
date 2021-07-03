import os
from dataservice.views import blueprints
from dataservice.database import User, db
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

    db.init_app(app)
    # login_manager.init_app(app)
    db.create_all(app=app)
    # create a user
    async with app.app_context():
        q = db.session.query(User).filter(User.email == "simon@flmx.org")
        user = q.first()
        if user is None:
            entry = User()
            entry.name = "Simon"
            entry.email = "simon@flmx.org"
            entry.slack_id = "U136F44A0"
            entry.is_admin = True
            entry.set_password("ok")
            entry.location = "London, UK"
            db.session.add(entry)
            db.session.commit()
            entry = User()
            entry.name = "Tarek"
            entry.email = "tarek@example.com"
            entry.is_admin = True
            entry.set_password("ok")
            entry.location = "France"
            db.session.add(entry)
            db.session.commit()
            entry = User()
            entry.name = "Alice"
            entry.email = "alice@example.com"
            entry.is_admin = False
            entry.set_password("ok")
            entry.location = "London, UK"
            db.session.add(entry)
            db.session.commit()
            entry = User()
            entry.name = "Bob"
            entry.email = "bob@aol.com"
            entry.is_admin = False
            entry.set_password("ok")
            entry.location = "London, UK"
            db.session.add(entry)
            db.session.commit()

    return app


app = None

loop = asyncio.get_event_loop()
app = loop.run_until_complete(create_app(blueprints=blueprints, settings=SETTINGS))
