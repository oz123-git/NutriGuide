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

    # Use session state to persist values
    for key in ["name", "email", "phone", "new_username", "new_password"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    st.session_state.name = st.text_input("Name", value=st.session_state.name)
    st.session_state.email = st.text_input("Email ID", value=st.session_state.email)
    st.session_state.phone = st.text_input("Phone Number", value=st.session_state.phone)
    st.session_state.new_username = st.text_input("Create Username", value=st.session_state.new_username)
    st.session_state.new_password = st.text_input("Create Password", type='password', value=st.session_state.new_password)

    if st.button("Register"):
        if not all([st.session_state.name, st.session_state.email, st.session_state.phone, st.session_state.new_username, st.session_state.new_password]):
            st.error("All fields are required!")
            return
        
        user_data = load_user_data()

        if st.session_state.new_username in user_data:
            st.error("Username already exists. Please choose another.")
        else:
            user_data[st.session_state.new_username] = {
                "name": st.session_state.name,
                "email": st.session_state.email,
                "phone": st.session_state.phone,
                "password": st.session_state.new_password
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

            # Reset fields after successful registration
            for key in ["name", "email", "phone", "new_username", "new_password"]:
                st.session_state[key] = ""

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
        else:
            st.error("Invalid credentials. Please try again.")

def generate_seven_day_diet(diet_goal):
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

    st.markdown(f"### 7-Day {diet_goal} Meal Plan:")
    for day, meals in diet_plans[diet_goal].items():
        st.markdown(f"**{day}:**")
        for meal_type, meal in meals.items():
            st.markdown(f"  - **{meal_type}:** {meal}")
        st.markdown("---")

def main_app():
    st.markdown("<h1 style='color: #FF5722;'>AI-Driven Personalized Nutrition</h1>", unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.success("You have been logged out.")
        return

    age = st.number_input("Enter your age", min_value=1)
    height = st.number_input("Enter your height (cm)", min_value=50)
    weight = st.number_input("Enter your weight (kg)", min_value=10)
    gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
    dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    health_goals = st.selectbox("Select Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])

    if st.button("Generate 7-Day Diet Plan"):
        generate_seven_day_diet(health_goals)

    st.markdown("**TechSpark Group**")
    st.markdown("- Dipak Walunj (Roll No. 60)\n- Divyank Wani (Roll No. 61)\n- Omkar Zinjurde (Roll No. 63)\n- Sakshi Ughade (Roll No. 73)")
    st.markdown("Amrutvahini College of Engineering, Sangamner")

if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        login_page()
    else:
        main_app()
