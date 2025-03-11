def get_app_logo():
    """Return a SVG logo for the fitness tracker app"""
    return """
    <div style="text-align: center;">
        <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" rx="20" fill="#4CAF50"/>
            <path d="M30 50C30 38.9543 38.9543 30 50 30C61.0457 30 70 38.9543 70 50C70 61.0457 61.0457 70 50 70C38.9543 70 30 61.0457 30 50Z" fill="white"/>
            <path d="M50 35V50H65" stroke="#4CAF50" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M25 25L30 30" stroke="white" stroke-width="4" stroke-linecap="round"/>
            <path d="M75 25L70 30" stroke="white" stroke-width="4" stroke-linecap="round"/>
            <path d="M25 75L30 70" stroke="white" stroke-width="4" stroke-linecap="round"/>
            <path d="M75 75L70 70" stroke="white" stroke-width="4" stroke-linecap="round"/>
        </svg>
    </div>
    """

def get_timer_icon():
    """Return a SVG icon for timer functionality"""
    return """
    <div>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="#4CAF50" stroke-width="2"/>
            <path d="M12 6V12L16 14" stroke="#4CAF50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    """

def get_calories_icon():
    """Return a SVG icon for calories tracking"""
    return """
    <div>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM17 13H13V17H11V13H7V11H11V7H13V11H17V13Z" fill="#FF9800"/>
        </svg>
    </div>
    """

def get_exercise_icon():
    """Return a SVG icon for exercise"""
    return """
    <div>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20.57 14.86L22 13.43L20.57 12L17 15.57L8.43 7L12 3.43L10.57 2L9.14 3.43L7.71 2L5.57 4.14L4.14 2.71L2.71 4.14L4.14 5.57L2 7.71L3.43 9.14L2 10.57L3.43 12L7 8.43L15.57 17L12 20.57L13.43 22L14.86 20.57L16.29 22L18.43 19.86L19.86 21.29L21.29 19.86L19.86 18.43L22 16.29L20.57 14.86Z" fill="#4CAF50"/>
        </svg>
    </div>
    """

def get_profile_icon():
    """Return a SVG icon for user profile"""
    return """
    <div>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z" fill="#2E7D32"/>
        </svg>
    </div>
    """