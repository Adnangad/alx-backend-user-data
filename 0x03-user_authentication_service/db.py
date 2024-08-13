#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """Adds a user to the db and returns an instance
        of the user"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self.__session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by input"""
        keyz = ['id',
                'email',
                'hashed_password',
                'session_id', 'reset_token']
        for key in kwargs.keys():
            if key not in keyz:
                raise InvalidRequestError
        rez = self._session.query(User).filter_by(**kwargs).first()
        if rez is None:
            raise NoResultFound
        return rez

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a users attribute"""
        user = self.find_user_by(id=user_id)
        keyz = ['id',
                'email',
                'hashed_password',
                'session_id', 'reset_token']
        for key, val in kwargs.items():
            if key not in keyz:
                raise ValueError
            setattr(user, key, val)
            self._session.commit()
