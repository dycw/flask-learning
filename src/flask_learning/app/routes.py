from random import SystemRandom

from flask import render_template

from flask_learning.app import app
from flask_learning.app.forms import LoginForm


RANDOM = SystemRandom()


@app.route("/")
@app.route("/index")
def index() -> str:
    title = "Home" if RANDOM.uniform(0.0, 1.0) <= 0.5 else None
    user = {"username": "Derek"}
    posts = [
        {"author": {"username": "John"}, "body": "Beautiful day in Portland!"},
        {
            "author": {"username": "Susan"},
            "body": "The Avengers movie was so cool!",
        },
    ]
    return render_template("index.html", title=title, user=user, posts=posts)


@app.route("/login")
def login() -> str:
    form = LoginForm()
    return render_template("login.html", title="Sign In", form=form)
