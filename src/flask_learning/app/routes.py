import datetime as dt
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
from flask_learning.app import db_session
from flask_learning.app.forms import EditProfileForm
from flask_learning.app.forms import EmptyForm
from flask_learning.app.forms import LoginForm
from flask_learning.app.forms import PostForm
from flask_learning.app.forms import RegistrationForm
from flask_learning.app.models import Post
from flask_learning.app.models import User


RANDOM = SystemRandom()


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index() -> str:
    if not (form := PostForm()).validate_on_submit():
        posts = current_user.followed_posts().all()
        return render_template(
            "index.html", title="Home", form=form, posts=posts
        )
    post = Post(body=form.post.data, author=current_user)
    db_session.add(post)
    db_session.commit()
    flash("Your post is now live!")
    page = request.args.get("page", 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    next_url = url_for("index", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("index", page=posts.prev_num) if posts.has_prev else None
    return render_template(
        "index.html",
        title="Home",
        form=form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
    )


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


@app.route("/register", methods=["GET", "POST"])
def register() -> Union[Response, str]:
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if not (form := RegistrationForm()).validate_on_submit():
        return render_template("register.html", title="Register", form=form)
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db_session.add(user)
    db_session.commit()
    flash("Congratulations, you are now a registered user!")
    return redirect(url_for("login"))


@app.route("/user/<username>")
@login_required
def user(username: str) -> str:
    user: User = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    next_url = (
        url_for("user", username=user.username, page=posts.next_num)
        if posts.has_next
        else None
    )
    prev_url = (
        url_for("user", username=user.username, page=posts.prev_num)
        if posts.has_prev
        else None
    )
    form = EmptyForm()
    return render_template(
        "user.html",
        user=user,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
        form=form,
    )


@app.before_request
def before_request() -> None:
    if current_user.is_authenticated:
        current_user.last_seen = dt.datetime.utcnow()
        db_session.commit()


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile() -> Union[Response, str]:
    if (form := EditProfileForm(current_user.username)).validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db_session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    if request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@app.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username: str) -> Union[Response, str]:
    if not EmptyForm().validate_on_submit():
        return redirect(url_for("index"))
    if (user := User.query.filter_by(username=username).first()) is None:
        flash(f"User {username} not found.")
        return redirect(url_for("index"))
    if user == current_user:
        flash("You cannot follow yourself!")
        return redirect(url_for("user", username=username))
    current_user.follow(user)
    db_session.commit()
    flash(f"You are following {username}!")
    return redirect(url_for("user", username=username))


@app.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username: str) -> Union[Response, str]:
    if not EmptyForm().validate_on_submit():
        return redirect(url_for("index"))
    if (user := User.query.filter_by(username=username).first()) is None:
        flash(f"User {username} not found.")
        return redirect(url_for("index"))
    if user == current_user:
        flash("You cannot unfollow yourself!")
        return redirect(url_for("user", username=username))
    current_user.unfollow(user)
    db_session.commit()
    flash(f"You are not following {username}.")
    return redirect(url_for("user", username=username))


@app.route("/explore")
@login_required
def explore() -> str:
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    next_url = (
        url_for("explore", page=posts.next_num) if posts.has_next else None
    )
    prev_url = (
        url_for("explore", page=posts.prev_num) if posts.has_prev else None
    )
    return render_template(
        "index.html",
        title="Explore",
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
    )
