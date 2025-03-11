from assets.exercises import EXERCISE_DATA


def get_all_exercises():
    """Return a list of all available exercises"""
    return EXERCISE_DATA


def get_exercise_by_id(exercise_id):
    """Get an exercise by its ID"""
    for exercise in EXERCISE_DATA:
        if exercise["id"] == exercise_id:
            return exercise
    return None


def get_exercises_by_difficulty(difficulty):
    """Get exercises filtered by difficulty level"""
    return [ex for ex in EXERCISE_DATA if ex["difficulty"] == difficulty]


def calculate_calories_burned(exercise_id, duration_minutes, weight_kg):
    """Calculate calories burned for a specific exercise"""
    exercise = get_exercise_by_id(exercise_id)
    if not exercise:
        return 0

    # Base calories burned per minute for the exercise
    base_calories = exercise["calories_per_minute"]

    # Adjust calories based on user weight (simplified formula)
    weight_factor = weight_kg / 70.0  # Normalize around 70kg reference weight

    return base_calories * duration_minutes * weight_factor