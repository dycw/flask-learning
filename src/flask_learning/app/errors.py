from typing import Any

from flask import render_template

from flask_learning.app import app
from flask_learning.app import db_session


@app.errorhandler(404)
def not_found_error(error: Any) -> tuple[Any, int]:
    raise NotImplementedError(type(error), render_template("404.html"))
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error: Any) -> tuple[Any, int]:
    raise NotImplementedError(type(error), render_template("404.html"))
    db_session.rollback()
    return render_template("500.html"), 500
