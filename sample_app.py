import streamlit as st
import json
import os
import random

# File to store user data
USER_DATA_FILE = "user_data.json"

# Load user data
if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "r") as f:
        user_data = json.load(f)
else:
    user_data = {}

# Save user data
def save_user_data():
    with open(USER_DATA_FILE, "w") as f:
        json.dump(user_data, f, indent=4)

# Streamlit config
st.set_page_config(page_title="AI Nutrition App", layout="wide")
st.title("AI Nutrition App 🍽️")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["Login", "Register"] if not st.session_state.logged_in else ["Dashboard", "Daily Meal Tracker", "Diet Plan", "Logout"])

# Sample Indian food items categorized by type (vegetarian only)
indian_foods = {
    "Breakfast": ["Poha", "Upma", "Idli", "Vegetable Dalia", "Moong Dal Chilla", "Besan Cheela", "Oats with fruits", "Paratha with curd", "Methi Thepla", "Rava Uttapam", "Sprouts Salad", "Dhokla", "Vegetable Sandwich", "Pesarattu", "Paneer Stuffed Paratha"],
    "Lunch": ["Rajma Chawal", "Chole Roti", "Vegetable Pulao", "Dal Tadka with Rice", "Palak Paneer with Roti", "Kadhi Chawal", "Mix Veg with Chapati", "Baingan Bharta with Roti", "Stuffed Capsicum with Rice", "Matar Paneer with Roti", "Bhindi Masala with Roti", "Toor Dal with Rice", "Aloo Methi with Roti", "Zunka Bhakri", "Veg Kofta with Roti"],
    "Dinner": ["Khichdi", "Veg Biryani", "Tinda with Roti", "Lauki Sabzi with Rice", "Vegetable Soup with Bread", "Paneer Bhurji with Chapati", "Tofu Curry with Rice", "Aloo Gobi with Roti", "Vegetable Stew with Idiyappam", "Masoor Dal with Rice", "Gatte ki Sabzi with Roti", "Tamarind Rice", "Bottle Gourd Curry with Roti", "Cabbage Poriyal with Rice", "Moong Dal Soup"]
}

# Generate a 7-day diet plan with unique meals per day
def generate_diet_plan():
    plan = []
    used_meals = {"Breakfast": set(), "Lunch": set(), "Dinner": set()}
    for day in range(7):
        day_plan = {}
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            available = list(set(indian_foods[meal_type]) - used_meals[meal_type])
            if not available:
                available = list(set(indian_foods[meal_type]))  # Reset if all used
                used_meals[meal_type] = set()
            meal = random.choice(available)
            used_meals[meal_type].add(meal)
            day_plan[meal_type] = meal
        plan.append(day_plan)
    return plan

# Register Page
if menu == "Register":
    st.subheader("Create an Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Register"):
        if new_username in user_data:
            st.error("Username already exists.")
        else:
            user_data[new_username] = {
                "password": new_password,
                "info": {},
                "diet_plan": [],
                "last_meal": {"Breakfast": "", "Lunch": "", "Dinner": ""}
            }
            save_user_data()
            st.success("Account created successfully. Please log in.")

# Login Page
elif menu == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in user_data and user_data[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

# Logout
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully.")

# Dashboard Page
elif st.session_state.logged_in and menu == "Dashboard":
    username = st.session_state.username
    st.subheader("Personalized Nutrition Info")

    # Load previous info if exists
    user_info = user_data[username].get("info", {})

    age = st.number_input("Age", min_value=1, value=user_info.get("Age", 25))
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user_info.get("Gender", "Male")))
    height = st.number_input("Height (in cm)", min_value=50, value=user_info.get("Height", 170))
    weight = st.number_input("Weight (in kg)", min_value=10, value=user_info.get("Weight", 70))
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active"], index=["Sedentary", "Lightly active", "Moderately active", "Very active"].index(user_info.get("Activity", "Sedentary")))
    goal = st.selectbox("Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"], index=["Weight Loss", "Balanced Nutrition", "Muscle Gain"].index(user_info.get("Goal", "Balanced Nutrition")))
    diet_pref = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian"], index=["Vegetarian", "Non-Vegetarian"].index(user_info.get("Diet", "Vegetarian")))
    allergies = st.text_input("Allergies (comma separated)", value=user_info.get("Allergies", ""))

    if st.button("Save Health Info"):
        user_data[username]["info"] = {
            "Age": age,
            "Gender": gender,
            "Height": height,
            "Weight": weight,
            "Activity": activity,
            "Goal": goal,
            "Diet": diet_pref,
            "Allergies": allergies
        }
        save_user_data()
        st.success("Health data saved successfully.")

    st.subheader("Your Current Info")
    st.write(user_data[username]["info"])

# Meal Tracker Page
elif st.session_state.logged_in and menu == "Daily Meal Tracker":
    username = st.session_state.username
    st.subheader("Daily Meal Tracker")

    if "last_meal" not in user_data[username]:
        user_data[username]["last_meal"] = {"Breakfast": "", "Lunch": "", "Dinner": ""}
        save_user_data()

    breakfast = st.text_input("Enter your Breakfast", value=user_data[username]["last_meal"].get("Breakfast", ""))
    lunch = st.text_input("Enter your Lunch", value=user_data[username]["last_meal"].get("Lunch", ""))
    dinner = st.text_input("Enter your Dinner", value=user_data[username]["last_meal"].get("Dinner", ""))

    if st.button("Save Meals"):
        user_data[username]["last_meal"] = {
            "Breakfast": breakfast,
            "Lunch": lunch,
            "Dinner": dinner
        }
        save_user_data()
        st.success("Your meals have been saved successfully!")

    st.subheader("Your Last Saved Meals")
    last_meal = user_data[username]["last_meal"]
    st.write(f"🍳 **Breakfast:** {last_meal.get('Breakfast', '')}")
    st.write(f"🍛 **Lunch:** {last_meal.get('Lunch', '')}")
    st.write(f"🍽️ **Dinner:** {last_meal.get('Dinner', '')}")

# Diet Plan Page
elif st.session_state.logged_in and menu == "Diet Plan":
    username = st.session_state.username
    st.subheader("Your 7-Day Personalized Indian Diet Plan")

    if not user_data[username].get("diet_plan"):
        user_data[username]["diet_plan"] = generate_diet_plan()
        save_user_data()

    for day_idx, meals in enumerate(user_data[username]["diet_plan"], start=1):
        st.markdown(f"### Day {day_idx}")
        st.markdown(f"**Breakfast:** {meals['Breakfast']}")
        st.markdown(f"**Lunch:** {meals['Lunch']}")
        st.markdown(f"**Dinner:** {meals['Dinner']}")
        st.markdown("---")

    if st.button("Regenerate Diet Plan"):
        user_data[username]["diet_plan"] = generate_diet_plan()
        save_user_data()
        st.success("Diet plan regenerated!")
        st.experimental_rerun()

# Footer
if st.session_state.logged_in:
    st.markdown("""
    <hr>
    <div style='text-align: right;'>
        <span style='color: #5bc0de;'>Group: TechSpark</span><br>
        <span style='color: #5cb85c;'>College: Amrutvahini College of Engineering, Sangamner</span><br>
        <span style='color: #f0ad4e;'>Branch: Artificial Intelligence and Data Science (AIDS)</span>
    </div>
    """, unsafe_allow_html=True)
