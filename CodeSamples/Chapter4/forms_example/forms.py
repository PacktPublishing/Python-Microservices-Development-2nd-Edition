import quart.flask_patch
import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    email = wtforms.StringField("email", validators=[DataRequired()])
    slack_id = wtforms.StringField("Slack ID")
    name = wtforms.StringField("Name")

    display = ["email", "slack_id", "name"]
