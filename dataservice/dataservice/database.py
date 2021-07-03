# encoding: utf8
from dataclasses import dataclass
import quart.flask_patch
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

from sqlalchemy.inspection import inspect


class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


@dataclass
class User(db.Model, Serializer):
    __tablename__ = "user"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.Unicode(128))
    email: str = db.Column(db.Unicode(128))
    slack_id: str = db.Column(db.Unicode(128))
    email_address: str = db.Column(db.String(128))
    password: str = db.Column(db.Unicode(128))
    strava_tokens: str = db.Column(db.String(128))
    location: str = db.Column(db.String(128))
    config: dict = db.Column(db.JSON)
    location: str = db.Column(db.String(128))
    is_active: bool = db.Column(db.Boolean, default=True)
    is_admin: bool = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id
