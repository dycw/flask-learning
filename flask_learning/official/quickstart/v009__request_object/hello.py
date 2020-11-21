from __future__ import annotations

from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "index"


@app.route("/login", methods=["POST", "GET"])
def login() -> str:
    error = None
    if request.method == "POST":
        if valid_login(  # type: ignore  # noqa: F821
            request.form["username"],
            request.form["password"],
        ):
            return log_the_user_in(  # type: ignore # noqa: F821
                request.form["username"],
            )
        else:
            error = "Invalid username/password"
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template("login.html", error=error)
