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
