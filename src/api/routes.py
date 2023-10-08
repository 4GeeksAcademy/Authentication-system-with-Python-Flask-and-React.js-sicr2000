"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import re
import bcrypt

def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/accounts/user', methods=['POST'])
def create_user():

    body = request.get_json()

    name = body.get("name", None)
    last_name = body.get("last_name", None)
    email = body.get("email", None)
    password = body.get("password", None)

    bpassword = bytes(password, 'utf-8')

    salt = bcrypt.gensalt(14)

    hashed_password = bcrypt.hashpw(password=bpassword, salt=salt)

    print( len(hashed_password.decode('utf-8')), len(salt.decode('utf-8')))

    if email != None and password != None:
        
        if check(email) == False:
            return { "message": "email format is invalid" }, 400
        

        try:
            new_user = User(name=name, last_name=last_name, email=email, password=hashed_password.decode('utf-8'), salt=salt.decode('utf-8'))

            db.session.add(new_user)

            db.session.commit()

        except ValueError as error:
            return {"message": "An error has occured" + error}, 500
    
    else:
        return { "message": "user fields missing in request body" }, 400

    return jsonify(body), 200
    
@api.route ('/token', methods=['POST'])
def create_token():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if email is None or password is None:
        return {'message': "parameter missing"}, 400
    user = User.query.filter_by(email=email).one_or_none()
    if user is None:
        return {'message': "user doesn't exist"}, 400
    password_byte = bytes(password, 'utf-8')
    if bcrypt.checkpw(password_byte, user.password.encode('utf-8')):
        return {'token': create_access_token(identity = user.email)}, 200
    return {'message': 'you shall no pass'}, 501

@api.route('/profile')
@jwt_required()
def get_user_profile():
    email = get_jwt_identity()

    # body = request.get_json()

    # name = body.get("name", None)
    # last_name = body.get("last_name", None)
    # email = body.get("email", None)

    # name = request.json.get('name', None)
    # last_name = request.json.get('last_name', None)
    # email = request.json.get('email', None)

    user = User.query.filter_by(email=email).one_or_none()
    if user is not None:
        return user.serialize(), 200
    
    return {"message": "Not Authorized"}, 401

# name=name, last_name=last_name, 