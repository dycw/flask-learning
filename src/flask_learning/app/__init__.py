from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_learning.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from flask_learning.app import models  # noqa: E402, F401
from flask_learning.app import routes  # noqa: E402, F401
