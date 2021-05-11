# Purpose here: ensure everyone accessing the api has a user token
# This is like @loginrequired but we're making it ourselves

from functools import wraps # wrapper
import secrets # serial ids, hextools

from flask import request, jsonify
from car_api.models import Car, User

def token_required(our_flask_function):
    """when this placed above a fun with @, that fun gets passed in as arg"""
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        # handle a request from Insomnia
        if 'x-access-token' in request.headers:
            # set token as equal to incoming token from Insomnia
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        # check if incoming token matches token of current user
        try:
            current_user_token = User.query.filter_by(token = token).first() # specify first data point returned

        except:
            owner = User.query.filter_by(token = token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid!'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

# deal with json's difficulty handling floats by converting floats to strings
# we may have decimal values in models that must be converted
import decimal
from flask import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # convert to string
            return str(obj)

        # use super to override our objects within the class
        # checks all objects in class
        return super(JSONEncoder, self).default(obj)



















