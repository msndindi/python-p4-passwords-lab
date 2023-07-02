#!/usr/bin/env python3

from flask import request, session, jsonify
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):
    def delete(self):    
        session['page_views'] = None
        session['user_id'] = None
        return {}, 204
api.add_resource(ClearSession, '/clear', endpoint='clear')  

class Signup(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']
        if username and password:
            new_user = User(username=username)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return new_user.to_dict(), 201
        return {'error': '422 Unprocessable Entity'}, 422
api.add_resource(Signup, '/signup', endpoint='signup')

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session.get('user_id')).first()
            return user.to_dict(), 200  ## OR ## return jsonify(user.to_dict()), 200 ##
        return {'message': '204: Completed'}, 204  ## OR ## return jsonify({'message': '401: Not Authorized'}), 401 ##
api.add_resource(CheckSession, '/check_session', endpoint='check_session')

class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']
        user = User.query.filter(User.username == username).first()
        if user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200     ## OR ## return jsonify(user.to_dict()), 200 ##
        return {'error': '401 Unauthorized'}, 401
api.add_resource(Login, '/login', endpoint='login')

class Logout(Resource):
    def delete(self): 
        session['user_id'] = None
        return {'message': '204: No Content'}, 204  ## OR ## return jsonify({'message': '204: No Content'}), 204 ##
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)