from os import environ
from pathlib import Path


PATH_DB = Path(__file__).absolute().parent.joinpath("app.db")


class Config:
    SECRET_KEY = environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = (
        environ.get("DATABASE_URL") or f"sqlite:///{PATH_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
