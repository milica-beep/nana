from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
from mongo_db import db
from passlib.hash import sha256_crypt

auth_route = Blueprint('auth', __name__)

users = db.users

@auth_route.route('/auth/login', methods=['POST'])
def login():
    req = request.get_json()
    email = str(req['email'])
    password_candidate = str(req['password'])

    if not email:
        return {'email': 'This field is required.'}, 400

    if not password_candidate:
        return {'password': 'This field is required.'}, 400

    existing_user = users.find_one({'email': email})

    if not existing_user:
        return jsonify({'message':'The email you entered is not connected to an account.'}), 422

    if sha256_crypt.verify(password_candidate, existing_user['password']):
        access_token = create_access_token(identity=existing_user['email'])
        resp = jsonify({'message': 'Uspešno prijavljivanje', 'access_token' : access_token})
        return resp, 200
    else:
        return jsonify({'message': 'Wrong data'}), 422


@auth_route.route('/auth/register', methods=['GET', 'POST'])
def register():
    req = request.get_json()

    name = str(req['name'])
    lastname = str(req['lastname'])
    email = str(req['email'])
    password = str(req['password'])

    # Check if fields are empty

    if not name:
        return {'name': 'This field is required.'}, 400

    if not lastname:
        return {'lastname': 'This field is required.'}, 400

    if not email:
        return {'email': 'This field is required.'}, 400

    if not password:
        return {'password': 'This field is required.'}, 400

    # Check if email already exists

    existing_user = users.find_one({'email': email})

    if existing_user:
        return jsonify({'message': 'Email already in use.'}), 422

    # Create user

    new_user = {
        'email': email,
        'password': sha256_crypt.hash(password),
        'name': name,
        'lastname': lastname
    }

    user_id = users.insert_one(new_user).inserted_id
    print(user_id)

    return jsonify({'message': 'Successfully registered'}), 200

@auth_route.route('/auth/current-user', methods=['GET'])
@jwt_required()
def current_user():
    user_id = get_jwt_identity()
    existing_user = users.find_one({'email': user_id})
    return {'user': existing_user}