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
    
    name = st.text_input("Name")
    email = st.text_input("Email ID")
    phone = st.text_input("Phone Number")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type='password')

    if st.button("Register", key='register_button'):
        if not name or not email or not phone or not new_username or not new_password:
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
                "password": new_password
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

def login_page():
    st.markdown("<h1 style='color: #2196F3;'>AI Nutrition - Login</h1>", unsafe_allow_html=True)
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

def generate_seven_day_diet(diet_goal):
    diet_plans = {
        "Weight Loss": {
            "Day 1": {"Breakfast": "Oatmeal with fruits", "Lunch": "Grilled chicken salad", "Dinner": "Vegetable soup"},
            "Day 2": {"Breakfast": "Smoothie with spinach and banana", "Lunch": "Quinoa salad", "Dinner": "Grilled fish with veggies"},
            "Day 3": {"Breakfast": "Boiled eggs with toast", "Lunch": "Chickpea salad", "Dinner": "Soup and steamed vegetables"},
            "Day 4": {"Breakfast": "Greek yogurt with nuts", "Lunch": "Lentil soup with a side of brown rice", "Dinner": "Grilled tofu with stir-fry veggies"},
            "Day 5": {"Breakfast": "Avocado toast with poached eggs", "Lunch": "Vegetable stir fry with rice", "Dinner": "Steamed vegetables with fish"},
            "Day 6": {"Breakfast": "Chia pudding with berries", "Lunch": "Grilled chicken wrap", "Dinner": "Zucchini noodles with marinara sauce"},
            "Day 7": {"Breakfast": "Scrambled eggs with spinach", "Lunch": "Quinoa bowl with mixed veggies", "Dinner": "Lentil soup with salad"}
        },
        "Balanced Nutrition": {
            "Day 1": {"Breakfast": "Pancakes with honey", "Lunch": "Rice, dal, and veggies", "Dinner": "Grilled chicken with mashed potatoes"},
            "Day 2": {"Breakfast": "Smoothie with almond milk", "Lunch": "Lentil soup with whole wheat bread", "Dinner": "Fish curry with brown rice"},
            "Day 3": {"Breakfast": "Omelet with whole wheat toast", "Lunch": "Vegetable pulao with yogurt", "Dinner": "Grilled paneer with quinoa"},
            "Day 4": {"Breakfast": "Cornflakes with milk", "Lunch": "Dal, roti, and sabzi", "Dinner": "Chicken stew with brown rice"},
            "Day 5": {"Breakfast": "Idli with coconut chutney", "Lunch": "Chickpea salad with yogurt", "Dinner": "Vegetable soup with bread"},
            "Day 6": {"Breakfast": "Fruit salad with yogurt", "Lunch": "Grilled fish with rice", "Dinner": "Paneer tikka with roti"},
            "Day 7": {"Breakfast": "Poha with nuts", "Lunch": "Rajma rice", "Dinner": "Grilled vegetables with couscous"}
        },
        "Muscle Gain": {
            "Day 1": {"Breakfast": "Scrambled eggs with toast", "Lunch": "Grilled chicken with quinoa", "Dinner": "Salmon with roasted potatoes"},
            "Day 2": {"Breakfast": "Protein shake with banana", "Lunch": "Lentil soup with brown rice", "Dinner": "Grilled steak with vegetables"},
            "Day 3": {"Breakfast": "Oats with peanut butter", "Lunch": "Chicken breast with sweet potato", "Dinner": "Tofu stir-fry with rice"},
            "Day 4": {"Breakfast": "Greek yogurt with almonds", "Lunch": "Fish with quinoa and salad", "Dinner": "Grilled paneer with whole wheat bread"},
            "Day 5": {"Breakfast": "Omelet with cheese", "Lunch": "Beef stir fry with rice", "Dinner": "Baked chicken with mashed potatoes"},
            "Day 6": {"Breakfast": "Protein pancakes", "Lunch": "Grilled turkey sandwich", "Dinner": "Vegetable curry with brown rice"},
            "Day 7": {"Breakfast": "Cottage cheese with nuts", "Lunch": "Salmon with quinoa and greens", "Dinner": "Steak with roasted veggies"}
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

    if st.button("Logout", key='logout_button'):
        st.session_state['authenticated'] = False
        st.success("You have been logged out.")
        return

    health_goals = st.selectbox("Select Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])

    if st.button("Generate 7-Day Diet Plan", key='generate_button'):
        generate_seven_day_diet(health_goals)

if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_page()
    else:
        main_app()
