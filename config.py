import os #base dir, tells flask where to find project

basedir = os.path.abspath(os.path.dirname(__file__)) #file refers to root dir in project tree

# gives access to project in any operating sys and allows access to outside folders

class Config():
    """
    Set config variables for the flask app here using env variables where available,
    otherwise create them if not done already
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess...'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #turns off notifications from db
