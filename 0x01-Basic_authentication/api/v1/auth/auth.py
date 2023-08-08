#!/usr/bin/env python3
""" Authentication class """
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns bool"""
        if path is None excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path if path.endswith('/') else path + '/'

        for pa in excluded_paths:
            if pa.endswith('*'):
                temp = path[:-1]
                if path.startswith(temp):
                    return False
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns header obj"""
        if request is None or "Authorization" not in request.headers:
            return None
        header = request.headers.get("Authorization")
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns user obj"""
        return None
