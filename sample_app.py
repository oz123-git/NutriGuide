import streamlit as st
import json
import os

# Paths
image_path = os.getcwd()
db_file = os.path.join(image_path, "user_data.json")

# Load user data from JSON file
def load_user_data():
    try:
        with open(db_file, "r") as file:
            data = file.read().strip()
            return json.loads(data) if data else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save user data to JSON file
def save_user_data(data):
    with open(db_file, "w") as file:
        json.dump(data, file, indent=4)

# Calculate BMR using Mifflin-St Jeor Equation
def calculate_bmr(weight, height, age, activity_level):
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    activity_multiplier = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    return bmr * activity_multiplier.get(activity_level, 1.2)

# Unique Indian 7-Day Diet Plans
diet_plans = {
    "Weight Loss": {
        "Day 1": {"Breakfast": "Oats with skim milk", "Lunch": "Roti with lauki sabzi", "Dinner": "Vegetable soup and salad"},
        "Day 2": {"Breakfast": "Poha with sprouts", "Lunch": "Brown rice with dal", "Dinner": "Grilled paneer with vegetables"},
        "Day 3": {"Breakfast": "Ragi dosa", "Lunch": "Multigrain roti with chole", "Dinner": "Moong dal khichdi with curd"},
        "Day 4": {"Breakfast": "Fruit smoothie", "Lunch": "Quinoa with vegetables", "Dinner": "Palak soup and salad"},
        "Day 5": {"Breakfast": "Upma with peanuts", "Lunch": "Roti with mixed veg", "Dinner": "Vegetable stew with brown bread"},
        "Day 6": {"Breakfast": "Idli with chutney", "Lunch": "Barley khichdi", "Dinner": "Grilled tofu and steamed veg"},
        "Day 7": {"Breakfast": "Besan chilla", "Lunch": "Rice with sambhar", "Dinner": "Lentil soup with salad"},
    },
    "Balanced Nutrition": {
        "Day 1": {"Breakfast": "Idli with sambar", "Lunch": "Rice with dal", "Dinner": "Vegetable pulao"},
        "Day 2": {"Breakfast": "Chapati with bhaji", "Lunch": "Roti with paneer", "Dinner": "Mixed vegetable curry with rice"},
        "Day 3": {"Breakfast": "Cornflakes with milk", "Lunch": "Khichdi with papad", "Dinner": "Chapati with bhindi"},
        "Day 4": {"Breakfast": "Fruit salad and curd", "Lunch": "Veg pulao", "Dinner": "Dal and rice"},
        "Day 5": {"Breakfast": "Upma with chutney", "Lunch": "Paratha with curd", "Dinner": "Stuffed capsicum with rice"},
        "Day 6": {"Breakfast": "Multigrain toast", "Lunch": "Rajma with roti", "Dinner": "Vegetable noodles"},
        "Day 7": {"Breakfast": "Vegetable sandwich", "Lunch": "Pulao with raita", "Dinner": "Chapati with mix veg"},
    },
    "Muscle Gain": {
        "Day 1": {"Breakfast": "Boiled eggs with toast", "Lunch": "Chicken curry with rice", "Dinner": "Paneer with roti"},
        "Day 2": {"Breakfast": "Protein smoothie", "Lunch": "Fish curry with rice", "Dinner": "Egg bhurji with paratha"},
        "Day 3": {"Breakfast": "Sprouted moong salad", "Lunch": "Rajma rice", "Dinner": "Grilled chicken with vegetables"},
        "Day 4": {"Breakfast": "Paneer sandwich", "Lunch": "Stuffed paratha with curd", "Dinner": "Chana masala with rice"},
        "Day 5": {"Breakfast": "Oats with whey protein", "Lunch": "Mixed veg rice", "Dinner": "Soyabean curry with roti"},
        "Day 6": {"Breakfast": "Boiled chana chaat", "Lunch": "Egg curry with rice", "Dinner": "Tofu stir fry with noodles"},
        "Day 7": {"Breakfast": "Wheat flakes with milk", "Lunch": "Paneer tikka with roti", "Dinner": "Dal makhani with rice"},
    }
}

