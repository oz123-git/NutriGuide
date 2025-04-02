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

# Define diet plans with nutrition factors
diet_plans = {
    "Weight Loss": {
        "Day 1": {"Breakfast": ("Poha", 200, 5, 30, 5), "Lunch": ("Dal khichdi", 350, 10, 50, 8), "Dinner": ("Vegetable soup", 150, 3, 20, 2)},
        "Day 2": {"Breakfast": ("Oatmeal", 250, 8, 40, 6), "Lunch": ("Quinoa salad", 300, 12, 45, 10), "Dinner": ("Grilled chicken", 350, 40, 5, 15)},
    },
    "Balanced Nutrition": {
        "Day 1": {"Breakfast": ("Pancakes", 300, 8, 50, 10), "Lunch": ("Rice & Dal", 400, 12, 60, 12), "Dinner": ("Grilled Chicken", 350, 40, 5, 15)},
    },
    "Muscle Gain": {
        "Day 1": {"Breakfast": ("Eggs & Toast", 400, 30, 30, 20), "Lunch": ("Chicken & Quinoa", 500, 50, 60, 15), "Dinner": ("Salmon & Potatoes", 600, 45, 50, 25)},
    }
}

# Register Page
def register_page():
    st.markdown("<h1 style='color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_register.jpg.webp")
    
    name = st.text_input("Name")
    email = st.text_input("Email ID")
    phone = st.text_input("Phone Number")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type='password')
    
    if st.button("Register"):
        if not all([name, email, phone, new_username, new_password]):
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
                "diet_plan": ""
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")
            st.session_state['page'] = "login"
    
    if st.button("Back to Login"):
        st.session_state['page'] = "login"

# Login Page
def login_page():
    st.markdown("<h1 style='color: #2196F3;'>AI Nutrition - Login</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_login.jpg.webp")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.success(f"Welcome back, {user_data[username]['name']}!")
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.session_state['page'] = "main"
        else:
            st.error("Invalid credentials. Please try again.")
    
    if st.button("Create Account"):
        st.session_state['page'] = "register"

# Main App
def main_app():
    st.markdown("<h1 style='color: #FF5722;'>AI-Driven Personalized Nutrition</h1>", unsafe_allow_html=True)
    
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['page'] = "login"
        return
    
    user_data = load_user_data()
    username = st.session_state['username']
    
    st.markdown(f"*Welcome, {user_data[username]['name']}!*")
    
    # Select diet plan
    diet_choice = st.selectbox("Select your diet plan", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])
    
    if diet_choice:
        user_data[username]['diet_plan'] = diet_choice
        save_user_data(user_data)
        st.success(f"Your {diet_choice} diet plan has been saved!")
        
        # Show diet plan details
        st.subheader(f"{diet_choice} Diet Plan")
        for day, meals in diet_plans[diet_choice].items():
            st.markdown(f"**{day}**")
            for meal, (food, calories, protein, carbs, fats) in meals.items():
                st.markdown(f"- *{meal}:* {food} ({calories} kcal, {protein}g Protein, {carbs}g Carbs, {fats}g Fats)")
    
# Main function
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    
    if st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'register':
        register_page()
    elif st.session_state['page'] == 'main':
        main_app()

if __name__ == "__main__":
    main()
