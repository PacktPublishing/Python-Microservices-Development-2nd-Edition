from jeeves.views.admin import admin
from jeeves.views.auth import auth
from jeeves.views.home import home
from jeeves.views.slack_api import slack_api

blueprints = [home, auth, admin, slack_api]
