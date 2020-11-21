from __future__ import annotations

from flask import Flask
from flask import request


app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "index"


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        return do_the_login()  # type: ignore # noqa: F821
    else:
        return show_the_login_form()  # type: ignore # noqa: F821
