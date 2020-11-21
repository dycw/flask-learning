from __future__ import annotations

from flask import url_for

from flask_learning.official.quickstart.v005__url_building.hello import app


def test_hello() -> None:
    with app.test_request_context():
        assert url_for("index") == "/"
        assert url_for("login") == "/login"
        assert url_for("login", next="/") == "/login?next=%2F"
        assert url_for("profile", username="John Doe") == "/user/John%20Doe"
