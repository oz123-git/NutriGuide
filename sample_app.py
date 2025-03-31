import streamlit as st
import json
import datetime
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
            "Day 1": {
                "Breakfast": "Poha with vegetables",
                "Lunch": "Grilled chicken with roti and salad",
                "Dinner": "Dal Tadka with brown rice",
                "Snack": "Cucumber and carrot sticks",
                "Water": "8 glasses per day"
            },
            "Day 2": {
                "Breakfast": "Vegetable upma",
                "Lunch": "Palak paneer with chapati",
                "Dinner": "Vegetable soup and a small bowl of brown rice",
                "Snack": "Apple and almonds",
                "Water": "8 glasses per day"
            },
            "Day 3": {
                "Breakfast": "Oats porridge with nuts",
                "Lunch": "Tandoori chicken with green salad",
                "Dinner": "Moong dal khichdi with a side of curd",
                "Snack": "Greek yogurt with honey",
                "Water": "8 glasses per day"
            }
        },
        "Weight Gain": {
            "Day 1": {
                "Breakfast": "Aloo paratha with curd",
                "Lunch": "Paneer butter masala with naan",
                "Dinner": "Chicken curry with white rice",
                "Snack": "Peanut butter with whole wheat bread",
                "Water": "10 glasses per day"
            },
            "Day 2": {
                "Breakfast": "Masala dosa with sambar and coconut chutney",
                "Lunch": "Mutton curry with steamed rice",
                "Dinner": "Pasta with paneer and vegetable stir fry",
                "Snack": "Banana and milkshake",
                "Water": "10 glasses per day"
            },
            "Day 3": {
                "Breakfast": "Pancakes with ghee and honey",
                "Lunch": "Chole bhature",
                "Dinner": "Biryani with raita",
                "Snack": "Protein shake with milk",
                "Water": "10 glasses per day"
            }
        },
        "Balanced Nutrition": {
            "Day 1": {
                "Breakfast": "Oats idli with chutney",
                "Lunch": "Grilled fish with brown rice and vegetables",
                "Dinner": "Vegetable curry with roti",
                "Snack": "Paneer tikka",
                "Water": "8-10 glasses per day"
            },
            "Day 2": {
                "Breakfast": "Moong dal cheela with green chutney",
                "Lunch": "Rajma chawal with a side of salad",
                "Dinner": "Tofu stir fry with quinoa",
                "Snack": "Mixed nuts",
                "Water": "8-10 glasses per day"
            },
            "Day 3": {
                "Breakfast": "Dosa with sambar and coconut chutney",
                "Lunch": "Lentil soup with chapati",
                "Dinner": "Grilled chicken with steamed vegetables",
                "Snack": "Fruit salad with yogurt",
                "Water": "8-10 glasses per day"
            }
        }
    }

    days = {"1 Week": 7, "2 Weeks": 14, "1 Month": 30}
    full_plan = []
    for i in range(days[duration]):
        day_name = f"Day {i+1}"
        day_plan = plan[diet_goal].get(day_name, {})
        daily_plan = f"**{day_name}**\n"
        daily_plan += f"**Breakfast:** {day_plan.get('Breakfast', 'N/A')}\n"
        daily_plan += f"**Lunch:** {day_plan.get('Lunch', 'N/A')}\n"
        daily_plan += f"**Dinner:** {day_plan.get('Dinner', 'N/A')}\n"
        daily_plan += f"**Snack:** {day_plan.get('Snack', 'N/A')}\n"
        daily_plan += f"**Water Intake:** {day_plan.get('Water', 'N/A')}\n\n"
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
            st.markdown(day)
        
        # Save the diet plan for future use
        if username and username in user_data:
            user_data[username]['last_activity'] = f"Generated a {diet_duration} {diet_goal} diet plan on {datetime.date.today()}"
            save_user_data(user_data)
        
        # Provide PDF download option
        pdf_filename = create_pdf(plan)
        st.download_button("Download Diet Plan as PDF", pdf_filename)
    
    st.write("---")
    st.markdown("<p style='color: #3F51B5;'><b>Project by TechSpark Group</b></p>", unsafe_allow_html=True)
