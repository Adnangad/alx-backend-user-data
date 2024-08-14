#!/usr/bin/env python3
"""Ganerates a hashed password"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Returns a hashed password"""
    password = bytes(password, 'utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """Generates a string from uuid module"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a user to the db"""
        try:
            present = self._db.find_user_by(email=email)
            if present:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hash_pas = _hash_password(password)
            added_user = self._db.add_user(
                email=email, hashed_password=hash_pas)
            return added_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a users password during login"""
        try:
            present = self._db.find_user_by(email=email)
            if not isinstance(password, bytes):
                password = bytes(password, 'utf-8')
            if present:
                if bcrypt.checkpw(password, present.hashed_password):
                    return True
                else:
                    return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a users session id and returns it"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns a user based on session_id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a users session_id by setting it to none"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except ValueError:
            raise ValueError('Cannot destroy')

    def get_reset_password_token(self, email: str) -> str:
        """Returns a users reset_token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a users password using the reset_token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            password = _hash_password(password)
            self._db.update_user(
                user.id, reset_token=None, hashed_password=password)
            return None
        except NoResultFound:
            raise ValueError
