#from flask.ext.wtf import Form
from wtforms import TextAreaField, DateField, IntegerField, Form, validators


class SearchForm(Form):
    year = IntegerField('year', validators=[validators.optional(), validators.NumberRange(min=1900, max=2022, message='Not a valid year or no data')])
    author = TextAreaField('author', [validators.optional()])
    topic = TextAreaField('topic', validators=[validators.optional()])