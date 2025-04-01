import streamlit as st
import json
import os

# File to store user data
db_file = os.path.join(os.getcwd(), "user_data.json")

def load_user_data():
    try:
        with open(db_file, "r") as file:
            data = file.read().strip()
            return json.loads(data) if data else {}
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
        if not name or not email or not phone or not new_username or not new_password:
            st.error("All fields are required!")
            return
        
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

def generate_seven_day_diet(diet_goal):
    # Define the meal plans with calories for different diet goals
    daily_menus = {
        "Weight Loss": {
            "Day 1": {
                "Breakfast": {"meal": "Poha with vegetables and green tea", "calories": 250},
                "Lunch": {"meal": "Dal khichdi with curd", "calories": 350},
                "Dinner": {"meal": "Vegetable soup", "calories": 150}
            },
            "Day 2": {
                "Breakfast": {"meal": "Oats with fruits and green tea", "calories": 200},
                "Lunch": {"meal": "Chickpea salad", "calories": 300},
                "Dinner": {"meal": "Soup with quinoa", "calories": 200}
            },
            # Add more days as needed...
        },
        "Balanced Nutrition": {
            "Day 1": {
                "Breakfast": {"meal": "Scrambled eggs with whole wheat toast", "calories": 350},
                "Lunch": {"meal": "Grilled chicken with quinoa and salad", "calories": 500},
                "Dinner": {"meal": "Baked salmon with vegetables", "calories": 400}
            },
            # Add more days as needed...
        },
        "Muscle Gain": {
            "Day 1": {
                "Breakfast": {"meal": "Eggs with avocado toast", "calories": 500},
                "Lunch": {"meal": "Chicken breast with brown rice", "calories": 600},
                "Dinner": {"meal": "Steak with sweet potatoes", "calories": 700}
            },
            # Add more days as needed...
        }
    }

    # Show the diet plan based on the goal
    st.markdown(f"### 7-Day {diet_goal} Meal Plan (Breakfast, Lunch, and Dinner):")
    for day, meals in daily_menus[diet_goal].items():
        st.markdown(f"**{day}:**")
        for meal_type, meal_info in meals.items():
            st.markdown(f"  - **{meal_type}:** {meal_info['meal']} (Calories: {meal_info['calories']})")
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
    health_goals = st.selectbox("Select Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])

    # Generate Diet Plan
    if st.button("Generate 7-Day Diet Plan", key='generate_button'):
        generate_seven_day_diet(health_goals)

    # Project Info
    st.write("---")
    st.markdown("<p style='color: #3F51B5;'><b>Project by TechSpark Group</b></p>", unsafe_allow_html=True)
    st.markdown("- Dipak Walunj\n- Divyank Wani\n- Omkar Zinjurde\n- Sakshi Ughade", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Amrutvahini College of Engineering, Sangamner</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Contact: techspark.support@gmail.com</p>", unsafe_allow_html=True)

    # Account creation button at the bottom-right
    st.markdown("""
        <style>
            .stButton > button {
                position: fixed;
                bottom: 10px;
                right: 10px;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)
    if st.button("Create Account"):
        register_page()

if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_page()
    else:
        main_app()

