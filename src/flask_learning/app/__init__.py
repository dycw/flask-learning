from flask import Flask


app = Flask(__name__)


from flask_learning.app import routes  # noqa: E402, F401
