from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import uuid # stands for unique user identifier -- for primary keys

# adding Flask security
from werkzeug.security import generate_password_hash, check_password_hash 

# secrets module in python for token, hex value
import secrets

from flask_login import UserMixin, LoginManager

# install marshaller
from flask_marshmallow import Marshmallow




db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4()) # generates random uuid

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash 

    def __repr__(self):
        return f"User: {self.email} has been created and added to the database!"

class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    model = db.Column(db.String(100))
    make = db.Column(db.String(100))
    year = db.Column(db.Numeric(precision = 4))
    category = db.Column(db.String(20))
    seats = db.Column(db.Numeric(precision = 2))
    horsepower = db.Column(db.Numeric(precision = 4))
    torque = db.Column(db.Numeric(precision = 3))
    color = db.Column(db.String(20))
    interior = db.Column(db.String(20))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, model, make, year, category, seats, horsepower, torque, color, interior, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.model = model
        self.make = make
        self.year = year
        self.category = category
        self.seats = seats
        self.horsepower = horsepower
        self.torque = torque
        self.color = color
        self.interior = interior
        self.user_token = user_token
                
    def __repr__(self):
        return f'The following car has been created: {self.name}'

    def set_id(self):
        return str(uuid.uuid4())

#API schema via marshmallow
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'model', 'make', 'year', 'category', 'seats', 'horsepower', 'torque', 'color', 'interior']

# singular data point return
car_schema = CarSchema()

#list of objects
car_schemas = CarSchema(many = True)