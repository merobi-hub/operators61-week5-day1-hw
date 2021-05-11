from flask import Flask
from config import Config
from .site.routes import site # look for site in parent dir
from .authentication.routes import auth
from .api.routes import api
from flask_migrate import Migrate
from car_api.models import db as root_db, login_manager, ma
from flask_sqlalchemy import SQLAlchemy 

# CORS = cross origin resource sharing
from flask_cors import CORS

from car_api.helpers import JSONEncoder

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(api)
app.register_blueprint(site)
app.register_blueprint(auth)

root_db.init_app(app)
migrate = Migrate(app, root_db)
login_manager.init_app(app)
login_manager.login_view = 'auth.signin' # specifies route for non-authorized users

ma.init_app(app)
CORS(app)

app.json_encoder = JSONEncoder

from car_api import models
