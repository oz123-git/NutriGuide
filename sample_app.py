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

# Login Page
def login_page():
    st.markdown("<h1 style='color: #4CAF50;'>Login</h1>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.session_state['page'] = "main"
            st.session_state['username'] = username
        else:
            st.error("Invalid username or password")
    
    if st.button("Create Account"):
        st.session_state['page'] = "register"

# Register Page
def register_page():
    st.markdown("<h1 style='color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_register.jpg.webp")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (cm)", min_value=50, max_value=250, step=1)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=200, step=1)
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    health_goal = st.selectbox("Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])
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
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
                "activity_level": activity_level,
                "health_goal": health_goal,
                "password": new_password,
                "diet_plan": diet_plans.get(health_goal, {})
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")
            st.session_state['page'] = "login"

# Main Dashboard
def main_dashboard():
    st.write(f"Welcome {st.session_state.get('username', 'User')} to AI Nutrition App")
    user_data = load_user_data()
    username = st.session_state.get('username')
    if username in user_data:
        user_info = user_data[username]
        st.write(f"**Age:** {user_info['age']} | **Height:** {user_info['height']} cm | **Weight:** {user_info['weight']} kg")
        st.write(f"**Activity Level:** {user_info['activity_level']} | **Health Goal:** {user_info['health_goal']}")
        st.write("### Your Diet Plan")
        diet_plan = user_info.get("diet_plan", {})
        for day, meals in diet_plan.items():
            st.write(f"**{day}**")
            for meal, item in meals.items():
                st.write(f"- {meal}: {item}")

# Main function
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    if st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'register':
        register_page()
    elif st.session_state['page'] == 'main':
        main_dashboard()

if __name__ == "__main__":
    main()
