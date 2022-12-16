import os
basedir = os.path.abspath(os.path.dirname(__file__))


class WebConfig(object):
    #in app encryption:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #route to db provider like java jdbi connection string:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #bootstrap setup
    BOOTSTRAP_BTN_STYLE ='primary'
    BOOTSTRAP_BTN_SIZE = 'sm'
    #BOOTSTRAP_SERVE_LOCAL = True
    BOOTSTRAP_BOOTSWATCH_THEME = 'darkly'
    #BOOTSTRAP_BOOTSWATCH_THEME = 'cerulean'
    # bootstrap naming
    # set default icon title of table actions
    BOOTSTRAP_TABLE_VIEW_TITLE = 'Read'
    BOOTSTRAP_TABLE_EDIT_TITLE = 'Update'
    BOOTSTRAP_TABLE_DELETE_TITLE = 'Remove'
    BOOTSTRAP_TABLE_NEW_TITLE = 'Create'
    #mail server setup:
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    #misc
    POSTS_PER_PAGE = 25