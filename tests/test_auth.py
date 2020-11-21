from __future__ import annotations

from flask import Flask
from flask.testing import FlaskClient
from pytest import mark

from flaskr.db import get_db


def test_register(client: FlaskClient, app: Flask) -> None:
    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register",
        data={"username": "a", "password": "a"},
    )
    assert "http://localhost/auth/login" == response.headers["Location"]

    with app.app_context():
        assert (
            get_db()
            .execute(
                "select * from user where username = 'a'",
            )
            .fetchone()
            is not None
        )


@mark.parametrize(  # type: ignore
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("a", "", b"Password is required."),
        ("test", "test", b"already registered"),
    ),
)
def test_register_validate_input(
    client: FlaskClient,
    username: str,
    password: str,
    message: bytes,
) -> None:
    response = client.post(
        "/auth/register",
        data={"username": username, "password": password},
    )
    assert message in response.data
