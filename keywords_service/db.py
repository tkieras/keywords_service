""" Contains helper functions for interfacing with the database """

import psycopg2
import psycopg2.extras
from flask import current_app, g

def get_db():
    """ Returns a tuple of database and cursor objects. Stores the connection
    in Flask's g object for use in current connection lifetime. With postgresql
    both are needed for various operations. The cursor is initialized as a 
    DictCursor. """
    if 'db' not in g:
        g.db = psycopg2.connect(
                host=current_app.config['DATABASE_HOST'],
                port=current_app.config['DATABASE_PORT'],
                dbname=current_app.config['DATABASE_NAME'],
                user=current_app.config['DATABASE_USER'],
                password=current_app.config['DATABASE_PASSWORD']
        )

    return g.db, g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

def close_db(e=None):
    """ Closes database and removes from g object."""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    """ Helper function to register the close_db function with create_app."""
    app.teardown_appcontext(close_db)
