from __future__ import annotations

from sqlite3.dbapi2 import ProgrammingError

from _pytest.monkeypatch import MonkeyPatch
from flask import Flask
from flask.testing import FlaskCliRunner
from pytest import raises

from flaskr.db import get_db


def test_get_close_db(app: Flask) -> None:
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with raises(ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(
    runner: FlaskCliRunner,
    monkeypatch: MonkeyPatch,
) -> None:
    class Recorder:
        called = False

    def fake_init_db() -> None:
        Recorder.called = True

    monkeypatch.setattr("flaskr.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
