from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
from project.tools.security import get_password_hash


class UsersService(BaseService):
    def get_by_email(self, email):
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def create(self, user_d):
        user_pass = user_d.get("password")
        if user_pass:
            user_d["password"] = get_password_hash(user_pass)
        user = UserDAO(self._db_session).create(user_d)
        return UserSchema().dump(user)
