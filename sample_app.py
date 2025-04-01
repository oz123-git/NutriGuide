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
            "Day 1": {
                "Breakfast": "Poha with vegetables",
                "Lunch": "Dal khichdi with curd",
                "Dinner": "Vegetable soup"
            },
            "Day 2": {
                "Breakfast": "Oatmeal with fruits",
                "Lunch": "Quinoa salad",
                "Dinner": "Grilled chicken with veggies"
            },
            "Day 3": {
                "Breakfast": "Scrambled eggs with spinach",
                "Lunch": "Vegetable stir fry with rice",
                "Dinner": "Soup and toast"
            },
            "Day 4": {
                "Breakfast": "Greek yogurt with nuts",
                "Lunch": "Chickpea salad",
                "Dinner": "Grilled fish with steamed veggies"
            },
            "Day 5": {
                "Breakfast": "Smoothie with spinach, banana, and almond milk",
                "Lunch": "Lentil soup with a side of salad",
                "Dinner": "Cauliflower rice with stir-fried tofu"
            },
            "Day 6": {
                "Breakfast": "Chia seeds pudding with berries",
                "Lunch": "Grilled chicken salad",
                "Dinner": "Zucchini noodles with marinara sauce"
            },
            "Day 7": {
                "Breakfast": "Avocado toast with poached eggs",
                "Lunch": "Vegetable stir fry with quinoa",
                "Dinner": "Steamed vegetables with a side of grilled salmon"
            }
        },
        "Balanced Nutrition": {
            "Day 1": {
                "Breakfast": "Pancakes with honey",
                "Lunch": "Rice, dal, and veggies",
                "Dinner": "Grilled chicken with mashed potatoes"
            },
            "Day 2": {
                "Breakfast": "Smoothie with almond milk",
                "Lunch": "Lentil soup with whole wheat bread",
                "Dinner": "Fish curry with brown rice"
            },
            "Day 3": {
                "Breakfast": "Omelet with whole wheat toast",
                "Lunch": "Vegetable pulao with yogurt",
                "Dinner": "Grilled paneer with quinoa"
            },
            "Day 4": {
                "Breakfast": "Cornflakes with milk",
                "Lunch": "Dal, roti, and sabzi",
                "Dinner": "Chicken stew with brown rice"
            },
            "Day 5": {
                "Breakfast": "Idli with coconut chutney",
                "Lunch": "Chickpea salad with yogurt",
                "Dinner": "Vegetable soup with bread"
            },
            "Day 6": {
                "Breakfast": "Fruit salad with yogurt",
                "Lunch": "Grilled fish with rice",
                "Dinner": "Paneer tikka with roti"
            },
            "Day 7": {
                "Breakfast": "Poha with nuts",
                "Lunch": "Rajma rice",
                "Dinner": "Grilled vegetables with couscous"
            }
        },
        "Muscle Gain": {
            "Day 1": {
                "Breakfast": "Scrambled eggs with toast",
                "Lunch": "Grilled chicken with quinoa",
                "Dinner": "Salmon with roasted potatoes"
            },
            "Day 2": {
                "Breakfast": "Protein shake with banana",
                "Lunch": "Lentil soup with brown rice",
                "Dinner": "Grilled steak with vegetables"
            },
            "Day 3": {
                "Breakfast": "Oats with peanut butter",
                "Lunch": "Chicken breast with sweet potato",
                "Dinner": "Tofu stir-fry with rice"
            },
            "Day 4": {
                "Breakfast": "Greek yogurt with almonds",
                "Lunch": "Fish with quinoa and salad",
                "Dinner": "Grilled paneer with whole wheat bread"
            },
            "Day 5": {
                "Breakfast": "Omelet with cheese",
                "Lunch": "Beef stir fry with rice",
                "Dinner": "Baked chicken with mashed potatoes"
            },
            "Day 6": {
                "Breakfast": "Protein pancakes",
                "Lunch": "Grilled turkey sandwich",
                "Dinner": "Vegetable curry with brown rice"
            },
            "Day 7": {
                "Breakfast": "Cottage cheese with nuts",
                "Lunch": "Salmon with quinoa and greens",
                "Dinner": "Steak with roasted veggies"
            }
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

    # Collect user details
    age = st.number_input("Enter your age", min_value=1)
    height = st.number_input("Enter your height (cm)", min_value=50)
    weight = st.number_input("Enter your weight (kg)", min_value=10)
    gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
    dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    health_goals = st.selectbox("Select Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])

    # Generate Diet Plan
    if st.button("Generate 7-Day Diet Plan", key='generate_button'):
        generate_seven_day_diet(health_goals)

    # Project Info
    st.write("---")
    st.markdown("<p style='color: #3F51B5;'><b>Project by TechSpark Group</b></p>", unsafe_allow_html=True)
    st.markdown("- Dipak Walunj (Roll No. 60)\n- Divyank Wani (Roll No. 61)\n- Omkar Zinjurde (Roll No. 63)\n- Sakshi Ughade (Roll No. 73)", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Amrutvahini College of Engineering, Sangamner</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Contact: techspark.support@gmail.com</p>", unsafe_allow_html=True)

    # Account creation button at the bottom-right
    
