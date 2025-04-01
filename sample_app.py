import streamlit as st
import json
import os

db_file = "user_data.json"

# Load existing user data
def load_user_data():
    if os.path.exists(db_file):
        try:
            with open(db_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.error("Error reading the user data. It may be corrupted.")
            return {}
    return {}

# Save user data
def save_user_data(data):
    with open(db_file, 'w') as f:
        json.dump(data, f)

# Update user data
def update_user_data(username, age, height, weight, gender, dietary_preference, health_goals):
    user_data = load_user_data()
    if username not in user_data:
        user_data[username] = {}
    
    user_data[username] = {
        "age": age,
        "height": height,
        "weight": weight,
        "gender": gender,
        "dietary_preference": dietary_preference,
        "health_goals": health_goals
    }
    save_user_data(user_data)

# Generate 7-day diet plan based on user health goal
def generate_seven_day_diet(diet_goal):
    diet_plans = {
        "Weight Loss": {
            "Day 1": "Oatmeal with nuts and fruits (Breakfast), Grilled chicken salad (Lunch), Steamed vegetables with brown rice (Dinner)",
            "Day 2": "Boiled eggs and toast (Breakfast), Quinoa and chickpea bowl (Lunch), Vegetable soup (Dinner)",
            "Day 3": "Greek yogurt with berries (Breakfast), Grilled salmon with veggies (Lunch), Rice and dal with salad (Dinner)",
            "Day 4": "Scrambled eggs with whole wheat bread (Breakfast), Paneer and roti (Lunch), Chicken curry with brown rice (Dinner)",
            "Day 5": "Fruits and nuts smoothie (Breakfast), Vegetable stir fry with tofu (Lunch), Protein smoothie with banana (Dinner)",
            "Day 6": "Rice and dal with salad (Breakfast), Grilled chicken with quinoa (Lunch), Lean beef with rice (Dinner)",
            "Day 7": "Peanut butter toast with milk (Breakfast), Grilled chicken salad (Lunch), Steamed vegetables with brown rice (Dinner)"
        },
        "Balanced Nutrition": {
            "Day 1": "Scrambled eggs with whole wheat bread (Breakfast), Grilled salmon with veggies (Lunch), Rice and dal with salad (Dinner)",
            "Day 2": "Fruits and nuts smoothie (Breakfast), Paneer and roti (Lunch), Vegetable stir fry with tofu (Dinner)",
            "Day 3": "Chicken curry with brown rice (Breakfast), Rice and dal with salad (Lunch), Grilled chicken with quinoa (Dinner)",
            "Day 4": "Grilled chicken with quinoa (Breakfast), Vegetable soup (Lunch), Scrambled eggs with whole wheat bread (Dinner)",
            "Day 5": "Greek yogurt with berries (Breakfast), Grilled salmon with veggies (Lunch), Quinoa and chickpea bowl (Dinner)",
            "Day 6": "Oatmeal with nuts and fruits (Breakfast), Boiled eggs and toast (Lunch), Chicken curry with brown rice (Dinner)",
            "Day 7": "Rice and dal with salad (Breakfast), Lean beef with rice (Lunch), Vegetable stir fry with tofu (Dinner)"
        },
        "Muscle Gain": {
            "Day 1": "Protein smoothie with banana (Breakfast), Grilled chicken with quinoa (Lunch), Cottage cheese and nuts (Dinner)",
            "Day 2": "Egg omelette with toast (Breakfast), Fish with sweet potatoes (Lunch), Lean beef with rice (Dinner)",
            "Day 3": "Peanut butter toast with milk (Breakfast), Grilled chicken with quinoa (Lunch), Egg omelette with toast (Dinner)",
            "Day 4": "Protein smoothie with banana (Breakfast), Grilled chicken with quinoa (Lunch), Cottage cheese and nuts (Dinner)",
            "Day 5": "Lean beef with rice (Breakfast), Peanut butter toast with milk (Lunch), Grilled chicken with quinoa (Dinner)",
            "Day 6": "Egg omelette with toast (Breakfast), Fish with sweet potatoes (Lunch), Protein smoothie with banana (Dinner)",
            "Day 7": "Grilled chicken with quinoa (Breakfast), Cottage cheese and nuts (Lunch), Peanut butter toast with milk (Dinner)"
        }
    }
    
    st.subheader(f"7-Day {diet_goal} Diet Plan")
    for day, meals in diet_plans[diet_goal].items():
        st.write(f"**{day}:** {meals}")

# Register new user
def register_page():
    st.title("Registration")
    
    username = st.text_input("Enter a username")
    password = st.text_input("Enter a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    
    if password != confirm_password:
        st.error("Passwords do not match!")
        return
    
    if st.button("Register"):
        user_data = load_user_data()
        
        if username in user_data:
            st.warning("Username already exists.")
        else:
            user_data[username] = {"password": password}
            save_user_data(user_data)
            st.success("Registration successful! You can now login.")

# Login page logic with registration option
def login_page():
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user_data = load_user_data()
        
        if username in user_data and "password" in user_data[username] and user_data[username]["password"] == password:
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid username or password.")
            return False
    
    # Add option to go to registration page
    if st.button("Don't have an account? Register here"):
        register_page()
        return False

def main_app():
    st.markdown("<h1 style='color: #FF5722;'>AI-Driven Personalized Nutrition</h1>", unsafe_allow_html=True)
    
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.warning("Please login to access the app.")
        if login_page():
            return

    username = st.session_state.get('username')
    if not username:
        st.error("Username not found in session.")
        return
    
    st.success(f"Welcome back, {username}!")
    user_data = load_user_data()
    user = user_data.get(username, {})
    
    if not user.get("age"):
        st.subheader("Enter Your Details")
        age = st.number_input("Enter your age", min_value=1)
        height = st.number_input("Enter your height (cm)", min_value=50)
        weight = st.number_input("Enter your weight (kg)", min_value=10)
        gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
        dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        health_goals = st.selectbox("Select Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])
        
        if st.button("Save Details"):
            update_user_data(username, age, height, weight, gender, dietary_preference, health_goals)
            st.success("Your details have been saved successfully!")
    else:
        st.subheader("Your Last Diet Plan")
        if user.get("health_goals"):
            generate_seven_day_diet(user["health_goals"])
        else:
            st.warning("No diet plan found. Please update your details.")
    
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.success("You have been logged out.")
        return

if __name__ == '__main__':
    main_app()
