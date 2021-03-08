import datetime as dt
from typing import cast

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from flask_learning.app import db


DbColumn = cast(type[Column], db.Column)  # type: ignore
DbInteger = cast(type[Integer], db.Integer)  # type: ignore
DbString = cast(type[String], db.String)  # type: ignore


class User(db.Model):
    id = DbColumn(DbInteger, primary_key=True)
    username = DbColumn(DbString(64), index=True, unique=True)
    email = DbColumn(db.String(120), index=True, unique=True)
    password_hash = DbColumn(db.String(128))
    posts = db.relationship("Post", backref="author")

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Post(db.Model):
    id = DbColumn(db.Integer, primary_key=True)
    body = DbColumn(db.String(140))
    timestamp = DbColumn(db.DateTime, index=True, default=dt.datetime.utcnow)
    user_id = DbColumn(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"<Post {self.body}>"
