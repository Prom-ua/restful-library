from datetime import datetime
from uuid import uuid4

from flask.ext.login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from restful_library import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(120),
        unique=True,
        index=True,
        nullable=False,
    )
    password = db.Column(db.String(64))

    def __init__(self, email=None, password=None):
        self.email = email
        if password is not None:
            self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return u'<User %r>' % (self.email)

    def __unicode__(self):
        return u'%s' % (self.email)


class ApiToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_expires = db.Column(db.DateTime)

    def __init__(self):
        self.uuid = str(uuid4())

    def __repr__(self):
        return '<ApiToken %r>' % (self.uuid)

    def __unicode__(self):
        return '%s' % (self.uuid)
