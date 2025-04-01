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
    daily_menus = {
        "Weight Loss": {  # Lower-calorie meals
            "Day 1": {"Breakfast": "Poha with green tea", "Lunch": "Dal khichdi with curd", "Dinner": "Vegetable soup"},
            "Day 2": {"Breakfast": "Oatmeal with fruits", "Lunch": "Quinoa salad", "Dinner": "Grilled chicken with veggies"},
            "Day 3": {"Breakfast": "Scrambled eggs with spinach", "Lunch": "Vegetable stir fry with rice", "Dinner": "Soup and toast"},
            "Day 4": {"Breakfast": "Greek yogurt with nuts", "Lunch": "Chickpea salad", "Dinner": "Grilled fish with veggies"},
            "Day 5": {"Breakfast": "Smoothie with banana and almond milk", "Lunch": "Lentil soup with salad", "Dinner": "Tofu stir-fry with cauliflower rice"},
            "Day 6": {"Breakfast": "Chia pudding with berries", "Lunch": "Grilled chicken salad", "Dinner": "Zucchini noodles with marinara sauce"},
            "Day 7": {"Breakfast": "Avocado toast with eggs", "Lunch": "Quinoa and veggie stir-fry", "Dinner": "Steamed fish with vegetables"}
        },
        "Balanced Nutrition": {  # Well-rounded meals
            "Day 1": {"Breakfast": "Whole wheat toast with peanut butter", "Lunch": "Brown rice with dal and salad", "Dinner": "Paneer curry with roti"},
            "Day 2": {"Breakfast": "Fruit smoothie with protein", "Lunch": "Grilled chicken with quinoa", "Dinner": "Vegetable curry with rice"},
            "Day 3": {"Breakfast": "Oats with nuts and honey", "Lunch": "Chickpea salad", "Dinner": "Grilled salmon with vegetables"},
            "Day 4": {"Breakfast": "Multigrain sandwich with avocado", "Lunch": "Egg curry with brown rice", "Dinner": "Vegetable stir-fry"},
            "Day 5": {"Breakfast": "Greek yogurt with granola", "Lunch": "Lentil soup with a side of whole grain bread", "Dinner": "Chicken and vegetable stew"},
            "Day 6": {"Breakfast": "Banana and nut smoothie", "Lunch": "Paneer tikka with mixed greens", "Dinner": "Stir-fried tofu with vegetables"},
            "Day 7": {"Breakfast": "Scrambled eggs with toast", "Lunch": "Brown rice with grilled fish", "Dinner": "Vegetable quinoa bowl"}
        },
        "Muscle Gain": {  # High-protein meals
            "Day 1": {"Breakfast": "Omelet with whole wheat bread", "Lunch": "Grilled chicken with brown rice", "Dinner": "Fish curry with quinoa"},
            "Day 2": {"Breakfast": "Protein smoothie", "Lunch": "Egg fried rice with vegetables", "Dinner": "Paneer tikka with mixed greens"},
            "Day 3": {"Breakfast": "Peanut butter toast with banana", "Lunch": "Grilled steak with veggies", "Dinner": "Dal and rice with roti"},
            "Day 4": {"Breakfast": "Greek yogurt with almonds", "Lunch": "Salmon with quinoa", "Dinner": "Chicken stir-fry with brown rice"},
            "Day 5": {"Breakfast": "Scrambled eggs with toast", "Lunch": "Grilled fish with spinach", "Dinner": "Mutton curry with rice"},
            "Day 6": {"Breakfast": "Oats with whey protein", "Lunch": "Paneer bhurji with roti", "Dinner": "Beef and vegetable stir-fry"},
            "Day 7": {"Breakfast": "Avocado smoothie", "Lunch": "Grilled chicken with roasted potatoes", "Dinner": "Egg curry with brown rice"}
        }
    }
    st.markdown(f"### 7-Day {diet_goal} Meal Plan:")
    for day, meals in daily_menus[diet_goal].items():
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
