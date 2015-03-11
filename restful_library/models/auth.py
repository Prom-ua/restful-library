from datetime import datetime, timedelta
from uuid import uuid4

from flask.ext.login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from restful_library import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(
        db.String(120),
        unique=True,
        index=True,
        nullable=False,
    )
    password = db.Column(db.String(80))

    def __init__(self, email=None, password=None):
        self.email = email
        if password is not None:
            self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % (self.email)

    def __str__(self):
        return self.email


class ApiToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_expiry = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now() + timedelta(30),
    )

    def __init__(self):
        self.uuid = uuid4()

    def is_not_expired(self):
        return self.date_expiry > datetime.now()

    def __repr__(self):
        return '<ApiToken %r>' % (self.uuid)

    def __str__(self):
        return self.uuid
