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

# Function to calculate caloric needs
def calculate_bmr(weight, height, age, activity_level):
    bmr = 10 * weight + 6.25 * height - 5 * age + 5  # Mifflin-St Jeor Equation for males
    activity_multiplier = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    return bmr * activity_multiplier[activity_level]

# Diet plans
diet_plans = {
    "Weight Loss": {
        "Day 1": {"Breakfast": "Poha", "Lunch": "Dal khichdi", "Dinner": "Vegetable soup"},
        "Day 2": {"Breakfast": "Oatmeal", "Lunch": "Quinoa salad", "Dinner": "Grilled chicken"},
    },
    "Balanced Nutrition": {
        "Day 1": {"Breakfast": "Pancakes", "Lunch": "Rice & Dal", "Dinner": "Grilled Chicken"},
        "Day 2": {"Breakfast": "Smoothie", "Lunch": "Lentil Soup", "Dinner": "Fish Curry"},
    },
    "Muscle Gain": {
        "Day 1": {"Breakfast": "Eggs & Toast", "Lunch": "Chicken & Quinoa", "Dinner": "Salmon & Potatoes"},
        "Day 2": {"Breakfast": "Protein Shake", "Lunch": "Lentil Soup", "Dinner": "Grilled Steak"},
    }
}

# Register Page
def register_page():
    st.markdown("<h1 style='color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)
    
    name = st.text_input("Name")
    email = st.text_input("Email ID")
    phone = st.text_input("Phone Number")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type='password')

    age = st.number_input("Age", min_value=1, max_value=120)
    height = st.number_input("Height (cm)", min_value=50, max_value=250)
    weight = st.number_input("Weight (kg)", min_value=10, max_value=300)
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])

    if st.button("Register"):
        if not all([name, email, phone, new_username, new_password, age, height, weight, activity_level]):
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
                "age": age,
                "height": height,
                "weight": weight,
                "activity_level": activity_level,
                "last_meal": {"Breakfast": "", "Lunch": "", "Dinner": ""},
                "diet_plan": {}
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")
            st.session_state['page'] = "login"

# Login Page with Account Creation Button
def login_page():
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

    # Add "Create Account" button
    if st.button("Create Account"):
        st.session_state['page'] = "register"

# Main App: Diet Plan and Meal Tracking
def main_app():
    st.markdown("<h1 style='color: #FF5722;'>AI-Driven Personalized Nutrition</h1>", unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['page'] = "login"
        return

    user_data = load_user_data()
    username = st.session_state['username']
    
    if username not in user_data:
        st.error("User data not found. Please log in again.")
        return
    
    if any(k not in user_data[username] for k in ["weight", "height", "age", "activity_level"]):
        st.error("Incomplete user data. Please update your profile.")
        return

    weight = user_data[username].get("weight", 70)
    height = user_data[username].get("height", 170)
    age = user_data[username].get("age", 30)
    activity_level = user_data[username].get("activity_level", "Sedentary")

    # Calculate and display caloric needs
    tdee = calculate_bmr(weight, height, age, activity_level)
    st.markdown(f"**Estimated Daily Caloric Needs:** {round(tdee)} kcal")

    # Select diet plan
    diet_choice = st.selectbox("Select your diet plan", ["Weight Loss", "Balanced Nutrition", "Muscle Gain"])
    if diet_choice:
        user_data[username]['diet_plan'] = diet_plans[diet_choice]
        save_user_data(user_data)
        st.success(f"Your {diet_choice} diet plan has been saved!")

    # Display last meal
    last_meal = user_data[username].get("last_meal", {"Breakfast": "No record", "Lunch": "No record", "Dinner": "No record"})
    st.markdown("*Last Recorded Meals:*")
    st.markdown(f"- *Breakfast:* {last_meal['Breakfast']}")
    st.markdown(f"- *Lunch:* {last_meal['Lunch']}")
    st.markdown(f"- *Dinner:* {last_meal['Dinner']}")

    # Meal Input
    breakfast = st.text_input("Enter your Breakfast details")
    lunch = st.text_input("Enter your Lunch details")
    dinner = st.text_input("Enter your Dinner details")
    
    if st.button("Save Meals"):
        user_data[username]["last_meal"] = {"Breakfast": breakfast, "Lunch": lunch, "Dinner": dinner}
        save_user_data(user_data)
        st.success("Meals saved successfully!")

# Main function controlling app navigation
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
