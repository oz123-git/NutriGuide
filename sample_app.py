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

# Register Page
def register_page():
    st.markdown("<h1 style='color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)
    name = st.text_input("Name")
    email = st.text_input("Email ID")
    age = st.text_input("Age")
    height = st.text_input("Height (cm)")
    weight = st.text_input("Weight (kg)")
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    health_goal = st.selectbox("Health Goal", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])
    dietary_preference = st.text_input("Dietary Preferences (e.g. Vegetarian, Vegan, etc.)")
    medical_conditions = st.text_input("Medical Conditions (if any)")
    allergies = st.text_input("Allergies (if any)")
    eating_schedule = st.text_input("Eating Schedule (e.g. 3 meals, 5 small meals, etc.)")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type='password')

    if st.button("Register"):
        if not all([name, email, age, height, weight, new_username, new_password]):
            st.error("All fields are required!")
            return
        
        user_data = load_user_data()
        
        if new_username in user_data:
            st.error("Username already exists. Please choose another.")
        else:
            user_data[new_username] = {
                "name": name,
                "email": email,
                "age": age,
                "height": height,
                "weight": weight,
                "activity_level": activity_level,
                "health_goal": health_goal,
                "dietary_preference": dietary_preference,
                "medical_conditions": medical_conditions,
                "allergies": allergies,
                "eating_schedule": eating_schedule,
                "password": new_password,
                "diet_plan": diet_plans[health_goal]
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")
            st.session_state['page'] = "login"

# Display Group Members
def display_team():
    st.markdown("## TechSpark Group Members")
    st.markdown("- **Dipak Walunj (Roll No. 60)**")
    st.markdown("- **Divyank Wani (Roll No. 61)**")
    st.markdown("- **Omkar Zinjurde (Roll No. 63)**")
    st.markdown("- **Sakshi Ughade (Roll No. 73)**")

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if st.session_state['page'] == 'register':
        register_page()
    else:
        display_team()

if __name__ == "__main__":
    main()
