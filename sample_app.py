import streamlit as st
import json
import random

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
    st.title("🍽️ Create an Account")
    name = st.text_input("Name")
    email = st.text_input("Email ID")
    phone = st.text_input("Phone Number")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type='password')

    if st.button("Register"):
        user_data = load_user_data()
        if new_username in user_data:
            st.error("❌ Username already exists. Please choose another.")
        else:
            user_data[new_username] = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": new_password
            }
            save_user_data(user_data)
            st.success("✅ Account created successfully! Please login.")

def login_page():
    st.title("🔒 AI Nutrition Chatbot - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.success(f"🎉 Welcome back, {user_data[username]['name']}!")
            st.session_state['authenticated'] = True
        else:
            st.error("❌ Invalid credentials. Please try again.")

def generate_meal_plan():
    meal_options = [
        ["🥣 Oats + Fruits", "🍗 Grilled Chicken + Salad", "🥗 Veg Curry + Brown Rice"],
        ["🥗 Poha + Sprouts", "🧀 Paneer + Roti", "🍚 Quinoa + Veg Curry"],
        ["🥞 Idli + Sambar", "🐟 Fish Curry + Rice", "🥣 Soup + Bread"],
        ["🥐 Paratha + Curd", "🍳 Egg Curry + Rice", "🥘 Dal + Roti"],
        ["🍓 Smoothie Bowl", "🥦 Vegetable Stir Fry", "🌯 Chicken Wrap"]
    ]
    return random.choice(meal_options)

def main_app():
    st.title("🥗 AI-Driven Personalized Nutrition Chatbot")

    # Collect user details
    age = st.number_input("Enter your age", min_value=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Enter your height (cm)", min_value=50)
    weight = st.number_input("Enter your weight (kg)", min_value=10)
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
    health_goal = st.selectbox("Health Goal", ["Weight Loss", "Muscle Gain", "Balanced Diet", "Improved Immunity"])
    dietary_pref = st.selectbox("Dietary Preference", ["Vegetarian", "Vegan", "Non-Vegetarian"])
    medical_conditions = st.text_input("Medical Conditions (if any)")
    allergies = st.text_input("Allergies (if any)")
    eating_schedule = st.text_input("Eating Schedule (e.g., 3 meals/day)")
    diet_duration = st.selectbox("Select Diet Duration", ["1 Week", "2 Weeks", "1 Month"])

    if st.button("Get Nutrition Plan"):
        st.success("Here’s your personalized nutrition plan:")
        st.write(f"✅ Age: {age} years")
        st.write(f"✅ Gender: {gender}")
        st.write(f"✅ Height: {height} cm")
        st.write(f"✅ Weight: {weight} kg")
        st.write(f"✅ Activity Level: {activity_level}")
        st.write(f"✅ Health Goal: {health_goal}")
        st.write(f"✅ Dietary Preference: {dietary_pref}")
        st.write(f"📅 Diet Duration: {diet_duration}")

        # Sample meal plan with variety
        st.write("### Sample Diet Plan")
        for day in range(1, 8):
            meal_plan = generate_meal_plan()
            st.write(f"**Day {day}**")
            st.write(f"Breakfast: {meal_plan[0]}")
            st.write(f"Lunch: {meal_plan[1]}")
            st.write(f"Dinner: {meal_plan[2]}")

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

page = st.sidebar.selectbox("Select Page", ["Register", "Login", "Main App"])

if page == "Register":
    register_page()
elif page == "Login":
    if st.session_state['authenticated']:
        main_app()
    else:
        login_page()
else:
    if st.session_state['authenticated']:
        main_app()
    else:
        st.warning("⚠️ Please login first.")

# Group Members
st.sidebar.markdown("### Developed by TechSpark Team:")
st.sidebar.markdown("- Dipak Walunj")
st.sidebar.markdown("- Divyank Wani")
st.sidebar.markdown("- Omkar Zinjurde")
st.sidebar.markdown("- Sakshi Ugade")
