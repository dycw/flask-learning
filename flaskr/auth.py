from __future__ import annotations

import functools
from typing import Any

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug import Response
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register() -> Any:
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (
            db.execute(
                "SELECT id FROM user WHERE username = ?",
                (username,),
            ).fetchone()
            is not None
        ):
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    if not isinstance(out := render_template("auth/register.html"), Response):
        raise TypeError(out)
    return out


@bp.route("/login", methods=("GET", "POST"))
def login() -> Any:
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?",
            (username,),
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    if not isinstance(out := render_template("auth/login.html"), Response):
        raise TypeError(out)
    return out


@bp.before_app_request
def load_logged_in_user() -> None:
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db()
            .execute(
                "SELECT * FROM user WHERE id = ?",
                (user_id,),
            )
            .fetchone()
        )


@bp.route("/logout")
def logout() -> Any:
    session.clear()
    if not isinstance(out := redirect(url_for("index")), str):
        raise TypeError(out)
    return out


def login_required(view: Any) -> Any:
    @functools.wraps(view)
    def wrapped_view(**kwargs: Any) -> Any:
        if g.user is None:
            if not isinstance(out := redirect(url_for("auth.login")), str):
                raise TypeError(out)
            return out

        if not isinstance(out := view(**kwargs), str):
            raise TypeError(out)
        return out

    if not isinstance(wrapped_view, str):
        raise TypeError(wrapped_view)
    return wrapped_view
