# AI Nutrition App (Full Streamlit Code)

import streamlit as st
import json
import os
from datetime import datetime
import random

# File paths
image_path = os.getcwd()
db_file = os.path.join(image_path, "user_data.json")
login_image = os.path.join("image", "nutrition_login.jpg.webp")
register_image = os.path.join("image", "nutrition_register.jpg.webp")

# Load and Save JSON user data
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

# BMR calculator (Mifflin-St Jeor)
def calculate_bmr(weight, height, age, gender, activity_level):
    gender_factor = 5 if gender == "Male" else -161
    bmr = 10 * weight + 6.25 * height - 5 * age + gender_factor
    activity_multiplier = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    return round(bmr * activity_multiplier.get(activity_level, 1.2), 2)

# Streamlit UI
st.set_page_config(page_title="AI Nutrition App", layout="centered")

# App States
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

user_db = load_user_data()

# Authentication UI
def show_login():
    st.image(login_image, use_column_width=True)
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in user_db and user_db[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.current_user = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

    st.markdown("<div style='text-align:right;'>Don't have an account? 👉 [Create Account](#register)</div>", unsafe_allow_html=True)

def show_register():
    st.image(register_image, use_column_width=True)
    st.title("Register")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Register"):
        if username in user_db:
            st.error("Username already exists")
        else:
            user_db[username] = {"password": password, "profile": {}, "plan": {}}
            save_user_data(user_db)
            st.success("Account created! Please log in.")

# Diet Plan Generator with unique meals

def get_diet_plan(goal, diet_type):
    plan_bank = {
        "Weight Loss": {
            "Vegetarian": [
                "Oats with fruits", "Roti with sabzi", "Moong dal khichdi", "Poha", "Brown rice with dal", "Vegetable soup with toast",
                "Upma", "Paneer bhurji", "Mixed veg curry", "Idli with chutney", "Lentil salad", "Veg pulao", "Fruit smoothie",
                "Vegetable khichdi", "Dalia with veggies", "Cornflakes with milk", "Stuffed paratha", "Tofu curry with roti",
                "Besan chilla", "Veg sandwich", "Spinach soup with toast"
            ],
            "Non-Vegetarian": [
                "Boiled eggs with toast", "Grilled chicken salad", "Fish curry with brown rice", "Egg curry with rice", "Chicken soup",
                "Vegetable omelette", "Grilled chicken wrap", "Fish tikka", "Tuna salad", "Egg bhurji with roti", "Smoothie with nuts",
                "Chicken rice bowl", "Grilled fish with veggies", "Egg fried rice", "Boiled chicken with veggies", "Multigrain toast",
                "Chicken curry with roti", "Tandoori fish", "Egg curry + oats", "Chicken tikka + salad", "Tuna sandwich"
            ]
        },
        "Balanced Nutrition": {
            "Vegetarian": [
                "Milk + paratha", "Dal chawal + salad", "Veg curry + roti", "Upma + milk", "Chole with rice", "Paneer sabzi + roti",
                "Smoothie + toast", "Rajma with brown rice", "Dalia with curd", "Idli + sambhar", "Veg paratha + curd", "Kadhi + rice",
                "Cornflakes + fruit", "Lauki sabzi + roti", "Khichdi with ghee", "Poha + sprouts", "Palak dal + rice", "Paneer tikka with salad",
                "Multigrain sandwich", "Veg pulao + raita", "Mix veg with chapati"
            ],
            "Non-Vegetarian": [
                "Boiled eggs + bread", "Chicken curry + rice", "Fish curry + roti", "Oats + fruits", "Egg bhurji + paratha", "Chicken rice",
                "Toast + smoothie", "Grilled fish + salad", "Egg curry + rice", "Poha + milk", "Chicken wrap", "Grilled chicken with chapati",
                "Upma + juice", "Tuna salad", "Boiled eggs + veg soup", "Idli + chutney", "Fish biryani", "Chicken tikka",
                "Fruit + toast", "Boiled eggs + roti", "Chicken stew + rice"
            ]
        },
        "Muscle Gain": {
            "Vegetarian": [
                "Paneer paratha + milk", "Dal rice + paneer", "Chole with roti", "Oats with peanut butter", "Rajma + rice", "Tofu bhurji with bread",
                "Banana shake + roti", "Soya chunks + pulao", "Veg biryani", "Dalia + dry fruits", "Khichdi + curd", "Paneer butter masala + roti",
                "Boiled chana + poha", "Mixed dal + roti", "Palak paneer + rice", "Fruit + oats", "Chole bhature", "Stuffed paratha + curd",
                "Multigrain toast + milk", "Paneer tikka", "Matar paneer + roti"
            ],
            "Non-Vegetarian": [
                "Eggs + toast", "Chicken curry + rice", "Fish + veggies", "Smoothie + boiled eggs", "Grilled chicken + roti", "Fish pulao",
                "Oats + omelet", "Boiled chicken + rice", "Egg curry + chapati", "Idli + sambhar", "Chicken wrap", "Grilled fish + curd",
                "Paratha + eggs", "Tandoori chicken", "Fish tikka + salad", "Cornflakes + milk", "Chicken biryani", "Boiled eggs + soup",
                "Fruit + toast", "Egg roll", "Chicken stew"
            ]
        }
    }

    meals = random.sample(plan_bank[goal][diet_type], 21)
    return [(meals[i], meals[i+1], meals[i+2]) for i in range(0, 21, 3)]

# Main App (after login)
def show_dashboard():
    st.title("Personalized Indian Diet Plan")
    user = st.session_state.current_user

    if not user_db[user].get("profile"):
        st.subheader("Enter Your Health Details")
        age = st.number_input("Age", 10, 100)
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.number_input("Height (cm)", 100, 250)
        weight = st.number_input("Weight (kg)", 30, 200)
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
        goal = st.selectbox("Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])
        diet_type = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
        allergies = st.text_input("Any Allergies (comma-separated)")

        if st.button("Generate Diet Plan"):
            bmr = calculate_bmr(weight, height, age, gender, activity_level)
            plan = get_diet_plan(goal, diet_type)
            profile = {
                "age": age, "gender": gender, "height": height, "weight": weight,
                "activity_level": activity_level, "goal": goal,
                "diet": diet_type, "allergies": allergies, "bmr": bmr
            }
            user_db[user]["profile"] = profile
            user_db[user]["plan"] = plan
            save_user_data(user_db)
            st.success("Diet plan generated and saved successfully!")

    else:
        profile = user_db[user]["profile"]
        plan = user_db[user].get("plan", [])
        st.subheader("Welcome back! Here's your profile")
        st.write(f"**Goal:** {profile['goal']} | **Calories/day:** {profile['bmr']} kcal")
        st.markdown(f"💧 Recommended Water: {round(profile['weight'] * 0.033, 2)} liters")

        if plan:
            st.subheader("Your 7-Day Diet Plan")
            for i, (b, l, d) in enumerate(plan):
                st.markdown(f"### Day {i+1}")
                st.write(f"**Breakfast:** {b}")
                st.write(f"**Lunch:** {l}")
                st.write(f"**Dinner:** {d}")
                st.markdown("---")

    # Footer
    st.markdown("""
    <hr>
    <div style='text-align:center; color:gray;'>
        <b>TechSpark Group:</b> Sakshi Ughade, Dipak Walunj, Divyank Wani, Omkar Zinjurde<br>
        Amrutvahini College of Engineering, Sangamner - IT Department<br>
        <span style='color:darkorange;'>© 2025 AI-Driven Personalized Nutrition Using IoT</span>
    </div>
    """, unsafe_allow_html=True)

# Routing UI
page = st.experimental_get_query_params().get("page", ["login"])[0]
if page == "register":
    show_register()
elif not st.session_state.authenticated:
    show_login()
else:
    show_dashboard()
