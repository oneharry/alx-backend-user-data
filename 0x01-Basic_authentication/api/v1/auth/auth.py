#!/usr/bin/env python3
""" Authentication class """
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns bool"""
        slashed_path = path if path.endswith('/') else path + '/'
        if path is None:
            return None
        if slashed_path in excluded_paths:
            return False
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

    def authorization_header(self, request=None) -> str:
        """ Returns header obj"""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns user obj"""
        return None
