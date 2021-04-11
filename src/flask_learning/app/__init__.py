from logging import ERROR
from logging import INFO
from logging import Formatter
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import cast

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
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
mail = Mail(app)


from flask_learning.app import errors  # noqa: E402, F401
from flask_learning.app import models  # noqa: E402, F401
from flask_learning.app import routes  # noqa: E402, F401


if not app.debug:
    app.logger.setLevel(INFO)

    if mail_host := app.config["MAIL_HOST"]:
        mail_username = app.config["MAIL_USERNAME"]
        smtp_handler = SSLSMTPHandler(
            mailhost=mail_host,
            fromaddr=mail_username,
            toaddrs=[app.config["MAIL_TO_ADDRESS"]],
            subject="Microblog failure",
            credentials=(mail_username, app.config["MAIL_PASSWORD"]),
        )
        smtp_handler.setLevel(ERROR)
        app.logger.addHandler(smtp_handler)

    logs = Path("logs")
    logs.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        logs.joinpath("microblog.log"), maxBytes=10240, backupCount=1
    )
    file_handler.setFormatter(
        Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(INFO)
    app.logger.addHandler(file_handler)

    app.logger.info("Microblog startup")
