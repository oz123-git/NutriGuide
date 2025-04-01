import streamlit as st
import json

# File to store user data
db_file = "user_data.json"

def load_user_data():
    try:
        with open(db_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(data):
    with open(db_file, "w") as file:
        json.dump(data, file, indent=4)

def register_page():
    st.markdown("<h1 style='color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_register.jpg.webp")
    name = st.text_input("Name")
    email = st.text_input("Email ID")
    phone = st.text_input("Phone Number")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type='password')

    if st.button("Register", key='register_button'):
        user_data = load_user_data()
        if new_username in user_data:
            st.error("Username already exists. Please choose another.")
        else:
            user_data[new_username] = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": new_password
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

def login_page():
    st.markdown("<h1 style='color: #2196F3;'>AI Nutrition Chatbot - Login</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_login.jpg.webp")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login", key='login_button'):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.success(f"Welcome back, {user_data[username]['name']}!")
            st.session_state['authenticated'] = True
        else:
            st.error("Invalid credentials. Please try again.")

    # Create account link at the bottom right
    st.markdown(
        "<p style='position: absolute; bottom: 20px; right: 20px;'><a href='#' style='color: #4CAF50;'>Create an Account</a></p>", 
        unsafe_allow_html=True
    )

def generate_seven_day_diet(diet_goal):
    # Separate meals into breakfast, lunch, and dinner for seven days based on diet goal
    daily_menus = {
        "Weight Loss": {
            "Day 1": {
                "Breakfast": "Poha with vegetables and green tea",
                "Lunch": "Dal khichdi with curd",
                "Dinner": "Vegetable soup"
            },
            "Day 2": {
                "Breakfast": "Oats porridge with nuts",
                "Lunch": "Paneer butter masala with naan",
                "Dinner": "Sprouts salad"
            },
            "Day 3": {
                "Breakfast": "Masala dosa with chutney",
                "Lunch": "Rajma chawal with salad",
                "Dinner": "Grilled fish with vegetables"
            },
            "Day 4": {
                "Breakfast": "Oats idli with chutney",
                "Lunch": "Chole bhature",
                "Dinner": "Fruit salad with yogurt"
            },
            "Day 5": {
                "Breakfast": "Pesarattu with chutney",
                "Lunch": "Paneer tikka with salad",
                "Dinner": "Vegetable biryani with raita"
            },
            "Day 6": {
                "Breakfast": "Moong dal chilla with mint chutney",
                "Lunch": "Aloo paratha with curd",
                "Dinner": "Lentil soup with bread"
            },
            "Day 7": {
                "Breakfast": "Dhokla with chutney",
                "Lunch": "Vegetable pulao with raita",
                "Dinner": "Grilled chicken with vegetables"
            }
        },
        # Other goals can be added similarly
    }

    # Show the diet plan based on the goal
    st.markdown(f"### 7-Day {diet_goal} Meal Plan (Breakfast, Lunch, and Dinner):")
    for day, meals in daily_menus[diet_goal].items():
        st.markdown(f"**{day}:**")
        st.markdown(f"  - **Breakfast:** {meals['Breakfast']}")
        st.markdown(f"  - **Lunch:** {meals['Lunch']}")
        st.markdown(f"  - **Dinner:** {meals['Dinner']}")
        st.markdown("---")
    
    st.markdown("### This meal plan repeats every week.")

def main_app():
    st.markdown("<h1 style='color: #FF5722;'>AI-Driven Personalized Nutrition</h1>", unsafe_allow_html=True)

    if st.button("Logout", key='logout_button'):
        st.session_state['authenticated'] = False
        st.success("You have been logged out.")
        return

    # Collect user details
    age = st.number_input("Enter your age", min_value=1)
    height = st.number_input("Enter your height (cm)", min_value=50)
    weight = st.number_input("Enter your weight (kg)", min_value=10)
    gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
    dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    diet_goal = st.selectbox("Diet Goal", ["Weight Loss", "Weight Gain", "Balanced Nutrition"])
    allergies = st.text_input("List any allergies (comma separated)")
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
    diet_duration = st.selectbox("Select Diet Duration", ["1 Week", "2 Weeks", "1 Month", "3 Months", "6 Months", "1 Year"])

    # Optional details
    sleep_hours = st.number_input("Sleep Hours per Day", min_value=0, max_value=24)
    water_intake = st.number_input("Water Intake (liters/day)", min_value=0.0)
    stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])

    # Show diet plan for 7 days
    if diet_duration == "1 Week":
        if st.button("Get 7-Day Nutrition Plan"):
            generate_seven_day_diet(diet_goal)

    st.write("---")
    st.markdown("<p style='color: #3F51B5;'><b>Project by TechSpark Group</b></p>", unsafe_allow_html=True)
    st.markdown("- Dipak Walunj\n- Divyank Wani\n- Omkar Zinjurde\n- Sakshi Ughade", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Amrutvahini College of Engineering, Sangamner</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Contact: techspark.support@gmail.com</p>", unsafe_allow_html=True)

# Ensure login page is displayed first by default
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Set the default page to "Login"
if st.session_state['authenticated']:
    main_app()
else:
    login_page()
