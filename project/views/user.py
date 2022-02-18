from flask import request
from flask_restx import Namespace, Resource, abort

from project.exceptions import ItemNotFound
from project.services import UsersService
from project.setup_db import db
from project.tools.auth import auth_required
from project.tools.security import compare_passwords

user_ns = Namespace("user")


@user_ns.route('/')
class UserView(Resource):
    @auth_required
    @user_ns.response(200, "OK")
    @user_ns.response(404, "User not found")
    def get(self, token_data):
        try:
            return UsersService(db.session).get_by_email(token_data["email"])
        except ItemNotFound:
            abort(404, message="User not found")

    @auth_required
    def patch(self, token_data):
        user_d = request.json
        if not user_d:
            abort(400, message="Bad Request")
        return UsersService(db.session).update(token_data, user_d), 204


@user_ns.route('/password')
class UserPutView(Resource):
    @auth_required
    @user_ns.response(200, "OK")
    @user_ns.response(400, "Bad Request")
    def put(self, token_data):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        if not req_json.get("password_1") or not req_json.get("password_2"):
            abort(400, message="Bad Request")
        try:
            user = UsersService(db.session).get_by_email(token_data["email"])
            if not compare_passwords(user["password"], req_json.get("password_1")):
                # print(req_json)
                '''frontend bug: getting value from only the 'new password' field in both password_1 and password_2 
                {'password_1': 'asdfg', 'password_2': 'asdfg'}'''
                abort(401)
            return UsersService(db.session).update_pass(token_data, req_json.get("password_2"))
        except ItemNotFound:
            abort(404, message="User not found")
