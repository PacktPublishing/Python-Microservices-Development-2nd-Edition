# etcd_basic.py
from quart import Quart, current_app
import etcd3


# Can read this map from a traditional config file
settings_map = {
    "dataservice_url": "/services/dataservice/url",
}
settings_reverse_map = {v: k for k, v in settings_map.items()}

etcd_client = etcd3.client()


def load_settings():
    config = dict()
    for setting, etcd_key in settings_map.items():
        config[setting] = etcd_client.get(etcd_key)[0].decode("utf-8")
    return config


def create_app(name=__name__):
    app = Quart(name)
    app.config.update(load_settings())
    return app


app = create_app()


def watch_callback(event):
    global app
    for update in event.events:
        # Determine which setting to update, and convert from bytes to str
        config_option = settings_reverse_map[update.key.decode("utf-8")]
        app.config[config_option] = update.value.decode("utf-8")


# Start to watch for dataservice url changes
# You can also watch entire areas with add_watch_prefix_callback
watch_id = etcd_client.add_watch_callback("/services/dataservice/url", watch_callback)


@app.route("/api")
def what_is_url():
    return {"url": app.config["dataservice_url"]}


app.run()
