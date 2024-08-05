#!/usr/bin/env python3
""" Contains a class that manages API authentication """
from typing import List, TypeVar
from flask import request


class Auth:
    """ Manages API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """For now returns a False bool"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns a str"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Checks current user
        Args:
        request: Flask request object
        """
        return None
