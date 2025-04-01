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
    age = st.number_input("Age", min_value=1)
    weight = st.number_input("Weight (kg)", min_value=1)
    height = st.number_input("Height (cm)", min_value=1)
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly active", "Moderately active", "Very active"])
    health_goal = st.selectbox("Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])
    dietary_preference = st.text_input("Dietary Preferences (e.g., Vegetarian, Vegan, No Dairy)")
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
                "age": age,
                "weight": weight,
                "height": height,
                "activity_level": activity_level,
                "health_goal": health_goal,
                "dietary_preference": dietary_preference,
                "password": new_password
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

    st.markdown("<p style='text-align:right;'><a href='/' style='color:blue;'>Already have an account? Login</a></p>", unsafe_allow_html=True)

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
            st.session_state['user_data'] = user_data[username]
        else:
            st.error("Invalid credentials. Please try again.")

def generate_seven_day_diet(diet_goal):
    diet_plans = {
    "Weight Loss": {
        "Day 1": {"Breakfast": "Vegetable Upma", "Lunch": "Palak Dal with Brown Rice", "Dinner": "Grilled Tofu with Veggies"},
        "Day 2": {"Breakfast": "Moong Dal Chilla", "Lunch": "Quinoa with Vegetable Curry", "Dinner": "Vegetable Soup with Salad"},
        "Day 3": {"Breakfast": "Oats with Fresh Fruits", "Lunch": "Masoor Dal with Roti", "Dinner": "Grilled Chicken Salad"},
        "Day 4": {"Breakfast": "Poha with Peanuts", "Lunch": "Chickpea Salad with Cucumber", "Dinner": "Methi Thepla with Curd"},
        "Day 5": {"Breakfast": "Sprouts Salad with Lemon", "Lunch": "Vegetable Khichdi", "Dinner": "Grilled Fish with Steamed Vegetables"},
        "Day 6": {"Breakfast": "Idli with Coconut Chutney", "Lunch": "Rajma with Brown Rice", "Dinner": "Lentil Soup with Salad"},
        "Day 7": {"Breakfast": "Smoothie with Spinach and Banana", "Lunch": "Tofu and Broccoli Stir-Fry", "Dinner": "Grilled Paneer with Vegetables"}
    },
    "Balanced Nutrition": {
        "Day 1": {"Breakfast": "Aloo Paratha with Yogurt", "Lunch": "Rice with Dal and Vegetables", "Dinner": "Paneer Butter Masala with Roti"},
        "Day 2": {"Breakfast": "Pesarattu (Green Gram Pancake)", "Lunch": "Curry with Brown Rice", "Dinner": "Palak Paneer with Roti"},
        "Day 3": {"Breakfast": "Oats and Milk Porridge", "Lunch": "Chana Masala with Roti", "Dinner": "Vegetable Pulao with Cucumber Raita"},
        "Day 4": {"Breakfast": "Dosa with Sambar", "Lunch": "Vegetable Biryani", "Dinner": "Methi Paratha with Curd"},
        "Day 5": {"Breakfast": "Boiled Eggs with Whole Wheat Toast", "Lunch": "Dal Makhani with Jeera Rice", "Dinner": "Grilled Chicken with Veg Salad"},
        "Day 6": {"Breakfast": "Upma with Vegetables", "Lunch": "Rajma with Roti", "Dinner": "Vegetable Stir-Fry with Tofu"},
        "Day 7": {"Breakfast": "Poha with Peanuts", "Lunch": "Methi Thepla with Curd", "Dinner": "Palak Dal with Brown Rice"}
    },
    "Muscle Gain": {
        "Day 1": {"Breakfast": "Paneer Paratha with Yogurt", "Lunch": "Chicken Tikka with Quinoa", "Dinner": "Grilled Salmon with Rice"},
        "Day 2": {"Breakfast": "Oats with Peanut Butter", "Lunch": "Chicken Curry with Brown Rice", "Dinner": "Grilled Paneer with Salad"},
        "Day 3": {"Breakfast": "Boiled Eggs with Whole Wheat Toast", "Lunch": "Chickpea Salad with Quinoa", "Dinner": "Grilled Fish with Rice"},
        "Day 4": {"Breakfast": "Protein Shake with Banana", "Lunch": "Grilled Chicken with Steamed Veggies", "Dinner": "Lentil Soup with Brown Rice"},
        "Day 5": {"Breakfast": "Greek Yogurt with Almonds", "Lunch": "Vegetable Pulao with Raita", "Dinner": "Grilled Tofu Stir Fry"},
        "Day 6": {"Breakfast": "Scrambled Eggs with Toast", "Lunch": "Grilled Turkey Sandwich", "Dinner": "Fish Curry with Brown Rice"},
        "Day 7": {"Breakfast": "Cottage Cheese with Nuts", "Lunch": "Paneer Bhurji with Roti", "Dinner": "Grilled Chicken with Vegetables"}
    }
}

# Function to generate diet plan based on user's health goal
def generate_seven_day_diet(diet_goal):
    st.markdown(f"### 7-Day {diet_goal} Meal Plan:")
    
    # Display the meals for each day
    for day, meals in diet_plans[diet_goal].items():
        st.markdown(f"**{day}:**")
        st.markdown(f"  - **Breakfast:** {meals['Breakfast']}")
        st.markdown(f"  - **Lunch:** {meals['Lunch']}")
        st.markdown(f"  - **Dinner:** {meals['Dinner']}")
        st.markdown("---")


def main_app():
    st.markdown("<h1 style='color: #FF5722;'>AI-Driven Personalized Nutrition</h1>", unsafe_allow_html=True)
    st.markdown("**Developed by TechSpark Team:** Dipak Walunj, Divyank Wani, Omkar Zinjurde, and [Your Name]")
    
    if st.button("Logout", key='logout_button'):
        st.session_state['authenticated'] = False
        st.success("You have been logged out.")
        return
    
    user_info = st.session_state.get('user_data', {})
    health_goals = user_info.get("health_goal", "Balanced Nutrition")
    
    if st.button("Generate 7-Day Diet Plan", key='generate_button'):
        generate_seven_day_diet(health_goals)

if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        login_page()
    else:
        main_app()
