from random import SystemRandom

from flask import render_template

from flask_learning.app import app


RANDOM = SystemRandom()


@app.route("/")
@app.route("/index")
def index() -> str:
    title = "Home" if RANDOM.uniform(0.0, 1.0) <= 0.5 else None
    user = {"username": "Derek"}
    return render_template("index.html", title=title, user=user)
