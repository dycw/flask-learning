from __future__ import annotations

from flask import Flask
from markupsafe import escape


app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "Index Page"


@app.route("/user/<username>")
def show_user_profile(username: str) -> str:
    if not isinstance(username, str):
        raise TypeError(username)
    # show the user profile for that user
    return f"User {escape(username)}"


@app.route("/post/<int:post_id>")
def show_post(post_id: int) -> str:
    if not isinstance(post_id, int):
        raise TypeError(post_id)
    # show the post with the given id, the id is an integer
    return "Post %d" % post_id


@app.route("/path/<path:subpath>")
def show_subpath(subpath: str) -> str:
    if not isinstance(subpath, str):
        raise TypeError(subpath)
    # show the subpath after /path/
    return f"Subpath {escape(subpath)}"
