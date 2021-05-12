from flask import Blueprint, request, jsonify
from flask.helpers import make_response
from car_api import models
from car_api.helpers import token_required
from car_api.models import User, Car, car_schema, car_schemas, db

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 73}

# CREATE CAR ENDPOINT
@api.route('/cars', methods=['POST'])
@token_required # protects route -- only for valid tokens
def create_car(current_user_token): # comes from token_required decorator
    """create_car will be our_flask_function"""
    name = request.json['name']
    model = request.json['model']
    make = request.json['make']
    year = request.json['year']
    category = request.json['category']
    seats = request.json['seats']
    horsepower = request.json['horsepower']
    torque = request.json['torque']
    color = request.json['color']
    interior = request.json['interior']
    user_token = current_user_token.token # comes from token_required wrapper

    car = Car(name,model,make,year,category,seats,horsepower,torque,color,interior,user_token=user_token)

    db.session.add(car)
    db.session.commit()
    response = car_schema.dump(car) # turns sql data into list obj that can be jsonified
    return jsonify(response)

# RETRIEVE ALL CARS
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all() # returns all cars for user
    response = car_schemas.dump(cars)
    return jsonify(response)

# RETRIEVE ONE CAR ENDPOINT
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

# UPDATE CAR BY ID
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)

    #below will modify car in db
    car.name = request.json['name']
    car.model = request.json['model']
    car.make = request.json['make']
    car.year = request.json['year']
    car.category = request.json['category']
    car.seats = request.json['seats']
    car.horsepower = request.json['horsepower']
    car.torque = request.json['torque']
    car.color = request.json['color']
    car.interior = request.json['interior']
    car.user_token = current_user_token.token # comes from token_required wrapper

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# DELETE DRONE BY ID
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

    





























