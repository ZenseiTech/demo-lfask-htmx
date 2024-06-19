"""Setup the application."""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

persistent_path = os.getenv(
    "PERSISTENT_STORAGE_DIR", os.path.dirname(os.path.realpath(__file__))
)

app = Flask(__name__)

db_path = os.path.join(persistent_path, "sqlite.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()


def do_import():
    """Trick to bypass git_commit error of being imported by unused."""
    from app import models, views

    models.logger
    views.logger


db.init_app(app)

with app.app_context():
    db.create_all()

do_import()
