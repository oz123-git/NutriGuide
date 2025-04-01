import streamlit as st
from utils import load_user_data, save_user_data

def registration_page():
    st.markdown("<h1 style='color: #4CAF50;'>Create an Account</h1>", unsafe_allow_html=True)
    
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
                "password": new_password,
                "age": None,
                "height": None,
                "weight": None,
                "gender": None,
                "dietary_preference": None,
                "health_goals": None,
                "last_diet": None,
                "stats": None
            }
            save_user_data(user_data)
            st.success("Account created successfully! Please login.")
