from __future__ import annotations

from flask import Flask
from flask.testing import FlaskClient
from pytest import mark

from flaskr.db import get_db
from tests.conftest import AuthActions


def test_index(client: FlaskClient, auth: AuthActions) -> None:
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"Log Out" in response.data
    assert b"test title" in response.data
    assert b"by test on 2018-01-01" in response.data
    assert b"test\nbody" in response.data
    assert b'href="/1/update"' in response.data


@mark.parametrize(  # type: ignore
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_login_required(client: FlaskClient, path: str) -> None:
    response = client.post(path)
    assert response.headers["Location"] == "http://localhost/auth/login"


def test_author_required(
    app: Flask,
    client: FlaskClient,
    auth: AuthActions,
) -> None:
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET author_id = 2 WHERE id = 1")
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get("/").data


@mark.parametrize(
    "path",
    (  # type: ignore
        "/2/update",
        "/2/delete",
    ),
)
def test_exists_required(
    client: FlaskClient,
    auth: AuthActions,
    path: str,
) -> None:
    auth.login()
    assert client.post(path).status_code == 404
