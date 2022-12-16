import sqlite3
import psycopg2
from sqlalchemy import create_engine
import click
from flask import current_app
from flask import g
from flask import Flask


def get_engine():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "engine" not in g:
        engine = create_engine('postgresql://flaskdbusr:flaskdbpw@host.docker.internal:5432/flaskdb')
        #engine = create_engine('postgresql://flaskdbusr:flaskdbpw@127.0.0.1:5432/flaskdb')

        g.engine = engine.connect()

    return g.engine


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    engine = g.pop("engine", None)

    if engine is not None:
        engine.close()


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
