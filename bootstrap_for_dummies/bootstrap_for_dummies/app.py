from flask import Flask, render_template, request, flash, Markup, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import *
from flask_bootstrap import Bootstrap4, SwitchField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bootstrap_for_dummies.config import WebConfig

app = Flask(__name__)
app.config.from_object(WebConfig())


bootstrap = Bootstrap4(app)
app.secret_key = 'dev'

#db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return redirect(url_for('/'))

@app.route('/sb')
def sb_base(user=None):
    return render_template('base_side.html', user=user, messages=[])


if __name__ == '__main__':
    app.run(debug=True)