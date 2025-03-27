import streamlit as st
import json

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
            user_data[new_username] = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": new_password
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

def login_page():
    st.title("AI Nutrition Chatbot - Login")
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

def main_app():
    st.title("AI-Driven Personalized Nutrition Chatbot")

    # Collect user details
    age = st.number_input("Enter your age", min_value=1)
    height = st.number_input("Enter your height (cm)", min_value=50)
    weight = st.number_input("Enter your weight (kg)", min_value=10)
    gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
    body_type = st.selectbox("Select Body Type", ["Ectomorph", "Mesomorph", "Endomorph"])
    dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    allergies = st.text_input("List any allergies (comma separated)")
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
    diet_duration = st.selectbox("Select Diet Duration", ["1 Week", "2 Weeks", "1 Month", "3 Months", "6 Months", "1 Year"])

    if st.button("Get Nutrition Plan"):
        st.success("Here’s your personalized nutrition plan:")
        st.write(f"✅ Age: {age} years")
        st.write(f"✅ Height: {height} cm")
        st.write(f"✅ Weight: {weight} kg")
        st.write(f"✅ Gender: {gender}")
        st.write(f"✅ Body Type: {body_type}")
        st.write(f"✅ Dietary Preference: {dietary_preference}")
        st.write(f"✅ Allergies: {allergies if allergies else 'None'}")
        st.write(f"📅 Diet Duration: {diet_duration}")

        # Example weekly diet plan
        st.write("### Sample Diet Plan")
        st.write("**Day 1**")
        st.write("Breakfast: Oats + Fruits / Boiled Eggs + Avocado Toast")
        st.write("Lunch: Grilled Chicken + Salad / Paneer Bhurji + Roti")
        st.write("Dinner: Veg Curry + Brown Rice / Dal Tadka + Jeera Rice")

        st.write("**Day 2**")
        st.write("Breakfast: Poha + Sprouts / Smoothie Bowl")
        st.write("Lunch: Paneer + Roti / Chicken Wrap")
        st.write("Dinner: Quinoa + Veg Curry / Pasta with Veggies")

        st.write("**Day 3**")
        st.write("Breakfast: Idli + Sambar / Veg Upma")
        st.write("Lunch: Rajma + Rice / Chicken Tikka Salad")
        st.write("Dinner: Mixed Veg Curry + Roti / Grilled Fish with Rice")

        st.write("**Day 4**")
        st.write("Breakfast: Paratha + Curd / Banana Pancakes")
        st.write("Lunch: Fish Curry + Rice / Chana Masala with Roti")
        st.write("Dinner: Dal Khichdi / Palak Paneer with Rice")

        st.write("**Day 5**")
        st.write("Breakfast: Upma + Coconut Chutney / Veg Sandwich")
        st.write("Lunch: Chicken Biryani / Veg Pulao")
        st.write("Dinner: Spinach Soup + Toast / Chicken Stew")

        st.write("**Day 6**")
        st.write("Breakfast: Dosa + Chutney / Masala Omelette")
        st.write("Lunch: Egg Curry + Rice / Veg Fried Rice")
        st.write("Dinner: Veg Pulao + Raita / Tofu Stir Fry")

        st.write("**Day 7**")
        st.write("Breakfast: Methi Thepla / Fruit Salad Bowl")
        st.write("Lunch: Soya Chunk Curry + Roti / Veg Thali")
        st.write("Dinner: Vegetable Stir Fry + Brown Rice / Chicken Korma")

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
