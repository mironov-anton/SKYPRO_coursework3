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

    def update(self, token_data, user_d):
        user = UserDAO(self._db_session).get_by_email(token_data["email"])
        if "name" in user_d:
            user.name = user_d.get("name")
        if "surname" in user_d:
            user.surname = user_d.get("surname")
        if "favourite_genre" in user_d:
            user.favorite_genre = user_d.get("favourite_genre")
        return UserDAO(self._db_session).update(user)

    def update_pass(self, token_data, password_2):
        user = UserDAO(self._db_session).get_by_email(token_data["email"])
        user.password = get_password_hash(password_2)
        return UserDAO(self._db_session).update(user)
