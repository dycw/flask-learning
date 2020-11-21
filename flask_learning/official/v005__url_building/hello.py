from __future__ import annotations

from flask import Flask
from flask import url_for
from markupsafe import escape


app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "index"


@app.route("/login")
def login() -> str:
    return "login"


@app.route("/user/<username>")
def profile(username: str) -> str:
    return f"{escape(username)}'s profile"


if __name__ == "__main__":
    with app.test_request_context():
        print(url_for("index"))
        print(url_for("login"))
        print(url_for("login", next="/"))
        print(url_for("profile", username="John Doe"))
