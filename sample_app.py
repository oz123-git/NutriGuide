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
            user_data[new_username] = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": new_password
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

def login_page():
    st.markdown("<h1 style='color: #2196F3;'>AI Nutrition Chatbot - Login</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_login.jpg.webp")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login", key='login_button'):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.success(f"Welcome back, {user_data[username]['name']}!")
            st.session_state['authenticated'] = True
        else:
            st.error("Invalid credentials. Please try again.")

    # Create account link at the bottom right
    st.markdown(
        "<p style='position: absolute; bottom: 20px; right: 20px;'><a href='#' style='color: #4CAF50;'>Create an Account</a></p>", 
        unsafe_allow_html=True
    )

def generate_monthly_diet():
    daily_menus = [
        # 30 days of different Indian meals
        "Day 1: Poha with vegetables and green tea",
        "Day 2: Oats porridge with nuts",
        "Day 3: Dal khichdi with curd",
        "Day 4: Vegetable soup",
        "Day 5: Sprouts salad",
        "Day 6: Aloo paratha with curd",
        "Day 7: Paneer butter masala with naan",
        "Day 8: Chicken curry with rice",
        "Day 9: Banana milkshake",
        "Day 10: Peanut butter toast",
        "Day 11: Oats idli with chutney",
        "Day 12: Rajma chawal with salad",
        "Day 13: Grilled fish with vegetables",
        "Day 14: Tofu stir-fry with quinoa",
        "Day 15: Fruit salad with yogurt",
        "Day 16: Masala dosa with sambar",
        "Day 17: Pesarattu with chutney",
        "Day 18: Aloo tikki with yogurt",
        "Day 19: Chapati with sabzi",
        "Day 20: Pulao with raita",
        "Day 21: Poached eggs on toast",
        "Day 22: Vegetable biryani with curd",
        "Day 23: Chole bhature",
        "Day 24: Kathi roll with veggies",
        "Day 25: Moong dal khichdi",
        "Day 26: Aloo masala with chapati",
        "Day 27: Dhokla with chutney",
        "Day 28: Rava upma with coconut chutney",
        "Day 29: Veg Pulao with salad",
        "Day 30: Palak paneer with rice"
    ]
    
    st.markdown("### 30-Day Indian Diet Plan:")
    for day in daily_menus:
        st.markdown(f"- {day}")

def main_app():
    st.markdown("<h1 style='color: #FF5722;'>AI-Driven Personalized Nutrition</h1>", unsafe_allow_html=True)

    if st.button("Logout", key='logout_button'):
        st.session_state['authenticated'] = False
        st.success("You have been logged out.")
        return

    # Collect user details
    age = st.number_input("Enter your age", min_value=1)
    height = st.number_input("Enter your height (cm)", min_value=50)
    weight = st.number_input("Enter your weight (kg)", min_value=10)
    gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
    dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    diet_goal = st.selectbox("Diet Goal", ["Weight Loss", "Weight Gain", "Balanced Nutrition"])
    allergies = st.text_input("List any allergies (comma separated)")
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
    diet_duration = st.selectbox("Select Diet Duration", ["1 Week", "2 Weeks", "1 Month", "3 Months", "6 Months", "1 Year"])

    # Optional details
    sleep_hours = st.number_input("Sleep Hours per Day", min_value=0, max_value=24)
    water_intake = st.number_input("Water Intake (liters/day)", min_value=0.0)
    stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])

    if diet_duration == "1 Month" and st.button("Get 30-Day Nutrition Plan"):
        generate_monthly_diet()

    if st.button("Get Nutrition Plan", key='plan_button'):
        st.success(f"Recommended Diet Type: {diet_goal}")
        st.markdown("### Suggested Indian Diet Options:")
        if diet_goal == "Weight Loss":
            st.markdown("- Poha with vegetables and green tea\n- Oats porridge with nuts\n- Dal khichdi with curd\n- Vegetable soup\n- Sprouts salad")
        elif diet_goal == "Weight Gain":
            st.markdown("- Aloo paratha with curd\n- Paneer butter masala with naan\n- Chicken curry with rice\n- Banana milkshake\n- Peanut butter toast")
        elif diet_goal == "Balanced Nutrition":
            st.markdown("- Oats idli with chutney\n- Rajma chawal with salad\n- Grilled fish with vegetables\n- Tofu stir-fry with quinoa\n- Fruit salad with yogurt")

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