# Register Page
def register_page():
    st.image("nutrition_register.jpg.webp", use_container_width=True)
    st.markdown("<h1 style='color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)

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
                "details_entered": False,
                "water_intake": 0.0,
                "weight_history": [],
                "last_meal": {"Breakfast": "", "Lunch": "", "Dinner": ""},
                "diet_plan": {}
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")
            st.session_state['page'] = "login"

# Login Page
def login_page():
    st.image("nutrition_login.jpg.webp", use_container_width=True)
    st.markdown("<h1 style='color: #2196F3;'>AI Nutrition - Login</h1>", unsafe_allow_html=True)

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

# Main App After Login
def main_app():
    st.image("nutrition_dashboard.jpg.webp", use_container_width=True)
    st.markdown("<h1 style='color: #FF5722;'>AI-Driven Personalized Nutrition</h1>", unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['page'] = "login"
        return

    user_data = load_user_data()
    username = st.session_state['username']

    if not user_data[username].get("details_entered", False):
        st.subheader("Please complete your profile:")
        age = st.number_input("Age", min_value=1, max_value=120)
        height = st.number_input("Height (cm)", min_value=50, max_value=250)
        weight = st.number_input("Weight (kg)", min_value=10, max_value=300)
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])

        if st.button("Save Info"):
            user_data[username].update({
                "age": age,
                "height": height,
                "weight": weight,
                "activity_level": activity_level,
                "details_entered": True
            })
            save_user_data(user_data)
            st.success("Profile updated successfully!")
        return

    weight = user_data[username]["weight"]
    height = user_data[username]["height"]
    age = user_data[username]["age"]
    activity_level = user_data[username]["activity_level"]

    tdee = calculate_bmr(weight, height, age, activity_level)
    st.markdown(f"**Estimated Daily Caloric Needs:** {round(tdee)} kcal")

    water_intake = float(user_data[username].get("water_intake", 0.0))
    water_input = st.number_input("Water Intake (Liters)", min_value=0.0, max_value=10.0, value=water_intake, step=0.1)
    user_data[username]["water_intake"] = water_input

    new_weight = st.number_input("Update Weight (kg)", min_value=10, max_value=300, value=weight)
    if st.button("Save Weight"):
        if "weight_history" not in user_data[username]:
            user_data[username]["weight_history"] = []
        user_data[username]["weight_history"].append(new_weight)
        user_data[username]["weight"] = new_weight
        save_user_data(user_data)
        st.success("Weight updated successfully!")

    diet_choice = st.selectbox("Select your diet plan", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])
    if diet_choice:
        user_data[username]['diet_plan'] = diet_plans[diet_choice]
        save_user_data(user_data)
        st.success(f"Your {diet_choice} diet plan has been saved!")

    st.subheader("Your 7-Day Diet Plan:")
    for day, meals in user_data[username]['diet_plan'].items():
        st.markdown(f"**{day}**")
        for meal_time, food in meals.items():
            st.markdown(f"- **{meal_time}:** {food}")

    st.subheader("Daily Meal Tracker")
    breakfast = st.text_input("Enter your Breakfast")
    lunch = st.text_input("Enter your Lunch")
    dinner = st.text_input("Enter your Dinner")
    if st.button("Save Meals"):
        user_data[username]["last_meal"] = {
            "Breakfast": breakfast,
            "Lunch": lunch,
            "Dinner": dinner
        }
        save_user_data(user_data)
        st.success("Meals saved successfully!")

    st.markdown("""
        <hr>
        <p style='color: teal; text-align: center;'>
        Group Name: <strong>TechSpark</strong> | College: <strong>Amrutvahini College of Engineering, Sangamner</strong><br>
        Branch: <strong>Computer Engineering</strong> | Team Members: <strong>Sakshi Ughade, Dipak Walunj, Divyank Wani, Omkar Zinjurde</strong>
        </p>
    """, unsafe_allow_html=True)
# Navigation
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
