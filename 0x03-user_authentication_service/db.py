#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """saves users to db"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kw) -> User:
        """Returns the first row of users matching kwargs"""
        keys = ['id', 'email', 'hashed_password', 'session_id', 'reser_token']

        for k in kw.keys():
            if k not in keys:
                raise InvalidRequestError

        result = self._session.query(User).filter_by(**kw).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kw) -> None:
        """Update a user found by find_user method"""
        try:
            keys = ['id', 'email', 'hashed_password', 'session_id',
                    'reser_token']
            user = self.find_user_by(id=user_id)
            for k, v in kw.items():
                if k in keys:
                    setattr(user, k, v)
        except (InvalidRequestError, NoResultFound):
            raise ValueError("Error updating")
        self._session.commit()
