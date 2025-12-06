from flask import Flask, request
from flask_restful import Api, Resource, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import UserModel, db



class Register(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if UserModel.query.filter_by(username=username).first():
            abort(404, message='user can not be found')
        
        generated_password = generate_password_hash(password)
        new_user = UserModel(username = username, password = generated_password)

        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created seccessfully'}, 201 
    

class  Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        user = UserModel.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return {'access_token' : access_token, 'username' : user.username}, 200
        

        return {'message': 'Invalid Credentials'}, 401 