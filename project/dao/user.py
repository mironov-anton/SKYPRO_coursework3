import sqlalchemy.exc
from sqlalchemy.orm import scoped_session

from project.dao.models import User
from project.exceptions import DuplicateError


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_all(self):
        return self._db_session.query(User).all()

    def get_by_email(self, email: str):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def create(self, user_d):
        try:
            ent = User(**user_d)
            self._db_session.add(ent)
            self._db_session.commit()
            return ent
        except sqlalchemy.exc.IntegrityError:
            raise DuplicateError
