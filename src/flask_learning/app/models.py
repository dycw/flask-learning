import datetime as dt
from typing import cast

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative.api import Table
from sqlalchemy.orm import relationship

from flask_learning.app import db


DbModel = cast(type[Table], db.Model)  # type: ignore
DbColumn = cast(type[Column], db.Column)  # type: ignore
DbDateTime = cast(type[DateTime], db.DateTime)  # type: ignore
DbInteger = cast(type[Integer], db.Integer)  # type: ignore
DbString = cast(type[String], db.String)  # type: ignore
DbForeignKey = cast(type[ForeignKey], db.ForeignKey)  # type: ignore
DbRelationship = cast(type[relationship], db.relationship)  # type: ignore


class User(DbModel):
    id = DbColumn(DbInteger, primary_key=True)
    username = DbColumn(DbString(64), index=True, unique=True)
    email = DbColumn(DbString(120), index=True, unique=True)
    password_hash = DbColumn(DbString(128))
    posts = DbRelationship("Post", backref="author")

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Post(DbModel):
    id = DbColumn(DbInteger, primary_key=True)
    body = DbColumn(DbString(140))
    timestamp = DbColumn(DbDateTime, index=True, default=dt.datetime.utcnow)
    user_id = DbColumn(DbInteger, DbForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"<Post {self.body}>"
