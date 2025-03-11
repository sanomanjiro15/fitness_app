import streamlit as st
import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go
from datetime import datetime, timedelta


def show_workout_charts(workout_history):
    """Display visualizations of workout data"""
    if not workout_history:
        st.info("No workout data to display")
        return

    # Convert to DataFrame
    df = pd.DataFrame(workout_history)

    # Convert date strings to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # Sort by date
    df = df.sort_values('date')

    # Calculate daily totals
    daily_totals = df.groupby('date').agg({
        'duration_minutes': 'sum',
        'calories_burned': 'sum',
        'exercise_name': 'count'
    }).reset_index()
    daily_totals = daily_totals.rename(columns={'exercise_name': 'exercise_count'})

    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Calories Burned", "Workout Duration", "Exercise Distribution"])

    with tab1:
        # Create calories burned trend chart
        fig = px.line(
            daily_totals,
            x='date',
            y='calories_burned',
            markers=True,
            title='Calories Burned Over Time',
            labels={'date': 'Date', 'calories_burned': 'Calories Burned (kcal)'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Create workout duration trend chart
        fig = px.bar(
            daily_totals,
            x='date',
            y='duration_minutes',
            title='Workout Duration Over Time',
            labels={'date': 'Date', 'duration_minutes': 'Duration (minutes)'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Create pie chart of exercise distribution
        exercise_counts = df['exercise_name'].value_counts().reset_index()
        exercise_counts.columns = ['Exercise', 'Count']

        fig = px.pie(
            exercise_counts,
            values='Count',
            names='Exercise',
            title='Exercise Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Weekly summary
    st.subheader("Weekly Summary")

    # Create a date range covering the last 7 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    date_range = pd.date_range(start=start_date, end=end_date)

    # Filter data for last 7 days
    last_week_df = df[df['date'] >= pd.Timestamp(start_date)]

    # Calculate weekly totals
    weekly_calories = last_week_df['calories_burned'].sum()
    weekly_duration = last_week_df['duration_minutes'].sum()
    weekly_workouts = len(last_week_df)

    # Display weekly metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Weekly Calories", f"{int(weekly_calories)} kcal")
    with col2:
        st.metric("Weekly Duration", f"{int(weekly_duration)} min")
    with col3:
        st.metric("Weekly Workouts", weekly_workouts)

    # Display daily activity as a heatmap
    daily_activity = pd.DataFrame({'date': date_range})
    daily_activity['date_str'] = daily_activity['date'].dt.strftime('%Y-%m-%d')

    # Count workouts per day in the last week
    workout_counts = last_week_df.groupby(last_week_df['date'].dt.strftime('%Y-%m-%d')).size().reset_index()
    workout_counts.columns = ['date_str', 'count']

    # Merge with full date range
    daily_activity = daily_activity.merge(workout_counts, on='date_str', how='left')
    daily_activity['count'] = daily_activity['count'].fillna(0)
    daily_activity['day'] = daily_activity['date'].dt.strftime('%a')

    st.write("Daily Activity:")

    # Create a simple text-based activity visualization
    for _, row in daily_activity.iterrows():
        day = row['day']
        count = int(row['count'])
        activity_bar = "🔥" * count if count > 0 else "❌"
        st.write(f"{day}: {activity_bar} ({count} workouts)")