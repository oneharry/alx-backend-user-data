#!/usr/bin/env python3
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash the password"""
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd
