from flask import Flask
from .models import db, setup_db


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        setup_db(app)

    return app