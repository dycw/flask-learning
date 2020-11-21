from __future__ import annotations

import os
from typing import Any
from typing import Dict
from typing import Optional

from flask import Flask


__version__ = "0.0.2"


def create_app(test_config: Optional[Dict[str, Any]] = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(  # noqa: S106
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello() -> str:
        return "Hello, World!"

    from . import db

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import blog

    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app