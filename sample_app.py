import streamlit as st
import json
import os

# File to store user data
db_file = "user_data.json"

def load_user_data():
    try:
        with open(db_file, "r") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(data):
    with open(db_file, "w") as file:
        json.dump(data, file, indent=4)

def register_page():
    st.title("Create an Account")
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
            st.error("Username already exists. Choose another.")
        else:
            user_data[new_username] = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": new_password,
                "last_meal_plan": ""
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.success(f"Welcome back, {user_data[username]['name']}!")
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
        else:
            st.error("Invalid credentials. Please try again.")

def generate_diet_plan(diet_goal):
    diet_plans = {
        "Weight Loss": "Dal khichdi, salad, soup",
        "Balanced Nutrition": "Rice, dal, veggies",
        "Muscle Gain": "Eggs, grilled chicken, paneer"
    }
    return diet_plans.get(diet_goal, "No diet plan found.")

def main_app():
    st.title("AI Nutrition - Personalized Diet")
    username = st.session_state.get("username")
    user_data = load_user_data()
    
    if not username or username not in user_data:
        st.error("Session expired. Please login again.")
        return
    
    age = st.number_input("Age", min_value=1)
    height = st.number_input("Height (cm)", min_value=50)
    weight = st.number_input("Weight (kg)", min_value=10)
    diet_goal = st.selectbox("Select Diet Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])
    
    if st.button("Generate Diet Plan"):
        meal_plan = generate_diet_plan(diet_goal)
        user_data[username]["last_meal_plan"] = meal_plan
        save_user_data(user_data)
        st.session_state["last_meal_plan"] = meal_plan
        st.success("Diet plan saved!")
        st.write(meal_plan)
    
    if "last_meal_plan" in user_data[username]:
        st.subheader("Your Last Selected Diet Plan")
        st.write(user_data[username]["last_meal_plan"])
    
    if st.button("Logout"):
        st.session_state.clear()
        st.success("Logged out successfully!")

def main():
    if "authenticated" not in st.session_state:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
