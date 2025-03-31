import streamlit as st
import json
import datetime

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

def generate_diet_plan(diet_goal, duration):
    plan = {
        "Weight Loss": ["Oats and fruits", "Salad and grilled chicken", "Vegetable soup", "Nuts and green tea"],
        "Weight Gain": ["Milk and banana", "Rice with protein", "Peanut butter toast", "Protein shakes"],
        "Balanced Nutrition": ["Eggs and toast", "Fish with veggies", "Lentils and brown rice", "Yogurt and almonds"]
    }
    
    days = {"1 Week": 7, "2 Weeks": 14, "1 Month": 30}
    return [f"Day {i+1}: {meal}" for i, meal in enumerate(plan[diet_goal] * (days[duration] // 4))]

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
            user_data[new_username] = {"name": name, "email": email, "phone": phone, "password": new_password, "last_activity": "No previous activity"}
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

def login_page():
    st.markdown("<h1 style='color: #2196F3;'>AI for Personalized Nutrition - Login</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_login.jpg.webp")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login", key='login_button'):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.success(f"Welcome back, {user_data[username]['name']}!")
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
        else:
            st.error("Invalid credentials. Please try again.")

def main_app():
    st.markdown("<h1 style='color: #FF5722;'>AI-Driven Personalized Nutrition Chatbot</h1>", unsafe_allow_html=True)
    
    if st.button("Logout", key='logout_button'):
        st.session_state['authenticated'] = False
        st.success("You have been logged out.")
        return
    
    username = st.session_state.get('username', None)
    user_data = load_user_data()
    
    if username and username in user_data:
        st.info(f"Last Activity: {user_data[username].get('last_activity', 'No previous activity')}")
    
    age = st.number_input("Enter your age", min_value=1)
    height = st.number_input("Enter your height (cm)", min_value=50)
    weight = st.number_input("Enter your weight (kg)", min_value=10)
    dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    diet_goal = st.selectbox("Diet Goal", ["Weight Loss", "Weight Gain", "Balanced Nutrition"])
    diet_duration = st.selectbox("Select Diet Duration", ["1 Week", "2 Weeks", "1 Month"])
    
    if st.button("Get Nutrition Plan", key='plan_button'):
        plan = generate_diet_plan(diet_goal, diet_duration)
        st.success(f"Your personalized diet plan for {diet_duration}:")
        for day in plan:
            st.write(day)
        
        if username and username in user_data:
            user_data[username]['last_activity'] = f"Generated a {diet_duration} {diet_goal} diet plan on {datetime.date.today()}"
            save_user_data(user_data)
    
    st.write("---")
    st.markdown("<p style='color: #3F51B5;'><b>Project by TechSpark Group</b></p>", unsafe_allow_html=True)
    st.markdown("- Dipak Walunj\n- Divyank Wani\n- Omkar Zinjurde\n- Sakshi Ughade", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Amrutvahini College of Engineering, Sangamner</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Contact: techspark.support@gmail.com</p>", unsafe_allow_html=True)

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
        st.warning("Please login first.")

