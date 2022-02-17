from typing import Dict, Any

from flask import request, abort
from jwt import PyJWTError
from marshmallow import ValidationError

from project.tools.jwt_token import JwtToken, JwtSchema


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        auth_header = request.headers['Authorization']
        token = auth_header.split("Bearer ")[-1]
        try:
            data = JwtToken.decode_token(token)
            token_data: Dict[str, Any] = JwtSchema().load(data)
            return func(*args, **kwargs, token_data=token_data)
        except (PyJWTError, ValidationError):
            abort(401)

    return wrapper
