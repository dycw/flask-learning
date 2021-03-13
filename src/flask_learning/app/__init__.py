from logging import ERROR
from typing import cast

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from ssl_smtp_handler import SSLSMTPHandler

from flask_learning.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db_session = cast(Session, db.session)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"  # type: ignore


from flask_learning.app import errors  # noqa: E402, F401
from flask_learning.app import models  # noqa: E402, F401
from flask_learning.app import routes  # noqa: E402, F401


if not app.debug and (mail_host := app.config["MAIL_HOST"]):
    mail_username = app.config["MAIL_USERNAME"]
    handler = SSLSMTPHandler(
        mailhost=mail_host,
        fromaddr=mail_username,
        toaddrs=[app.config["MAIL_TO_ADDRESS"]],
        subject="Microblog failure",
        credentials=(mail_username, app.config["MAIL_PASSWORD"]),
    )
    handler.setLevel(ERROR)
    app.logger.addHandler(handler)
