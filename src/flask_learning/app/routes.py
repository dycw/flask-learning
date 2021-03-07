from flask import render_template

from flask_learning.app import app


@app.route("/")
@app.route("/index")
def index() -> str:
    user = {"username": "Derek"}
    return render_template("index.html", title="Home", user=user)
