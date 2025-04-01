import streamlit as st
import json

# File to store user data
db_file = "user_data.json"

def load_user_data():
    try:
        with open(db_file, "r") as file:
            return json.load(file)
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
    st.markdown("<h1 style='color: #2196F3;'>AI Nutrition Chatbot - Login</h1>", unsafe_allow_html=True)
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

    # Create account link at the bottom right
    st.markdown(
        "<p style='position: absolute; bottom: 20px; right: 20px;'><a href='#' style='color: #4CAF50;'>Create an Account</a></p>", 
        unsafe_allow_html=True
    )

def generate_seven_day_diet(diet_goal):
    # Define the meal plans with calories for different diet goals
    daily_menus = {
        "Weight Loss": {
            "Day 1": {
                "Breakfast": {"meal": "Poha with vegetables and green tea", "calories": 250},
                "Lunch": {"meal": "Dal khichdi with curd", "calories": 350},
                "Dinner": {"meal": "Vegetable soup", "calories": 150}
            },
            "Day 2": {
                "Breakfast": {"meal": "Oats porridge with nuts", "calories": 300},
                "Lunch": {"meal": "Paneer butter masala with naan", "calories": 450},
                "Dinner": {"meal": "Sprouts salad", "calories": 200}
            },
            "Day 3": {
                "Breakfast": {"meal": "Masala dosa with chutney", "calories": 350},
                "Lunch": {"meal": "Rajma chawal with salad", "calories": 400},
                "Dinner": {"meal": "Grilled fish with vegetables", "calories": 300}
            },
            "Day 4": {
                "Breakfast": {"meal": "Oats idli with chutney", "calories": 280},
                "Lunch": {"meal": "Chole bhature", "calories": 500},
                "Dinner": {"meal": "Fruit salad with yogurt", "calories": 180}
            },
            "Day 5": {
                "Breakfast": {"meal": "Pesarattu with chutney", "calories": 300},
                "Lunch": {"meal": "Paneer tikka with salad", "calories": 350},
                "Dinner": {"meal": "Vegetable biryani with raita", "calories": 400}
            },
            "Day 6": {
                "Breakfast": {"meal": "Moong dal chilla with mint chutney", "calories": 250},
                "Lunch": {"meal": "Aloo paratha with curd", "calories": 400},
                "Dinner": {"meal": "Lentil soup with bread", "calories": 250}
            },
            "Day 7": {
                "Breakfast": {"meal": "Dhokla with chutney", "calories": 200},
                "Lunch": {"meal": "Vegetable pulao with raita", "calories": 350},
                "Dinner": {"meal": "Grilled chicken with vegetables", "calories": 350}
            }
        },
        "Balanced Nutrition": {
            "Day 1": {
                "Breakfast": {"meal": "Oats idli with chutney", "calories": 280},
                "Lunch": {"meal": "Rajma chawal with salad", "calories": 400},
                "Dinner": {"meal": "Grilled fish with vegetables", "calories": 300}
            },
            "Day 2": {
                "Breakfast": {"meal": "Methi paratha with curd", "calories": 350},
                "Lunch": {"meal": "Chana masala with rice", "calories": 400},
                "Dinner": {"meal": "Tofu stir-fry with quinoa", "calories": 350}
            },
            "Day 3": {
                "Breakfast": {"meal": "Pesarattu with chutney", "calories": 300},
                "Lunch": {"meal": "Grilled chicken with salad", "calories": 350},
                "Dinner": {"meal": "Vegetable curry with roti", "calories": 350}
            },
            "Day 4": {
                "Breakfast": {"meal": "Poha with vegetables", "calories": 250},
                "Lunch": {"meal": "Dal tadka with rice", "calories": 350},
                "Dinner": {"meal": "Vegetable biryani with raita", "calories": 400}
            },
            "Day 5": {
                "Breakfast": {"meal": "Rava upma with chutney", "calories": 280},
                "Lunch": {"meal": "Vegetable pulao with salad", "calories": 350},
                "Dinner": {"meal": "Dal khichdi with curd", "calories": 300}
            },
            "Day 6": {
                "Breakfast": {"meal": "Moong dal chilla with chutney", "calories": 250},
                "Lunch": {"meal": "Aloo paratha with curd", "calories": 400},
                "Dinner": {"meal": "Lentil soup with bread", "calories": 250}
            },
            "Day 7": {
                "Breakfast": {"meal": "Dosa with sambar", "calories": 300},
                "Lunch": {"meal": "Vegetable curry with chapati", "calories": 350},
                "Dinner": {"meal": "Fruit salad with yogurt", "calories": 150}
            }
        },
        "Muscle Gain": {
            "Day 1": {
                "Breakfast": {"meal": "Eggs with avocado and toast", "calories": 500},
                "Lunch": {"meal": "Chicken breast with quinoa and broccoli", "calories": 600},
                "Dinner": {"meal": "Salmon with sweet potato", "calories": 700}
            },
            "Day 2": {
                "Breakfast": {"meal": "Oats with protein powder and almond butter", "calories": 550},
                "Lunch": {"meal": "Grilled steak with vegetables", "calories": 650},
                "Dinner": {"meal": "Chicken stir-fry with rice", "calories": 600}
            },
            "Day 3": {
                "Breakfast": {"meal": "Greek yogurt with granola", "calories": 400},
                "Lunch": {"meal": "Turkey sandwich with whole grain bread", "calories": 500},
                "Dinner": {"meal": "Pasta with chicken and pesto", "calories": 700}
            },
            "Day 4": {
                "Breakfast": {"meal": "Smoothie with protein powder", "calories": 450},
                "Lunch": {"meal": "Grilled chicken with sweet potato", "calories": 550},
                "Dinner": {"meal": "Salmon with quinoa and greens", "calories": 650}
            },
            "Day 5": {
                "Breakfast": {"meal": "Scrambled eggs with spinach and cheese", "calories": 400},
                "Lunch": {"meal": "Beef stir-fry with rice", "calories": 600},
                "Dinner": {"meal": "Chicken with roasted vegetables", "calories": 500}
            },
            "Day 6": {
                "Breakfast": {"meal": "Protein pancakes with syrup", "calories": 500},
                "Lunch": {"meal": "Salmon with roasted potatoes", "calories": 600},
                "Dinner": {"meal": "Grilled chicken with asparagus", "calories": 550}
            },
            "Day 7": {
                "Breakfast": {"meal": "Egg white omelet with veggies", "calories": 350},
                "Lunch": {"meal": "Turkey burger with sweet potato fries", "calories": 700},
                "Dinner": {"meal": "Steak with mashed potatoes", "calories": 750}
            }
        }
    }

    # Show the diet plan based on the goal
    st.markdown(f"### 7-Day {diet_goal} Meal Plan (Breakfast, Lunch, and Dinner):")
    for day, meals in daily_menus[diet_goal].items():
        st.markdown(f"**{day}:**")
        for meal_type, meal_info in meals.items():
            st.markdown(f"  - **{meal_type}:** {meal_info['meal']} (Calories: {meal_info['calories']})")
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

    # Button to generate diet plan
    if st.button("Generate 7-Day Diet Plan", key='generate_button'):
        generate_seven_day_diet(health_goals)

    st.write("---")
    st.markdown("<p style='color: #3F51B5;'><b>Project by TechSpark Group</b></p>", unsafe_allow_html=True)
    st.markdown("- Dipak Walunj\n- Divyank Wani\n- Omkar Zinjurde", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Amrutvahini College of Engineering, Sangamner</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3F51B5;'>Contact: techspark.support@gmail.com</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_page()
    else:
        main_app()
