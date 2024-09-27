#!/usr/bin/env python3
"""
End-to-End Integration Test Script
"""
import requests


def register_user(email: str, password: str) -> None:
    """Test user registration"""
    # Attempt to create a new user
    response = requests.post(
        "http://0.0.0.0:5000/users",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200, "Failed to create new user"
    assert response.json() == {"email": email, "message": "user created"}

    # Try creating the user again to verify duplicate handling
    response = requests.post(
        "http://0.0.0.0:5000/users",
        data={"email": email, "password": password}
    )
    assert response.status_code == 400, "Duplicate user registration error"
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Verify login fails with incorrect password"""
    response = requests.post(
        "http://0.0.0.0:5000/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 401, "Expected 401 for wrong password"
    assert response.cookies.get("session_id") is None,
    "Session ID should not be set"


def log_in(email: str, password: str) -> str:
    """Attempt to log in with correct credentials and return session ID"""
    response = requests.post(
        "http://0.0.0.0:5000/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200, "Login failed with valid credentials"
    assert response.json() == {"email": email, "message": "logged in"}

    session_id = response.cookies.get("session_id")
    assert session_id, "No session ID found"
    return session_id


def profile_unlogged() -> None:
    """Access profile without being logged in"""
    response = requests.get("http://0.0.0.0:5000/profile")
    assert response.status_code == 403,
    "Expected 403 for unauthorized profile access"


def profile_logged(session_id: str) -> None:
    """Access profile while logged in"""
    response = requests.get(
        "http://0.0.0.0:5000/profile", cookies={"session_id": session_id}
    )
    assert response.status_code == 200,
    "Profile access failed for logged-in user"
    assert response.json() == {"email": EMAIL}, "Incorrect profile information"


def log_out(session_id: str) -> None:
    """Log out of the current session"""
    response = requests.delete(
        "http://0.0.0.0:5000/sessions", cookies={"session_id": session_id}
    )
    assert response.status_code == 200, "Logout failed"
    assert response.json() == {"message": "Bienvenue"},
    "Unexpected logout response"


def reset_password_token(email: str) -> str:
    """Request a reset password token"""
    response = requests.post(
        "http://0.0.0.0:5000/reset_password", data={"email": email}
    )
    assert response.status_code == 200, "Reset password token request failed"

    reset_token = response.json().get("reset_token")
    assert isinstance(reset_token, str), "Invalid reset token"
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update user password using the reset token"""
    response = requests.put(
        "http://0.0.0.0:5000/reset_password",
        data={"email": email, "new_password": new_password,
              "reset_token": reset_token},
    )
    assert response.status_code == 200, "Password update failed"
    assert response.json() == {"email": email, "message": "Password updated"}


# Configuration and testing variables
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
