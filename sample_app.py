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

# Example 200+ Indian food items categorized (Shortened for simplicity)
unique_diet_items = {
    "Weight Loss": [
        "Upma with coconut chutney", "Poha", "Oats porridge", "Vegetable dalia", "Idli with chutney",
        "Vegetable soup", "Multigrain roti with sabzi", "Green moong dal", "Sprouts salad",
        "Fruit chaat", "Besan chilla", "Low-oil paneer bhurji", "Mixed vegetable curry",
        "Khichdi", "Lauki sabzi", "Tinda curry", "Boiled moong dal salad", "Low-oil rajma",
        "Missi roti", "Grilled paneer cubes", "Low-oil sambhar", "Vegetable upma", "Curd rice",
        "Roti with bottle gourd curry", "Stuffed tinda paratha", "Low-fat curd", "Lemon coriander soup",
        "Palak soup", "Beetroot poriyal", "Karela sabzi", "Baingan bharta"
        # Add more unique meals per day later in loop
    ],
    "Balanced Nutrition": [
        "Idli with sambar", "Rice with rajma", "Aloo-gobi sabzi", "Chapati with dal", "Paneer tikka",
        "Vegetable pulao", "Chana masala", "Mixed fruit salad", "Stuffed paratha", "Vegetable thepla",
        "Sprouted moong dal", "Cucumber raita", "Tomato curry", "Plain rice with kadhi", "Jeera aloo",
        "Baingan sabzi", "Tamarind rice", "Masoor dal", "Cabbage poriyal", "Green beans sabzi",
        "Cauliflower sabzi", "Corn chaat", "Vegetable semiya", "Mint paratha", "Sweet potato curry",
        "Coconut rice", "Vegetable stew", "Chapati with methi sabzi", "Rajgira roti", "Pesarattu"
    ],
    "Muscle Gain": [
        "Boiled eggs", "Paneer paratha", "Peanut butter toast", "Banana shake", "Grilled chicken breast",
        "Moong dal cheela", "Mixed veg curry with paneer", "Soya chunks curry", "Lassi", "Dry fruits",
        "Brown rice with chicken", "Scrambled paneer", "Vegetable khichdi with ghee", "Roti with egg curry",
        "Chickpea salad", "Sweet corn with butter", "Ragi roti", "Paneer bhurji with toast", "Milk with almonds",
        "Sprouts and paneer mix", "Rajma chawal", "Stuffed chicken rolls", "Palak paneer",
        "Besan laddoo", "Masala oats with paneer", "Cheese paratha", "Vegetable biryani with curd",
        "Roti with soyachunks curry", "Peanut ladoo", "Protein bar"
    ]
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
        user_data[username]["weight_history"].append(new_weight)
        user_data[username]["weight"] = new_weight
        save_user_data(user_data)
        st.success("Weight updated successfully!")

    diet_choice = st.selectbox("Select your diet plan", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])
    if diet_choice:
        meals = {}
        foods = unique_diet_items[diet_choice]
        for i in range(7):
            meals[f"Day {i+1}"] = {
                "Breakfast": foods[(i*3) % len(foods)],
                "Lunch": foods[(i*3 + 1) % len(foods)],
                "Dinner": foods[(i*3 + 2) % len(foods)]
            }
        user_data[username]['diet_plan'] = meals
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
        Group Members: <strong>Sakshi Ughade, Dipak Walunj, Divyank Wani, Omkar Zinjurde</strong><br>
        College: <strong>Amrutvahini College of Engineering, Sangamner</strong> | Branch: <strong> Artificial Intelligence and Data Science</strong>
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
