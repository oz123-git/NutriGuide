import streamlit as st
import json
import datetime
import random
from fpdf import FPDF

# File to store user data and diet plans
db_file = "user_data.json"
diet_plan_file = "diet_plans.json"

def load_user_data():
    try:
        with open(db_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(data):
    with open(db_file, "w") as file:
        json.dump(data, file, indent=4)

def load_diet_plans():
    try:
        with open(diet_plan_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_diet_plan(data):
    with open(diet_plan_file, "w") as file:
        json.dump(data, file, indent=4)

def generate_diet_plan(diet_goal, duration):
    plan = {
        "Weight Loss": {
            "Breakfast": [
                "Smoothie with spinach, banana, and almond milk",
                "Chia pudding with mixed berries",
                "Avocado toast with poached eggs",
                "Oats with almond milk and chia seeds",
                "Greek yogurt with honey and nuts"
            ],
            "Lunch": [
                "Grilled salmon with quinoa and mixed greens",
                "Chicken breast with sweet potato and spinach",
                "Zucchini noodles with marinara sauce and a side salad",
                "Turkey lettuce wraps with avocado and tomatoes",
                "Vegetable stir-fry with tofu"
            ],
            "Dinner": [
                "Grilled shrimp with quinoa and steamed broccoli",
                "Lentil soup with a side of whole-grain bread",
                "Baked cod with steamed vegetables and couscous",
                "Chicken curry with basmati rice",
                "Vegetable stir-fry with tofu"
            ],
            "Snack": [
                "Apple and almonds",
                "Carrot sticks with hummus",
                "Greek yogurt with berries",
                "Almonds and an orange",
                "Cottage cheese with pineapple"
            ],
            "Water": "8 glasses per day"
        },
        "Weight Gain": {
            "Breakfast": [
                "Oats with peanut butter and banana",
                "Scrambled eggs with avocado and whole wheat toast",
                "Greek yogurt with granola and honey",
                "Whole wheat pancakes with syrup and fruits",
                "Smoothie with protein powder, almond butter, and banana"
            ],
            "Lunch": [
                "Grilled steak with mashed potatoes and green beans",
                "Chicken breast with quinoa and roasted veggies",
                "Salmon with roasted vegetables and quinoa",
                "Pasta with chicken and Alfredo sauce",
                "Beef stew with carrots and potatoes"
            ],
            "Dinner": [
                "Chicken curry with basmati rice",
                "Grilled fish with steamed vegetables",
                "Lentil stew with brown rice",
                "Beef stew with vegetables",
                "Pasta with meatballs"
            ],
            "Snack": [
                "Protein shake with milk",
                "Granola bar and an apple",
                "Peanut butter with crackers",
                "Cheese and whole wheat crackers",
                "Greek yogurt with honey"
            ],
            "Water": "10 glasses per day"
        },
        "Balanced Nutrition": {
            "Breakfast": [
                "Omelette with spinach, mushrooms, and cheese",
                "Greek yogurt with berries and chia seeds",
                "Avocado toast with poached eggs",
                "Whole wheat toast with peanut butter and banana",
                "Smoothie with kale, apple, and almond milk"
            ],
            "Lunch": [
                "Grilled chicken salad with olive oil dressing",
                "Turkey and avocado wrap with whole wheat tortilla",
                "Lentil soup with a side of whole-grain bread",
                "Quinoa salad with chickpeas, cucumbers, and tomatoes",
                "Tuna salad with mixed greens"
            ],
            "Dinner": [
                "Grilled fish with brown rice and steamed broccoli",
                "Grilled shrimp with quinoa and steamed broccoli",
                "Lentil soup with a side of whole-grain bread",
                "Baked chicken with sweet potato and asparagus",
                "Vegetable stir-fry with tofu"
            ],
            "Snack": [
                "Carrot and celery sticks with hummus",
                "Almonds and an apple",
                "Cottage cheese with pineapple",
                "Granola bar",
                "Rice cakes with almond butter"
            ],
            "Water": "8-10 glasses per day"
        }
    }

    days = {"1 Week": 7, "2 Weeks": 14, "1 Month": 30}
    total_days = days[duration]
    
    full_plan = []
    for meal_type in ["Breakfast", "Lunch", "Dinner", "Snack"]:
        meals = plan[diet_goal][meal_type]
        meal_plan = random.sample(meals, len(meals))  # Shuffle meals to add variety
        while len(meal_plan) < total_days:
            meal_plan.extend(random.sample(meals, len(meals)))
        plan[diet_goal][meal_type] = meal_plan[:total_days]
    
    # Generate the full plan for the month
    for i in range(total_days):
        daily_plan = f"Day {i+1}:\n"
        for meal_type in ["Breakfast", "Lunch", "Dinner", "Snack"]:
            daily_plan += f"{meal_type}: {plan[diet_goal][meal_type][i]}\n"
        daily_plan += f"Water Intake: {plan[diet_goal]['Water']}\n\n"
        full_plan.append(daily_plan)
    
    return full_plan

def create_pdf(diet_plan, filename="diet_plan.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Personalized Diet Plan", ln=True, align="C")
    pdf.ln(10)
    
    for day in diet_plan:
        pdf.multi_cell(0, 10, day)
    
    pdf.output(filename)
    return filename

def register_page():
    st.markdown("<h1 style='color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_register.jpg.webp")
    name = st.text_input("Name")
    email = st.text_input("Email ID")
    phone = st.text_input("Phone Number")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type='password')
    
    if st.button("Register", key='register_button'):
        user_data = load_user_data()
        if new_username in user_data:
            st.error("Username already exists. Please choose another.")
        else:
            user_data[new_username] = {"name": name, "email": email, "phone": phone, "password": new_password, "last_activity": "No previous activity"}
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")

def login_page():
    st.markdown("<h1 style='color: #2196F3;'>AI for Personalized Nutrition - Login</h1>", unsafe_allow_html=True)
    st.image("image/nutrition_login.jpg.webp")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login", key='login_button'):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.success(f"Welcome back, {user_data[username]['name']}!")
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
        else:
            st.error("Invalid credentials. Please try again.")
    st.markdown("<p style='text-align: right;'><a href='#' style='color: #2196F3;'>Create Account</a></p>", unsafe_allow_html=True)

def main_app():
    st.markdown("<h1 style='color: #FF5722;'>AI for Personalized Nutrition</h1>", unsafe_allow_html=True)
    
    if st.button("Logout", key='logout_button'):
        st.session_state['authenticated'] = False
        st.success("You have been logged out.")
        return
    
    username = st.session_state.get('username', None)
    user_data = load_user_data()
    
    if username and username in user_data:
        st.info(f"Last Activity: {user_data[username].get('last_activity', 'No previous activity')}")
    
    age = st.number_input("Enter your age", min_value=1)
    height = st.number_input("Enter your height (cm)", min_value=50)
    weight = st.number_input("Enter your weight (kg)", min_value=10)
    dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    diet_goal = st.selectbox("Diet Goal", ["Weight Loss", "Weight Gain", "Balanced Nutrition"])
    diet_duration = st.selectbox("Select Diet Duration", ["1 Week", "2 Weeks", "1 Month"])
    
    if st.button("Get Nutrition Plan", key='plan_button'):
        plan = generate_diet_plan(diet_goal, diet_duration)
        st.success(f"Your personalized diet plan for {diet_duration}:")
        for day in plan:
            st.write(day)
        
        # Save the diet plan for future use
        if username and username in user_data:
            user_data[username]['last_activity'] = f"Generated a {diet_duration} {diet_goal} diet plan on {datetime.date.today()}"
            save_user_data(user_data)
        
        # Provide PDF download option
        pdf_filename = create_pdf(plan)
        st.download_button("Download Diet Plan as PDF", pdf_filename)
    
    st.write("---")
    st.markdown("<p style='color: #3F51B5;'><b>Project by TechSpark Group</b></p>", unsafe_allow_html=True)
    st.markdown("- Dipak Walunj\n- Divyank Wani\n- Omkar Zinjurde", unsafe_allow_html=True)

if __name__ == "__main__":
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if st.session_state['authenticated']:
        main_app()
    else:
        page = st.sidebar.radio("Choose an option", ["Login", "Register"])
        if page == "Login":
            login_page()
        else:
            register_page()
