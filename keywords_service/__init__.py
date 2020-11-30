""" The keywords_service package implements a Flask app
exposing several APIs for the extraction and manipulation of keywords
representing the content of a document. The submodule core contains the
stand-alone functions for extracting keywords and related tasks.
The submodule views contains the Flask blueprints for several groups
of functionality: absolute_keywords, documents, groups, and relative_keywords.
This package also includes helpers for authentication and database access."""

import os
from flask import Flask

from psycopg2 import OperationalError

from . import db, auth
from .views import absolute_keywords, documents, groups, relative_keywords

def create_app():
    """ Creates and configures the Flask app. A simple ping route is added
    to verify simple functionality. """

    app = Flask(__name__)
    app.config.from_mapping(
            SECRET_KEY=os.environ.get('FLASK_SECRET_KEY'),
            DATABASE_HOST=os.environ.get('POSTGRES_HOST'),
            DATABASE_PORT=os.environ.get('POSTGRES_PORT'),
            DATABASE_USER=os.environ.get('POSTGRES_USER'),
            DATABASE_PASSWORD=os.environ.get('POSTGRES_PASSWORD'),
            DATABASE_NAME=os.environ.get('POSTGRES_DB'),
    )

    app.url_map.strict_slashes = False

    @app.route('/ping')
    def ping():
        status = "alive"
        try:
            get_db()
        except OperationalError:
            status = "no_db"

        return {"status" : status}

    db.init_app(app)

    with app.app_context():
        db.init_db()

    app.register_blueprint(auth.bp)

    app.register_blueprint(documents.bp)
    app.register_blueprint(absolute_keywords.bp)
    app.register_blueprint(groups.bp)
    app.register_blueprint(relative_keywords.bp)

    return app
