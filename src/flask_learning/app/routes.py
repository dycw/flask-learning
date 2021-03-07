from flask_learning.app import app


@app.route("/")
@app.route("/index")
def index() -> str:
    return "Hello, World!"
