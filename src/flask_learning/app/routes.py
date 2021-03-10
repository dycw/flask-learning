from random import SystemRandom
from typing import Optional
from typing import Union
from typing import cast

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug import Response
from werkzeug.urls import url_parse

from flask_learning.app import app
from flask_learning.app.forms import LoginForm
from flask_learning.app.models import User


RANDOM = SystemRandom()


@app.route("/")
@app.route("/index")
@login_required
def index() -> str:
    title = "Home" if RANDOM.uniform(0.0, 1.0) <= 0.5 else None
    posts = [
        {"author": {"username": "John"}, "body": "Beautiful day in Portland!"},
        {
            "author": {"username": "Susan"},
            "body": "The Avengers movie was so cool!",
        },
    ]
    return render_template("index.html", title=title, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login() -> Union[Response, str]:
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if not (form := LoginForm()).validate_on_submit():
        return render_template("login.html", title="Sign In", form=form)
    user = cast(
        Optional[User],
        User.query.filter_by(username=form.username.data).first(),
    )
    if (user is None) or not user.check_password(form.password.data):
        flash("Invalid username or password")
        return redirect(url_for("login"))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get("next")
    location = (
        url_for("index")
        if not next_page or url_parse(next_page).netloc != ""
        else next_page
    )
    return redirect(location)


@app.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("index"))
