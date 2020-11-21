from __future__ import annotations

from flask import Flask


app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "Index Page"


@app.route("/hello")
def hello() -> str:
    return "Hello, World"
