#!/usr/bin/env python3
""" Contains a class that manages API authentication """
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """ Manages API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """For now returns a False bool"""
        if path is None:
            return True
        if not path.endswith('/'):
            path = path + '/'
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for x in excluded_paths:
            if x[-1] != '/':
                x += '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Returns a str"""
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Checks current user
        Args:
        request: Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from request"""
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
