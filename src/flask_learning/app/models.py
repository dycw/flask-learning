import datetime as dt
from hashlib import md5
from typing import cast

from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative.api import Table
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flask_learning.app import db
from flask_learning.app import login


DbModel = cast(type[Table], db.Model)  # type: ignore
DbColumn = cast(type[Column], db.Column)  # type: ignore
DbDateTime = cast(type[DateTime], db.DateTime)  # type: ignore
DbInteger = cast(type[Integer], db.Integer)  # type: ignore
DbString = cast(type[String], db.String)  # type: ignore
DbForeignKey = cast(type[ForeignKey], db.ForeignKey)  # type: ignore
DbRelationship = cast(type[relationship], db.relationship)  # type: ignore


class User(UserMixin, DbModel):
    id = DbColumn(DbInteger, primary_key=True)
    username = DbColumn(DbString(64), index=True, unique=True)
    email = DbColumn(DbString(120), index=True, unique=True)
    password_hash = DbColumn(DbString(128))
    posts = DbRelationship("Post", backref="author")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def avatar(self, size: int) -> str:
        digest = md5(  # noqa: S303
            self.email.lower().encode("utf-8")
        ).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size
        )


@login.user_loader
def load_user(id: str) -> "User":  # noqa: A002
    return User.query.get(int(id))


class Post(DbModel):
    id = DbColumn(DbInteger, primary_key=True)
    body = DbColumn(DbString(140))
    timestamp = DbColumn(DbDateTime, index=True, default=dt.datetime.utcnow)
    user_id = DbColumn(DbInteger, DbForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"<Post {self.body}>"
