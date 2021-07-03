import quart.flask_patch

from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    slack_id = f.StringField("Slack ID")
    password = f.PasswordField("password")

    display = ["email", slack_id, "password"]
