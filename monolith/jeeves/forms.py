import quart.flask_patch
import wtforms as f
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    display = ["email", "password"]


class UserForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    password = f.PasswordField("password")
    slack_id = f.StringField("Slack Username")
    admin = f.BooleanField("Admin?")

    display = ["email", "password", "slack_id", "admin"]
