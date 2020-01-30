import os
from pathlib import Path

basedir = Path(__file__).parent.absolute()

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
                                             "sqlite:///" + str(basedir / "app.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
