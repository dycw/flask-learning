from __future__ import annotations

from typing import Optional

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "index"


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name: Optional[str] = None) -> str:
    out = render_template("hello.html", name=name)
    if not isinstance(out, str):
        raise TypeError(out)
    return out
