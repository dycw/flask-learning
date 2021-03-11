from typing import cast

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session

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
