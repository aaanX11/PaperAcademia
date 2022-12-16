import os
from flask import Flask, url_for, render_template
from jinja2 import Template
from flask_bootstrap import Bootstrap4, SwitchField
from flask_dash.config import WebConfig

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
    )
    app.config.from_object(WebConfig())
    bootstrap = Bootstrap4(app)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from flask_dash import db

    db.init_app(app)
    with app.app_context():

        # Import Dash application
        from .dashboard import create_dashboard
        app = create_dashboard(app)


        # apply the blueprints to the app
        from flask_dash import auth, blog, routes

        app.register_blueprint(auth.bp)
        #app.register_blueprint(blog.bp)
        app.register_blueprint(routes.bp)



        # make url_for('index') == url_for('blog.index')
        # in another app, you might define a separate main index here with
        # app.route, while giving the blog blueprint a url_prefix, but for
        # the tutorial the blog will be the main index
        app.add_url_rule("/", endpoint="index")

        return app


