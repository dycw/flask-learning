from __future__ import annotations

from sqlite3 import Connection
from sqlite3.dbapi2 import connect
from sqlite3.dbapi2 import PARSE_DECLTYPES
from sqlite3.dbapi2 import Row
from typing import Any

from click import command
from click import echo
from flask import current_app
from flask import Flask
from flask import g
from flask.cli import with_appcontext


def get_db() -> Connection:
    if "db" not in g:
        g.db = connect(
            current_app.config["DATABASE"],
            detect_types=PARSE_DECLTYPES,
        )
        g.db.row_factory = Row

    return g.db


def close_db(e: Any = None) -> None:  # noqa: U100
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@command("init-db")
@with_appcontext
def init_db_command() -> None:
    """Clear the existing data and create new tables."""
    init_db()
    echo("Initialized the database.")


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
