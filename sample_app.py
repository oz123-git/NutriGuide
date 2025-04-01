import streamlit as st
import json
import datetime

# File to store user data and diet plans
db_file = "user_data.json"
diet_plan_file = "diet_plans.json"

# Group Information
group_name = "TechSpark"
members = ["Dipak Walunj (Roll No. 60)", "Divyank Wani (Roll No. 61)", "Omkar Zinjurde (Roll No. 63)"]
college_name = "Amrutvahini College of Engineering, Sangamner"

def load_user_data():
    try:
        with open(db_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(data):
    with open(db_file, "w") as file:
        json.dump(data, file, indent=4)

def load_diet_plans():
    try:
        with open(diet_plan_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_diet_plan(data):
    with open(diet_plan_file, "w") as file:
        json.dump(data, file, indent=4)

def generate_diet_plan(diet_goal, duration):
    plan = {
        "Weight Loss": [
            {"Breakfast": "Poha with vegetables and green tea", "Lunch": "Grilled chicken with roti and salad", "Dinner": "Dal Tadka with brown rice", "Snack": "Cucumber and carrot sticks", "Water": "8 glasses per day"},
            {"Breakfast": "Vegetable upma with buttermilk", "Lunch": "Palak paneer with chapati", "Dinner": "Vegetable soup and brown rice", "Snack": "Apple and almonds", "Water": "8 glasses per day"},
            {"Breakfast": "Oats porridge with nuts", "Lunch": "Tandoori chicken with green salad", "Dinner": "Moong dal khichdi with curd", "Snack": "Greek yogurt with honey", "Water": "8 glasses per day"}
        ],
        "Weight Gain": [
            {"Breakfast": "Aloo paratha with curd", "Lunch": "Paneer butter masala with naan", "Dinner": "Chicken curry with white rice", "Snack": "Peanut butter with whole wheat bread", "Water": "10 glasses per day"},
            {"Breakfast": "Masala dosa with sambar and coconut chutney", "Lunch": "Mutton curry with steamed rice", "Dinner": "Pasta with paneer and vegetable stir fry", "Snack": "Banana and milkshake", "Water": "10 glasses per day"},
            {"Breakfast": "Pancakes with ghee and honey", "Lunch": "Chole bhature", "Dinner": "Biryani with raita", "Snack": "Protein shake with milk", "Water": "10 glasses per day"}
        ],
        "Balanced Nutrition": [
            {"Breakfast": "Oats idli with chutney", "Lunch": "Grilled fish with brown rice and vegetables", "Dinner": "Vegetable curry with roti", "Snack": "Paneer tikka", "Water": "8-10 glasses per day"},
            {"Breakfast": "Moong dal cheela with green chutney", "Lunch": "Rajma chawal with a side of salad", "Dinner": "Tofu stir fry with quinoa", "Snack": "Mixed nuts", "Water": "8-10 glasses per day"},
            {"Breakfast": "Dosa with sambar and coconut chutney", "Lunch": "Lentil soup with chapati", "Dinner": "Grilled chicken with steamed vegetables", "Snack": "Fruit salad with yogurt", "Water": "8-10 glasses per day"}
        ]
    }
    
    days = {"1 Week": 7, "2 Weeks": 14, "1 Month": 30}
    total_days = days[duration]
    full_plan = []
    
    for i in range(total_days):
        meal_plan = plan[diet_goal][i % len(plan[diet_goal])]
        full_plan.append(f"Day {i+1}\n" + "="*20 + "\n"
                         f"- **Breakfast:** {meal_plan['Breakfast']}\n"
                         f"- **Lunch:** {meal_plan['Lunch']}\n"
                         f"- **Dinner:** {meal_plan['Dinner']}\n"
                         f"- **Snack:** {meal_plan['Snack']}\n"
                         f"- **Water Intake:** {meal_plan['Water']}\n")
    return full_plan

def register_page():
    st.title("Create an Account")
    st.image("image/nutrition_register.jpg.webp")
    name = st.text_input("Name")
    email = st.text_input("Email ID")
    phone = st.text_input("Phone Number")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type='password')
    
    if st.button("Register"):
        user_data = load_user_data()
        if new_username in user_data:
            st.error("Username already exists. Please choose another.")
        else:
            user_data[new_username] = {"name": name, "email": email, "phone": phone, "password": new_password}
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

def login_page():
    st.title("AI for Personalized Nutrition - Login")
    st.image("image/nutrition_login.jpg.webp")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.success(f"Welcome back, {user_data[username]['name']}!")
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
        else:
            st.error("Invalid credentials. Please try again.")

def main_app():
    st.title("AI for Personalized Nutrition")
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.success("You have been logged out.")
        return
    
    diet_goal = st.selectbox("Diet Goal", ["Weight Loss", "Weight Gain", "Balanced Nutrition"])
    diet_duration = st.selectbox("Select Diet Duration", ["1 Week", "2 Weeks", "1 Month"])
    
    if st.button("Get Nutrition Plan"):
        plan = generate_diet_plan(diet_goal, diet_duration)
        for day in plan:
            st.markdown(day)
