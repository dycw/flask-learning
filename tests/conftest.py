from __future__ import annotations

import os
import tempfile
from typing import Any
from typing import Iterator

from flask import Flask
from flask import Response
from flask.testing import FlaskClient
from flask.testing import FlaskCliRunner
from pytest import fixture

from flaskr import create_app
from flaskr.db import get_db
from flaskr.db import init_db


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@fixture  # type: ignore
def app() -> Iterator[Flask]:
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        },
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@fixture  # type: ignore
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@fixture  # type: ignore
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


class AuthActions:
    def __init__(self: AuthActions, client: FlaskClient) -> None:
        self._client = client

    def login(  # noqa: S107
        self: AuthActions,
        username: str = "test",
        password: str = "test",
    ) -> Response:
        return self._client.post(
            "/auth/login",
            data={"username": username, "password": password},
        )

    def logout(self: AuthActions) -> Any:
        out = self._client.get("/auth/logout")
        raise TypeError(type(out))

        return self._client.get("/auth/logout")


@fixture  # type: ignore
def auth(client: FlaskClient) -> AuthActions:
    return AuthActions(client)