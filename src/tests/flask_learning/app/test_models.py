from flask_learning.app.models import User


class TestUser:
    def test_password_hashing(self) -> None:
        user = User(username="susan")
        user.set_password("cat")
        assert user.check_password("cat")
        assert not user.check_password("dog")
