import streamlit as st
import re
from datetime import datetime


def is_valid_email(email):
    """Validate email format using regex"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def format_time(seconds):
    """Format seconds into mm:ss format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def calculate_bmi(height_cm, weight_kg):
    """Calculate BMI given height in cm and weight in kg"""
    if height_cm <= 0 or weight_kg <= 0:
        return 0

    height_m = height_cm / 100
    bmi = weight_kg / (height_m * height_m)
    return round(bmi, 1)


def get_bmi_category(bmi):
    """Get BMI category based on BMI value"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def apply_custom_css():
    """Apply custom CSS styling to the app"""
    st.markdown("""
    <style>
        /* Main theme colors - зеленая гамма */
        :root {
            --primary-color: #4CAF50;       /* Основной зеленый */
            --secondary-color: #2E7D32;     /* Темно-зеленый */
            --background-color: #f8fff8;    /* Светлый фон с зеленым оттенком */
            --text-color: #1a8f35;          /* Зеленый текст */
            --accent-color: #8BC34A;        /* Светло-зеленый акцент */
            --deep-green: #0e6c1e;          /* Насыщенный зеленый */
            --light-green: #e6ffe6;         /* Очень светлый зеленый */
        }

        /* Body styling */
        body {
            color: var(--text-color);
            background-color: var(--background-color);
            font-family: 'Roboto', sans-serif;
        }

        /* Улучшенная видимость текста на любом фоне */
        /* Заголовки с тенью для лучшей видимости и зеленым цветом */
        h1, h2, h3, h4, h5, h6 {
            color: #0e6c1e; /* Насыщенный зеленый для заголовков */
            font-weight: 700;
            text-shadow: 
                0px 1px 2px rgba(255, 255, 255, 0.9),
                0px -1px 1px rgba(0, 0, 0, 0.2);
            letter-spacing: 0.02em;
        }

        /* Основной текст с улучшенным контрастом и зеленым цветом */
        p, div, span, label {
            color: #1a8f35; /* Яркий зеленый цвет */
            text-shadow: 
                0px 1px 1px rgba(255, 255, 255, 0.7),
                0px -1px 1px rgba(0, 0, 0, 0.1);
            letter-spacing: 0.01em;
            font-weight: 500;
        }

        /* Информационные блоки с контрастным текстом */
        .stInfo, .stSuccess, .stWarning, .stError {
            text-shadow: none;
            font-weight: 500;
        }

        /* Текст на кнопках */
        .stButton button {
            text-shadow: 0px 1px 2px rgba(0, 0, 0, 0.2);
            font-weight: 600;
            letter-spacing: 0.03em;
        }

        /* Метрики с улучшенной видимостью */
        .st-emotion-cache-1wivap2 p, .st-ae label {
            text-shadow: 
                0px 1px 1px rgba(255, 255, 255, 0.8),
                0px -1px 1px rgba(0, 0, 0, 0.2);
            font-weight: 600;
        }

        /* Форма с зелеными элементами */
        form {
            border: 1px solid rgba(76, 175, 80, 0.3);
            padding: 20px;
            border-radius: 8px;
            background-color: rgba(240, 255, 240, 0.8); /* Очень светлый зеленый фон */
            box-shadow: 0 4px 8px rgba(76, 175, 80, 0.1);
        }

        /* Улучшенные стили для полей ввода с зеленым оформлением */
        input, .stTextInput input, .stNumberInput input {
            border: 1px solid rgba(76, 175, 80, 0.4) !important;
            background-color: rgba(245, 255, 245, 0.9) !important;
            color: #1a8f35 !important; /* Зеленый цвет для текста в полях ввода */
            font-weight: 500 !important;
            border-radius: 5px !important;
            padding: 8px 12px !important;
            box-shadow: 0 1px 3px rgba(76, 175, 80, 0.1) !important;
        }

        /* Фокус на полях ввода */
        input:focus, .stTextInput input:focus, .stNumberInput input:focus {
            border: 1px solid rgba(76, 175, 80, 0.7) !important;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
        }

        /* Стили для подсказок (помощь текстовым полям) */
        .stTextInput div[data-baseweb=form-control-message], 
        .stNumberInput div[data-baseweb=form-control-message] {
            color: #555555 !important;
            font-style: italic;
            font-weight: 400;
            margin-top: 3px;
        }

        /* Sidebar с зеленым оттенком */
        .css-1d391kg, .css-1544g2n {
            background-color: #f1f8f1 !important; /* Светло-зеленый фон */
            border-right: 1px solid rgba(76, 175, 80, 0.2);
        }

        /* Зеленые кнопки */
        .stButton button {
            border-radius: 20px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: 1px solid rgba(76, 175, 80, 0.2);
            background-color: rgba(240, 255, 240, 0.9);
            color: #1a8f35 !important;
            padding: 6px 16px;
        }

        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(76, 175, 80, 0.2);
            background-color: rgba(230, 255, 230, 1);
            border: 1px solid rgba(76, 175, 80, 0.4);
        }

        /* Primary buttons */
        .stButton button[data-baseweb="button"][kind="primary"] {
            background-color: var(--primary-color);
            color: white !important;
            border: 1px solid rgba(46, 125, 50, 0.3);
            font-weight: 700;
        }

        /* Primary buttons hover */
        .stButton button[data-baseweb="button"][kind="primary"]:hover {
            background-color: var(--secondary-color);
            box-shadow: 0 4px 8px rgba(46, 125, 50, 0.4);
        }

        /* Timer display с контрастным зеленым текстом */
        .timer-display {
            font-size: 48px;
            font-weight: 700;
            text-align: center;
            color: #0e8129; /* Яркий зеленый для таймера */
            text-shadow: 
                0px 2px 2px rgba(255, 255, 255, 0.8),
                0px -1px 1px rgba(0, 0, 0, 0.3);
            background-color: rgba(230, 255, 230, 0.6); /* Светло-зеленый фон */
            border: 2px solid rgba(26, 143, 53, 0.3); /* Тонкая зеленая рамка */
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
        }

        /* Progress indicators */
        .stProgress .css-1l269bu {
            background-color: var(--primary-color);
        }
    </style>
    """, unsafe_allow_html=True)