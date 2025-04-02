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

# Define diet plans
diet_plans = {
    "Weight Loss": {
        "Day 1": {"Breakfast": "Poha", "Lunch": "Dal khichdi", "Dinner": "Vegetable soup"},
        "Day 2": {"Breakfast": "Oatmeal", "Lunch": "Quinoa salad", "Dinner": "Grilled chicken"},
        "Day 3": {"Breakfast": "Eggs & Spinach", "Lunch": "Veg Stir Fry", "Dinner": "Soup & Toast"},
        "Day 4": {"Breakfast": "Greek Yogurt", "Lunch": "Chickpea Salad", "Dinner": "Grilled Fish"},
        "Day 5": {"Breakfast": "Smoothie", "Lunch": "Lentil Soup", "Dinner": "Cauliflower Rice"},
        "Day 6": {"Breakfast": "Chia Pudding", "Lunch": "Grilled Chicken Salad", "Dinner": "Zucchini Noodles"},
        "Day 7": {"Breakfast": "Avocado Toast", "Lunch": "Veg Stir Fry", "Dinner": "Steamed Veggies"}
    },
    "Balanced Nutrition": {
        "Day 1": {"Breakfast": "Pancakes", "Lunch": "Rice & Dal", "Dinner": "Grilled Chicken"},
        "Day 2": {"Breakfast": "Smoothie", "Lunch": "Lentil Soup", "Dinner": "Fish Curry"},
        "Day 3": {"Breakfast": "Omelet", "Lunch": "Vegetable Pulao", "Dinner": "Paneer with Quinoa"},
        "Day 4": {"Breakfast": "Cornflakes", "Lunch": "Dal & Roti", "Dinner": "Chicken Stew"},
        "Day 5": {"Breakfast": "Idli", "Lunch": "Chickpea Salad", "Dinner": "Vegetable Soup"},
        "Day 6": {"Breakfast": "Fruit Salad", "Lunch": "Grilled Fish", "Dinner": "Paneer Tikka"},
        "Day 7": {"Breakfast": "Poha", "Lunch": "Rajma Rice", "Dinner": "Grilled Veggies"}
    },
    "Muscle Gain": {
        "Day 1": {"Breakfast": "Eggs & Toast", "Lunch": "Chicken & Quinoa", "Dinner": "Salmon & Potatoes"},
        "Day 2": {"Breakfast": "Protein Shake", "Lunch": "Lentil Soup", "Dinner": "Grilled Steak"},
        "Day 3": {"Breakfast": "Oats & Peanut Butter", "Lunch": "Chicken & Sweet Potato", "Dinner": "Tofu Stir Fry"},
        "Day 4": {"Breakfast": "Greek Yogurt", "Lunch": "Fish & Quinoa", "Dinner": "Grilled Paneer"},
        "Day 5": {"Breakfast": "Omelet", "Lunch": "Beef Stir Fry", "Dinner": "Baked Chicken"},
        "Day 6": {"Breakfast": "Protein Pancakes", "Lunch": "Turkey Sandwich", "Dinner": "Veg Curry"},
        "Day 7": {"Breakfast": "Cottage Cheese", "Lunch": "Salmon & Greens", "Dinner": "Steak & Roasted Veggies"}
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
                "last_meal": {"Breakfast": "", "Lunch": "", "Dinner": ""},
                "diet_plan": {}  # Empty diet plan initially
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

# Main App: Diet Plan and Meal Saving
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
        user_data[username]['diet_plan'] = diet_plans[diet_choice]
        save_user_data(user_data)
        st.success(f"Your {diet_choice} diet plan has been saved!")

    # Display last meal
    last_meal = user_data[username].get("last_meal", {"Breakfast": "No record", "Lunch": "No record", "Dinner": "No record"})
    st.markdown("*Last Recorded Meals:*")
    st.markdown(f"- *Breakfast:* {last_meal['Breakfast']}")
    st.markdown(f"- *Lunch:* {last_meal['Lunch']}")
    st.markdown(f"- *Dinner:* {last_meal['Dinner']}")

    # Meal Input
    breakfast = st.text_input("Enter your Breakfast details")
    lunch = st.text_input("Enter your Lunch details")
    dinner = st.text_input("Enter your Dinner details")
    
    if st.button("Save Meals"):
        user_data[username]["last_meal"] = {"Breakfast": breakfast, "Lunch": lunch, "Dinner": dinner}
        save_user_data(user_data)
        st.success("Meals saved successfully!")

# Main function to control the app navigation
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'register':
        register_page()
    elif st.session_state['page'] == 'main':
        main_app()

if _name_ == "_main_":
    main()
