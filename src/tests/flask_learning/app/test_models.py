from flask_learning.app.models import User


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
