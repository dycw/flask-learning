from random import SystemRandom
from typing import Union

from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_user
from werkzeug import Response

from flask_learning.app import app
from flask_learning.app.forms import LoginForm
from flask_learning.app.models import User


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


@app.route("/login", methods=["GET", "POST"])
def login() -> Union[str, Response]:
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password")
                return redirect(url_for("login"))
            else:
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for("index"))
        else:
            return render_template("login.html", title="Sign In", form=form)
