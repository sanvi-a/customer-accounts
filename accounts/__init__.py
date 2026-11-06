"""Customer Accounts microservice application factory."""
import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

db = SQLAlchemy()


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///accounts.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    # Security headers (Sprint 3). HTTPS is terminated at the ingress/route,
    # so the app itself must not redirect plain HTTP requests.
    Talisman(app, force_https=False)
    # CORS policy (Sprint 3)
    CORS(app)

    # pylint: disable=import-outside-toplevel,cyclic-import
    from accounts import routes  # noqa: F401
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()

    return app
