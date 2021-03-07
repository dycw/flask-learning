from flask import Flask

from flask_learning.config import Config


app = Flask(__name__)
app.config.from_object(Config)


from flask_learning.app import routes  # noqa: E402, F401
