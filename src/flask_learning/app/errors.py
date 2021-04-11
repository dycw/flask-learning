from typing import Any

from flask import render_template
from werkzeug.exceptions import NotFound

from flask_learning.app import app
from flask_learning.app import db_session


@app.errorhandler(404)
def not_found_error(error: NotFound) -> tuple[str, int]:  # noqa: U100
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error: Any) -> tuple[Any, int]:
    raise NotImplementedError(type(error), render_template("500.html"))
    db_session.rollback()
    return render_template("500.html"), 500
