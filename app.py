import streamlit as st
import pandas as pd
import time
from datetime import datetime
import os

import auth
import database
import exercises
import stats
import utils
from assets import icons

# Page configuration
st.set_page_config(
    page_title="FitnessTracker",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
utils.apply_custom_css()

# Initialize session state variables if they don't exist
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "exercise_timer_active" not in st.session_state:
    st.session_state.exercise_timer_active = False
if "timer_start_time" not in st.session_state:
    st.session_state.timer_start_time = None
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0
if "current_exercise" not in st.session_state:
    st.session_state.current_exercise = None


# Function to navigate between pages
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()


# Sidebar menu
def render_sidebar():
    with st.sidebar:
        st.markdown(icons.get_app_logo(), unsafe_allow_html=True)
        st.title("FitnessTracker")

        if st.session_state.user_id:
            user_data = database.get_user_data(st.session_state.user_id)
            st.write(f"Welcome, {user_data['email'].split('@')[0]}!")

            # Navigation menu
            st.subheader("Navigation")
            if st.button("📊 Dashboard", use_container_width=True):
                navigate_to("dashboard")
            if st.button("🏋️ Start Workout", use_container_width=True):
                navigate_to("exercise_selection")
            if st.button("📚 Exercise Library", use_container_width=True):
                navigate_to("exercise_library")
            if st.button("👤 Profile", use_container_width=True):
                navigate_to("profile")

            # Logout button
            if st.button("Logout", type="primary", use_container_width=True):
                auth.logout()
                navigate_to("login")
        else:
            # Login/Register buttons for unauthenticated users
            st.button("Login", key="sidebar_login", on_click=lambda: navigate_to("login"))
            st.button("Register", key="sidebar_register", on_click=lambda: navigate_to("register"))


# Main content area
def render_main_content():
    if st.session_state.current_page == "login":
        render_login_page()
    elif st.session_state.current_page == "register":
        render_register_page()
    elif st.session_state.user_id is None:
        # Redirect to login if trying to access protected pages without authentication
        navigate_to("login")
    elif st.session_state.current_page == "dashboard":
        render_dashboard()
    elif st.session_state.current_page == "exercise_selection":
        render_exercise_selection()
    elif st.session_state.current_page == "exercise_timer":
        render_exercise_timer()
    elif st.session_state.current_page == "exercise_library":
        render_exercise_library()
    elif st.session_state.current_page == "exercise_details":
        render_exercise_details()
    elif st.session_state.current_page == "profile":
        render_profile_page()
    else:
        st.error("Page not found!")


def render_login_page():
    st.title("Вход в FitnessTracker")

    # Login instructions
    st.info("Введите ваш email и пароль для входа в систему")

    with st.form("login_form"):
        # Email field with placeholder
        email = st.text_input(
            "Электронная почта (Email)",
            placeholder="example@mail.com",
            help="Введите адрес электронной почты, указанный при регистрации"
        )

        # Password field with help text
        password = st.text_input(
            "Пароль",
            type="password",
            help="Введите ваш пароль"
        )

        # Login button
        submitted = st.form_submit_button("Войти")

        if submitted:
            user_id = auth.login_user(email, password)
            if user_id:
                st.session_state.user_id = user_id
                st.success("Вход выполнен успешно!")
                navigate_to("dashboard")
            else:
                st.error("Неверный email или пароль")

    st.write("Нет учетной записи?")
    if st.button("Зарегистрироваться"):
        navigate_to("register")


def render_register_page():
    st.title("Создание учетной записи FitnessTracker")

    # Instructions for registration
    st.info("Пожалуйста, заполните все поля ниже для создания учетной записи")

    with st.form("register_form"):
        # Email with placeholder and help text
        email = st.text_input(
            "Электронная почта (Email)",
            placeholder="example@mail.com",
            help="Введите действующий адрес электронной почты"
        )

        # Password with help text
        password = st.text_input(
            "Пароль",
            type="password",
            help="Придумайте надежный пароль для вашей учетной записи"
        )

        # Confirm password with help text
        confirm_password = st.text_input(
            "Подтверждение пароля",
            type="password",
            help="Повторите введенный выше пароль"
        )

        st.write("### Физические параметры")
        st.caption("Эти данные используются для расчета калорий и BMI")

        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input(
                "Рост (см)",
                min_value=100,
                max_value=250,
                step=1,
                help="Введите ваш рост в сантиметрах"
            )
        with col2:
            weight = st.number_input(
                "Вес (кг)",
                min_value=30,
                max_value=300,
                step=1,
                help="Введите ваш вес в килограммах"
            )

        submitted = st.form_submit_button("Зарегистрироваться")

        if submitted:
            if password != confirm_password:
                st.error("Пароли не совпадают")
            elif not utils.is_valid_email(email):
                st.error("Пожалуйста, введите корректный email адрес")
            else:
                user_id = auth.register_user(email, password, height, weight)
                if user_id:
                    st.session_state.user_id = user_id
                    st.success("Регистрация успешно завершена!")
                    navigate_to("dashboard")
                else:
                    st.error("Этот email уже зарегистрирован")

    st.write("Уже есть учетная запись?")
    if st.button("Войти"):
        navigate_to("login")


def render_dashboard():
    st.title("Fitness Dashboard")

    # Get user data and workout history
    user_data = database.get_user_data(st.session_state.user_id)
    workout_history = database.get_workout_history(st.session_state.user_id)

    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Workouts", len(workout_history))
    with col2:
        total_minutes = sum([w["duration_minutes"] for w in workout_history])
        st.metric("Total Time", f"{total_minutes} min")
    with col3:
        total_calories = sum([w["calories_burned"] for w in workout_history])
        st.metric("Total Calories", f"{total_calories} kcal")
    with col4:
        if workout_history:
            last_workout = max([datetime.strptime(w["date"], "%Y-%m-%d") for w in workout_history])
            last_workout_str = last_workout.strftime("%d %b %Y")
        else:
            last_workout_str = "No workouts yet"
        st.metric("Last Workout", last_workout_str)

    # Recent workouts
    st.subheader("Recent Workouts")
    if not workout_history:
        st.info("No workout data yet. Start your first workout!")
        if st.button("Start a workout now"):
            navigate_to("exercise_selection")
    else:
        # Display recent workouts table
        recent_workouts = sorted(workout_history, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)[
                          :5]
        workout_df = pd.DataFrame(recent_workouts)
        st.dataframe(
            workout_df[["date", "exercise_name", "duration_minutes", "calories_burned"]]
            .rename(columns={
                "date": "Date",
                "exercise_name": "Exercise",
                "duration_minutes": "Duration (min)",
                "calories_burned": "Calories Burned"
            }),
            hide_index=True,
            use_container_width=True
        )

    # Progress visualization
    if workout_history:
        st.subheader("Your Progress")
        stats.show_workout_charts(workout_history)

    # Quick start
    st.subheader("Quick Start")
    if st.button("Start New Workout", type="primary", use_container_width=True):
        navigate_to("exercise_selection")


def render_exercise_selection():
    st.title("Choose an Exercise")

    # Get all available exercises
    exercise_list = exercises.get_all_exercises()

    # Create a grid layout for exercise selection
    col1, col2, col3 = st.columns(3)

    for i, exercise in enumerate(exercise_list):
        # Distribute exercises across columns
        col = [col1, col2, col3][i % 3]

        with col:
            st.write(f"### {exercise['name']}")
            st.write(f"{exercise['short_description']}")
            st.write(f"Difficulty: {exercise['difficulty']}")
            st.write(f"Calories: ~{exercise['calories_per_minute']}/min")

            if st.button(f"Start {exercise['name']}", key=f"btn_{exercise['id']}"):
                st.session_state.current_exercise = exercise
                navigate_to("exercise_timer")

            if st.button(f"View Details", key=f"details_{exercise['id']}"):
                st.session_state.current_exercise = exercise
                navigate_to("exercise_details")

            st.write("---")


def render_exercise_timer():
    if not st.session_state.current_exercise:
        st.error("No exercise selected!")
        if st.button("Select an exercise"):
            navigate_to("exercise_selection")
        return

    exercise = st.session_state.current_exercise
    st.title(f"Timer: {exercise['name']}")

    # Display exercise info
    st.write(exercise['short_description'])

    # Timer controls
    col1, col2 = st.columns([3, 1])

    with col1:
        # Initialize timer if not already running
        if not st.session_state.exercise_timer_active:
            if st.button("Start Exercise", type="primary", use_container_width=True):
                st.session_state.exercise_timer_active = True
                st.session_state.timer_start_time = time.time()
                st.session_state.elapsed_time = 0
                st.rerun()
        else:
            # Update timer
            current_time = time.time()
            st.session_state.elapsed_time = current_time - st.session_state.timer_start_time

            # Display timer
            minutes = int(st.session_state.elapsed_time // 60)
            seconds = int(st.session_state.elapsed_time % 60)
            st.markdown(f"<h1 style='text-align: center;'>{minutes:02d}:{seconds:02d}</h1>", unsafe_allow_html=True)

            # Stop button
            if st.button("Complete Exercise", type="primary", use_container_width=True):
                # Calculate statistics
                duration_minutes = st.session_state.elapsed_time / 60
                calories_burned = exercise['calories_per_minute'] * duration_minutes

                # Save workout
                database.save_workout(
                    st.session_state.user_id,
                    exercise['id'],
                    exercise['name'],
                    duration_minutes,
                    calories_burned
                )

                # Reset timer
                st.session_state.exercise_timer_active = False
                st.session_state.timer_start_time = None
                st.session_state.elapsed_time = 0

                st.success(f"Workout completed! You burned approximately {int(calories_burned)} calories.")
                time.sleep(2)
                navigate_to("dashboard")

    with col2:
        # Display estimated calories in real-time if timer is active
        if st.session_state.exercise_timer_active:
            calories = exercise['calories_per_minute'] * (st.session_state.elapsed_time / 60)
            st.metric("Calories", f"{int(calories)} kcal")

    # Display exercise instructions
    st.subheader("Instructions")
    for i, step in enumerate(exercise['instructions']):
        st.write(f"{i + 1}. {step}")

    # Cancel button
    if st.button("Cancel Exercise"):
        st.session_state.exercise_timer_active = False
        st.session_state.timer_start_time = None
        st.session_state.elapsed_time = 0
        navigate_to("exercise_selection")


def render_exercise_library():
    st.title("Exercise Library")

    # Get all available exercises
    exercise_list = exercises.get_all_exercises()

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        difficulty_filter = st.multiselect(
            "Difficulty Level",
            options=["Beginner", "Intermediate", "Advanced"],
            default=[]
        )
    with col2:
        search_term = st.text_input("Search Exercise", "")

    # Apply filters
    filtered_exercises = exercise_list
    if difficulty_filter:
        filtered_exercises = [ex for ex in filtered_exercises if ex['difficulty'] in difficulty_filter]
    if search_term:
        filtered_exercises = [ex for ex in filtered_exercises if search_term.lower() in ex['name'].lower()]

    # Display exercises
    if not filtered_exercises:
        st.info("No exercises match your filters")
    else:
        for exercise in filtered_exercises:
            with st.expander(f"{exercise['name']} - {exercise['difficulty']}"):
                st.write(exercise['short_description'])
                st.write(f"Calories: ~{exercise['calories_per_minute']}/min")

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(f"Start {exercise['name']}", key=f"start_{exercise['id']}"):
                        st.session_state.current_exercise = exercise
                        navigate_to("exercise_timer")
                with col2:
                    if st.button(f"View Details", key=f"view_{exercise['id']}"):
                        st.session_state.current_exercise = exercise
                        navigate_to("exercise_details")


def render_exercise_details():
    if not st.session_state.current_exercise:
        st.error("No exercise selected!")
        if st.button("Back to Exercise Library"):
            navigate_to("exercise_library")
        return

    exercise = st.session_state.current_exercise

    st.title(exercise['name'])
    st.write(f"**Difficulty:** {exercise['difficulty']}")
    st.write(f"**Calories:** ~{exercise['calories_per_minute']} kcal/min")

    st.write(exercise['description'])

    # Display instructions with exercise image
    st.subheader("How to perform this exercise")

    col1, col2 = st.columns([1, 1])

    with col1:
        # Display exercise image
        st.image(exercise['image_url'], use_column_width=True)

    with col2:
        # Display numbered instructions
        for i, instruction in enumerate(exercise['instructions']):
            st.write(f"{i + 1}. {instruction}")

    # Display muscles worked section
    st.subheader("Muscles Worked")
    st.write(exercise['muscles_worked'])

    # Benefits section
    st.subheader("Benefits")
    for benefit in exercise['benefits']:
        st.write(f"• {benefit}")

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Exercise", type="primary", use_container_width=True):
            navigate_to("exercise_timer")
    with col2:
        if st.button("Back to Library", use_container_width=True):
            navigate_to("exercise_library")


def render_profile_page():
    st.title("Your Profile")

    user_data = database.get_user_data(st.session_state.user_id)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Personal Information")
        with st.form("profile_form"):
            email = st.text_input("Email", value=user_data['email'], disabled=True)
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=user_data['height'])
            weight = st.number_input("Weight (kg)", min_value=30, max_value=300, value=user_data['weight'])

            submitted = st.form_submit_button("Update Profile")

            if submitted:
                success = database.update_user_profile(st.session_state.user_id, height, weight)
                if success:
                    st.success("Profile updated successfully!")
                else:
                    st.error("An error occurred while updating your profile")

    with col2:
        st.subheader("Workout Statistics")
        workout_history = database.get_workout_history(st.session_state.user_id)

        if not workout_history:
            st.info("No workout data yet. Start your first workout!")
        else:
            total_workouts = len(workout_history)
            total_minutes = sum([w["duration_minutes"] for w in workout_history])
            total_calories = sum([w["calories_burned"] for w in workout_history])

            st.metric("Total Workouts", total_workouts)
            st.metric("Total Time", f"{int(total_minutes)} min")
            st.metric("Total Calories Burned", f"{int(total_calories)} kcal")

            # Calculate BMI
            bmi = user_data['weight'] / ((user_data['height'] / 100) ** 2)
            st.metric("BMI", f"{bmi:.1f}")

            # Show BMI classification
            if bmi < 18.5:
                st.info("BMI Classification: Underweight")
            elif bmi < 25:
                st.success("BMI Classification: Normal weight")
            elif bmi < 30:
                st.warning("BMI Classification: Overweight")
            else:
                st.error("BMI Classification: Obese")


# Main app execution
def main():
    render_sidebar()
    render_main_content()

    # Auto-update timer if active
    if st.session_state.exercise_timer_active and st.session_state.current_page == "exercise_timer":
        time.sleep(1)
        st.rerun()


if __name__ == "__main__":
    main()