#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require_auth method
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        path = path.rstrip("/") + "/"
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.split("*")[0]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization_header method
        """
        if request is None:
            return request
        if "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar("User"):
        """
        current_user method
        """
        return None
