from flask import request, abort
from flask_restx import Namespace, Resource
from marshmallow import fields, Schema, ValidationError

from project.services import UsersService
from project.setup_db import db
from project.tools.jwt_token import JwtSchema, JwtToken
from project.tools.security import compare_passwords

auth_ns = Namespace('auth')


class LoginValidator(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class RefreshTokenValidator(Schema):
    refresh_token = fields.Str(required=True)


@auth_ns.route('/register')
class AuthRegisterView(Resource):
    def post(self):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        return UsersService(db.session).create(req_json)


@auth_ns.route('/login')
class AuthLoginView(Resource):
    def post(self):
        try:
            validated_data = LoginValidator().load(request.json)
            user = UsersService(db.session).get_by_email(validated_data["email"])
            if not user:
                abort(401)

            if not compare_passwords(user["password"], validated_data["password"]):
                abort(401)

            token_data = JwtSchema().load({"email": user["email"]})
            return JwtToken(token_data).get_tokens(), 201

        except ValidationError:
            abort(400)

    def put(self):
        try:
            validated_data = RefreshTokenValidator().load(request.json)
            token_data = JwtToken.decode_token(validated_data["refresh_token"])
            user = UsersService(db.session).get_by_email(token_data["email"])
            if not user:
                abort(401)

            new_token_data = JwtSchema().load({"email": user["email"]})
            return JwtToken(new_token_data).get_tokens(), 201

        except ValidationError:
            abort(400)
