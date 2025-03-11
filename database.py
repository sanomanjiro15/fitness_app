import json
import os
from datetime import datetime

# Define file paths for data storage
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
WORKOUTS_FILE = os.path.join(DATA_DIR, "workouts.json")

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)


# Initialize empty data files if they don't exist
def initialize_data_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)

    if not os.path.exists(WORKOUTS_FILE):
        with open(WORKOUTS_FILE, "w") as f:
            json.dump([], f)


initialize_data_files()


# Helper functions to read and write JSON data
def read_json_file(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Return empty list if file is empty or doesn't exist
        return []


def write_json_file(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    return True


def get_current_date():
    """Get current date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")


# User-related functions
def get_user_by_email(email):
    """Get user by email"""
    users = read_json_file(USERS_FILE)
    for user in users:
        if user["email"] == email:
            return user
    return None


def get_user_data(user_id):
    """Get user data by ID"""
    users = read_json_file(USERS_FILE)
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def create_user(user_data):
    """Create a new user"""
    users = read_json_file(USERS_FILE)
    users.append(user_data)
    return write_json_file(USERS_FILE, users)


def update_user_profile(user_id, height, weight):
    """Update user profile information"""
    users = read_json_file(USERS_FILE)

    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i]["height"] = height
            users[i]["weight"] = weight
            return write_json_file(USERS_FILE, users)

    return False


def update_last_login(user_id):
    """Update user's last login time"""
    users = read_json_file(USERS_FILE)

    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i]["last_login"] = get_current_date()
            return write_json_file(USERS_FILE, users)

    return False


# Workout-related functions
def save_workout(user_id, exercise_id, exercise_name, duration_minutes, calories_burned):
    """Save a completed workout"""
    workouts = read_json_file(WORKOUTS_FILE)

    workout_data = {
        "id": str(len(workouts) + 1),
        "user_id": user_id,
        "exercise_id": exercise_id,
        "exercise_name": exercise_name,
        "duration_minutes": round(duration_minutes, 2),
        "calories_burned": round(calories_burned, 2),
        "date": get_current_date()
    }

    workouts.append(workout_data)
    return write_json_file(WORKOUTS_FILE, workouts)


def get_workout_history(user_id):
    """Get workout history for a user"""
    workouts = read_json_file(WORKOUTS_FILE)
    return [workout for workout in workouts if workout["user_id"] == user_id]
