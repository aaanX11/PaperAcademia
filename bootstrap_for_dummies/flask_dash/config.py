import os
basedir = os.path.abspath(os.path.dirname(__file__))


class WebConfig(object):
    #in app encryption:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #route to db provider like java jdbi connection string:


    #bootstrap setup
    BOOTSTRAP_BTN_STYLE ='primary'
    BOOTSTRAP_BTN_SIZE = 'sm'
    #BOOTSTRAP_SERVE_LOCAL = True
    #BOOTSTRAP_BOOTSWATCH_THEME = 'darkly'
    #BOOTSTRAP_BOOTSWATCH_THEME = 'cerulean'
    # bootstrap naming
    # set default icon title of table actions
    BOOTSTRAP_TABLE_VIEW_TITLE = 'Read'
    BOOTSTRAP_TABLE_EDIT_TITLE = 'Update'
    BOOTSTRAP_TABLE_DELETE_TITLE = 'Remove'
    BOOTSTRAP_TABLE_NEW_TITLE = 'Create'


    #misc
    POSTS_PER_PAGE = 25