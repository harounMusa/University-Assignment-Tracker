from flask import Flask, request, session
from flask_restful import Api, Resource, abort
import os

class AdminLogin(Resource):
    def post(self):
        data = request.get_json()

        if not data or 'password' not in data:
            return {'message': 'Password required'}, 400
        
        if data['password'] == os.getenv('LEADER_PSW'):
            session.permanent = True
            session['is_admin'] = True
            return {'message': 'Admin logged in successfully'}, 200
        
        return {'message': 'You are not the Leader'}, 401

class AdminLogout(Resource):
    def post(self):
        session.clear()
        return {'message': 'Admin logged out successfully'}, 200

class AdminCheck(Resource):
    def get(self):
        is_admin = session.get('is_admin') is True
        return {'is_admin': is_admin}, 200