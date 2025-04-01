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
                "password": new_password,
                "age": None,
                "height": None,
                "weight": None,
                "gender": None,
                "dietary_preference": None,
                "health_goals": None
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

def login_page():
    st.markdown("<h1 style='color: #2196F3;'>AI Nutrition - Login</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_login.jpg.webp")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login", key='login_button'):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.success(f"Welcome back, {user_data[username]['name']}!")
            st.session_state['authenticated'] = True
            st.session_state['username'] = username  # Store username in session state
        else:
            st.error("Invalid credentials. Please try again.")

def update_user_data(username, age, height, weight, gender, dietary_preference, health_goals):
    user_data = load_user_data()
    if username in user_data:
        user_data[username].update({
            "age": age,
            "height": height,
            "weight": weight,
            "gender": gender,
            "dietary_preference": dietary_preference,
            "health_goals": health_goals
        })
        save_user_data(user_data)

def generate_seven_day_diet(diet_goal):
    # Your existing code for generating the diet plan...
    pass

def main_app():
    st.markdown("<h1 style='color: #FF5722;'>AI-Driven Personalized Nutrition</h1>", unsafe_allow_html=True)

    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.warning("Please login to access the app.")
        login_page()
        return

    username = st.session_state['username']

    # Collect user details if they haven't been entered yet
    user_data = load_user_data()
    if user_data[username]["age"] is None:
        st.subheader("Enter Your Details")

        age = st.number_input("Enter your age", min_value=1)
        height = st.number_input("Enter your height (cm)", min_value=50)
        weight = st.number_input("Enter your weight (kg)", min_value=10)
        gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
        dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        health_goals = st.selectbox("Select Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])

        if st.button("Save Details", key='save_details_button'):
            update_user_data(username, age, height, weight, gender, dietary_preference, health_goals)
            st.success("Your details have been saved successfully!")
    
    # Rest of the code to generate diet plan, logout, etc.
    if st.button("Logout", key='logout_button'):
        st.session_state['authenticated'] = False
        st.success("You have been logged out.")
        return

    # Generate Diet Plan
    if st.button("Generate 7-Day Diet Plan", key='generate_button'):
        generate_seven_day_diet(user_data[username]["health_goals"])

    # Project Info
    st.write("---")
    st.markdown("<p style='color: #3F51B5;'><b>Project by TechSpark Group</b></p>", unsafe_allow_html=True)
    st.markdown("- Dipak Walunj (Roll No. 60)\n- Divyank Wani (Roll No. 61)\n- Omkar Zinjurde (Roll No. 63)\n- Sakshi Ughade (Roll No. 73)", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Amrutvahini College of Engineering, Sangamner</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Contact: techspark.support@gmail.com</p>", unsafe_allow_html=True)

    # Custom button for "Create Account" positioned at the bottom-right
    st.markdown("""
        <style>
            .create-account-btn {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                font-size: 14px;
                border-radius: 5px;
            }
        </style>
        <a href="javascript:void(0);" class="create-account-btn" onclick="window.location.href='/register'">Create Account</a>
    """)

if __name__ == '__main__':
    main_app()
