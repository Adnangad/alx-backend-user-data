#!/usr/bin/env python3
"""Ganerates a hashed password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Returns a hashed password"""
    password = bytes(password, 'utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password
