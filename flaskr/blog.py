from __future__ import annotations

from typing import Any
from typing import Union

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug import Response
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint("blog", __name__)


@bp.route("/")
def index() -> Any:
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC",
    ).fetchall()
    if not isinstance(
        out := render_template("blog/index.html", posts=posts),
        str,
    ):
        raise TypeError(type(out))
    return out


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create() -> Union[str, Response]:
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id)" " VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            if not isinstance(out := redirect(url_for("blog.index")), Response):
                raise TypeError(type(out))
            return out

    if not isinstance(out2 := render_template("blog/create.html"), str):
        raise TypeError(type(out2))
    return out2


def get_post(id: int, check_author: bool = True) -> Any:  # noqa: A002
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    if not isinstance(post, str):
        raise TypeError(type(post))
    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id: int) -> Any:  # noqa: A002
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?" " WHERE id = ?",
                (title, body, id),
            )
            db.commit()
            if not isinstance(out := redirect(url_for("blog.index")), str):
                raise TypeError(type(out))
            return out

    if not isinstance(
        out2 := render_template("blog/update.html", post=post),
        str,
    ):
        raise TypeError(type(out2))
    return out2


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id: int) -> Any:  # noqa: A002
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    if not isinstance(out := redirect(url_for("blog.index")), str):
        raise TypeError(type(out))
    return out
