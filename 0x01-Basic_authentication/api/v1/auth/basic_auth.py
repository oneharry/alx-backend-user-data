#!/usr/bin/env python3
""" Basic Authentication class """
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Auth class"""
    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Returns users credentials"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return decoded_base64_authorization_header.split(':', 1)

    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """ Returns base64 of auth headers"""
        header_auth = authorization_header
        if header_auth is None or type(header_auth) is not str:
            return None
        if not header_auth.startswith("Basic"):
            return None
        try:
            return header_auth.split(' ')[1]
        except Exception:
            return None

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Returns the decoded value of base64"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            base = base64.b64decode(base64_authorization_header)
            return base.decode('utf-8')
        except Exception:
            return None

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """ Returns user based on email and password"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves users instance of a request"""
        header_auth = self.authorization_header(header)
        if header_auth is None:
            return None
        ext_base = self.extract_base64_authorization_header(header_auth)
        decode_base = self.decode_base64_authorization_header(ext_base)
        user_cred = self.extract_user_credentials(decode_base)
        email = user_cred[0]
        pwd = user_cred[1]
        return self.user_object_from_credentials(email, pwd)
