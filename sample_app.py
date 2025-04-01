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

def login_page():
    st.markdown("<h1 style='color: #4CAF50;'>Login Page</h1>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.session_state['authenticated'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")

def register_page():
    st.markdown("<h1 style='color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_register.jpg.webp")
    
    name = st.text_input("Name")
    email = st.text_input("Email ID")
    phone = st.text_input("Phone Number")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type='password')

    if st.button("Register"):
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

def generate_seven_day_diet(diet_goal):
    # Define the meal plans for different diet goals
    daily_menus = {
        "Weight Loss": {
            "Day 1": {"Breakfast": "Poha with vegetables and green tea", "Lunch": "Dal khichdi with curd", "Dinner": "Vegetable soup"},
            "Day 2": {"Breakfast": "Oatmeal with fruits", "Lunch": "Quinoa salad", "Dinner": "Grilled chicken with veggies"},
            "Day 3": {"Breakfast": "Scrambled eggs with spinach", "Lunch": "Vegetable stir fry with rice", "Dinner": "Soup and toast"},
            "Day 4": {"Breakfast": "Greek yogurt with nuts", "Lunch": "Chickpea salad", "Dinner": "Grilled fish with steamed veggies"},
            "Day 5": {"Breakfast": "Smoothie with spinach, banana, and almond milk", "Lunch": "Lentil soup with a side of salad", "Dinner": "Cauliflower rice with stir-fried tofu"},
            "Day 6": {"Breakfast": "Chia seeds pudding with berries", "Lunch": "Grilled chicken salad", "Dinner": "Zucchini noodles with marinara sauce"},
            "Day 7": {"Breakfast": "Avocado toast with poached eggs", "Lunch": "Vegetable stir fry with quinoa", "Dinner": "Steamed vegetables with a side of grilled salmon"}
        },
        "Balanced Nutrition": {
            "Day 1": {"Breakfast": "Eggs and toast", "Lunch": "Chicken salad", "Dinner": "Grilled salmon with quinoa"},
            "Day 2": {"Breakfast": "Greek yogurt with honey and granola", "Lunch": "Tuna sandwich with veggies", "Dinner": "Stir-fried chicken with brown rice"},
            "Day 3": {"Breakfast": "Avocado toast with eggs", "Lunch": "Vegetable wrap with hummus", "Dinner": "Baked salmon with sweet potatoes"},
            "Day 4": {"Breakfast": "Smoothie with spinach, banana, and protein powder", "Lunch": "Turkey sandwich with a side salad", "Dinner": "Spaghetti with marinara sauce"},
            "Day 5": {"Breakfast": "Whole grain toast with peanut butter", "Lunch": "Chicken Caesar salad", "Dinner": "Grilled shrimp with vegetables"},
            "Day 6": {"Breakfast": "Oatmeal with almonds and chia seeds", "Lunch": "Roast beef with a side of veggies", "Dinner": "Grilled chicken with roasted potatoes"},
            "Day 7": {"Breakfast": "Egg and vegetable omelet", "Lunch": "Quinoa salad with feta", "Dinner": "Baked chicken with steamed broccoli"}
        },
        "Muscle Gain": {
            "Day 1": {"Breakfast": "Omelette with whole grain bread", "Lunch": "Chicken with rice", "Dinner": "Protein shake with nuts"},
            "Day 2": {"Breakfast": "Greek yogurt with protein powder and fruit", "Lunch": "Turkey sandwich with whole-grain bread", "Dinner": "Steak with quinoa and veggies"},
            "Day 3": {"Breakfast": "Scrambled eggs with avocado and toast", "Lunch": "Chicken and vegetable stir fry with brown rice", "Dinner": "Salmon with sweet potatoes and asparagus"},
            "Day 4": {"Breakfast": "Protein pancakes with berries", "Lunch": "Grilled chicken with quinoa and spinach", "Dinner": "Lentil soup with grilled chicken"},
            "Day 5": {"Breakfast": "Peanut butter smoothie with protein powder", "Lunch": "Tuna salad with avocado and whole grain crackers", "Dinner": "Grilled pork chops with mashed potatoes"},
            "Day 6": {"Breakfast": "Egg white omelette with veggies", "Lunch": "Chicken burrito bowl with brown rice", "Dinner": "Grilled chicken with sweet potato fries"},
            "Day 7": {"Breakfast": "Oats with milk, protein powder, and banana", "Lunch": "Grilled shrimp with rice and vegetables", "Dinner": "Beef stir fry with quinoa"}
        }
    }

    # Show the diet plan based on the goal
    st.markdown(f"### 7-Day {diet_goal} Meal Plan (Breakfast, Lunch, and Dinner):")
    for day, meals in daily_menus[diet_goal].items():
        st.markdown(f"**{day}:**")
        for meal_type, meal_info in meals.items():
            st.markdown(f"  - **{meal_type}:** {meal_info}")
        st.markdown("---")
    
    st.markdown("### This meal plan repeats every week.")

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
    st.markdown("- Dipak Walunj\n- Divyank Wani\n- Omkar Zinjurde\n- Sakshi Ughade", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Amrutvahini College of Engineering, Sangamner</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Contact: techspark.support@gmail.com</p>", unsafe_allow_html=True)

    # Account creation button at the bottom-right
    st.markdown("""
        <style>
            .stButton > button {
                position: fixed;
                bottom: 10px;
                right: 10px;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)
    if st.button("Create Account"):
        register_page()

if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_page()
    else:
        main_app()
