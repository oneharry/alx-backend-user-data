#!/usr/bin/env python3
""" Basic Authentication class """
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns bool"""
        slashed_path = path if path.endswith('/') else path + '/'
        if path is not None and slashed_path in excluded_paths:
            return False
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """ Returns base64 of auth headers"""
        header_auth = request.headers.get("Authorization")
        if header_auth is None or type(header_auth) is not str:
            return None
        if not header_auth.startswith("Basic"):
            return None
        return header_auth.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Returns the decoded value of base64"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            base = base64.b64.decode(base64_authorization_header)
            base_decode = base.decode('utf-8')
        except Exception:
            return None
        return base_decode
