from quart import Quart, current_app

app = Quart(__name__)
app.config.from_json("prod_settings.json")


def original_worker():
    """Do some work, as an example."""
    pass


def new_worker():
    """Do some work, as an example."""
    pass


@app.route("/migrating_endpoint")
async def migration_example():
    if current_app.config.get("USE_NEW_WORKER") is True:
        new_worker()
    else:
        original_worker()


app.run()
