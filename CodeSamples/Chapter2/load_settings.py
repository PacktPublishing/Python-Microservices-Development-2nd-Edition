# Load settings in an interactive Python environment.
# To start, run the python executable, and type the following as commands
# at the >>> prompt

from quart import Quart
import pprint

pp = pprint.PrettyPrinter(indent=4)
app = Quart(__name__)
app.config.from_object("prod_settings.Config")
pp.pprint(app.config)


app.config.from_json("prod_settings.json")


import yaml

app.config.from_file("settings.yml", yaml.safe_load)
