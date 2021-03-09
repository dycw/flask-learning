from typing import Any

from flask_learning.app import app
from flask_learning.app import db
from flask_learning.app.models import Post
from flask_learning.app.models import User


@app.shell_context_processor
def make_shell_context() -> dict[str, Any]:
    return {"db": db, "User": User, "Post": Post}
