from __future__ import annotations

from flask import Flask
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
