#!/usr/bin/env python3
""" Auth Class """
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """hash the password"""
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


def _generate_uuid() -> str:
    """generate unique id"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialization"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates credentials"""
        try:
            user = self._db.find_user_by(email=email)
            pass_check brycpt.checkpw(password.encode('utf-8'),
                                      user.hashed_password)
            if pass_check:
                return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """creates session """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """Return user from a session"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Returns none"""
        try:
            user = self.__db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Get password upon reset"""
        new_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=new_token)
            return new_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> str:
        """Update users password"""
        if password is None or reset_token is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_pwd = _hash_password(password)
        self.db.update_user(user.id, hashed_password=hashed_pwd,
                            reset_token=None)
