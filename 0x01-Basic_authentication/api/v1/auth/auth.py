#!/usr/bin/env python3
""" Authentication class """
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns bool"""
        slashed_path = path if path.endswith('/') else path + '/'
        if path is not None and slashed_path in excluded_paths:
            return False
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

    def authorization_header(self, request=None) -> str:
        """ Returns header obj"""
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns user obj"""
        return request
