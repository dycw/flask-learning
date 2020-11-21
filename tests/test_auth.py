from __future__ import annotations

from flask import Flask
from flask import g
from flask import session
from flask.testing import FlaskClient
from pytest import mark

from flaskr.db import get_db
from tests.conftest import AuthActions


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


def test_login(client: FlaskClient, auth: AuthActions) -> None:
    assert client.get("/auth/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"


@mark.parametrize(  # type: ignore
    ("username", "password", "message"),
    (
        ("a", "test", b"Incorrect username."),
        ("test", "a", b"Incorrect password."),
    ),
)
def test_login_validate_input(
    auth: AuthActions,
    username: str,
    password: str,
    message: bytes,
) -> None:
    response = auth.login(username, password)
    assert message in response.data
