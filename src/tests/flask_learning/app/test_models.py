import datetime as dt
from typing import Iterator
from typing import cast

from pytest import fixture
from pytest import mark
from sqlalchemy.orm.session import Session

from flask_learning.app import app
from flask_learning.app import db
from flask_learning.app.models import Post
from flask_learning.app.models import User


@fixture
def session() -> Iterator[Session]:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    db.create_all()
    yield cast(Session, db.session)
    db.session.remove()
    db.drop_all()


class TestUser:
    def test_password_hashing(self) -> None:
        user = User(username="susan")
        user.set_password("cat")
        assert user.check_password("cat")
        assert not user.check_password("dog")

    def test_avatar(self) -> None:
        user = User(username="john", email="john@example.com")
        assert user.avatar(128) == (
            "https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6"
            "?d=identicon&s=128"
        )

    def test_follow(self, session: Session) -> None:
        user1 = User(username="john", email="john@example.com")
        user2 = User(username="susan", email="susan@example.com")
        session.add(user1)
        session.add(user2)
        session.commit()
        assert user1.followed.all() == []
        assert user1.followers.all() == []
        user1.follow(user2)
        session.commit()
        assert user1.is_following(user2)
        assert user1.followed.count() == 1
        assert user1.followed.first().username == "susan"
        assert user2.followers.count() == 1
        assert user2.followers.first().username == "john"
        user1.unfollow(user2)
        session.commit()
        assert not user1.is_following(user2)
        assert user1.followed.count() == 0
        assert user2.followers.count() == 0

    @mark.xfail(
        until=dt.date(2021, 4, 13),
        reason='says there is a syntax error with "union"',
    )
    def test_follow_posts(self, session: Session) -> None:
        # create four users
        user1 = User(username="john", email="john@example.com")
        user2 = User(username="susan", email="susan@example.com")
        user3 = User(username="mary", email="mary@example.com")
        user4 = User(username="david", email="david@example.com")
        session.add_all([user1, user2, user3, user4])

        # create four posts
        now = dt.datetime.utcnow()
        p1 = Post(
            body="post from john",
            author=user1,
            timestamp=now + dt.timedelta(seconds=1),
        )
        p2 = Post(
            body="post from susan",
            author=user2,
            timestamp=now + dt.timedelta(seconds=4),
        )
        p3 = Post(
            body="post from mary",
            author=user3,
            timestamp=now + dt.timedelta(seconds=3),
        )
        p4 = Post(
            body="post from david",
            author=user4,
            timestamp=now + dt.timedelta(seconds=2),
        )
        session.add_all([p1, p2, p3, p4])
        session.commit()

        # setup the followers
        user1.follow(user2)  # john follows susan
        user1.follow(user4)  # john follows david
        user2.follow(user3)  # susan follows mary
        user3.follow(user4)  # mary follows david
        session.commit()

        # check the followed posts of each user
        f1 = user1.followed_posts().all()
        f2 = user2.followed_posts().all()
        f3 = user3.followed_posts().all()
        f4 = user4.followed_posts().all()
        assert f1 == [p2, p4, p1]
        assert f2 == [p2, p3]
        assert f3 == [p3, p4]
        assert f4 == [p4]
