import hashlib
import uuid
import database
import streamlit as st


def hash_password(password):
    """Hash a password with SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(email, password, height, weight):
    """Register a new user and return user_id if successful"""
    # Check if user already exists
    existing_user = database.get_user_by_email(email)
    if existing_user:
        return None

    # Hash password
    hashed_password = hash_password(password)

    # Create new user ID
    user_id = str(uuid.uuid4())

    # Create user in database
    user_data = {
        "id": user_id,
        "email": email,
        "password": hashed_password,
        "height": height,
        "weight": weight,
        "created_at": database.get_current_date(),
        "last_login": database.get_current_date()
    }

    success = database.create_user(user_data)
    if success:
        return user_id
    return None


def login_user(email, password):
    """Authenticate user and return user_id if successful"""
    # Get user from database
    user = database.get_user_by_email(email)
    if not user:
        return None

    # Check password
    hashed_password = hash_password(password)
    if hashed_password != user["password"]:
        return None

    # Update last login time
    database.update_last_login(user["id"])

    return user["id"]


def logout():
    """Clear session state to log out user"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]