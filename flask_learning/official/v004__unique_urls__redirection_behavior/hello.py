from __future__ import annotations

from flask import Flask


app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "Index Page"


@app.route("/projects/")
def projects() -> str:
    return "The project page"


@app.route("/about")
def about() -> str:
    return "The about page"
