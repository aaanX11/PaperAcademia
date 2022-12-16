import sqlite3
import psycopg2
from sqlalchemy import create_engine
import click
from flask import current_app
from flask import g
from flask import Flask
#
# conn = psycopg2.connect(database="mytest",
#                             host="127.0.0.1",
#                             user="postgres",
#                             password="mysecretpassword",
#                             port="5432")
#
#     cursor = conn.cursor()
#     cursor.execute('''DROP TABLE IF EXISTS links;''')


def get_engine():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "engine" not in g:
        engine = create_engine('postgresql://flaskdbusr:flaskdbpw@127.0.0.1:5432/flaskdb')

        g.engine = engine.connect()

    return g.engine


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_engine()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

app = Flask(__name__)

@app.route("/")
def register():
    get_engine()
    return "hello"

if __name__ == '__main__':
    print()

    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
