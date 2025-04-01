import streamlit as st
from utils import load_user_data

def login_page():
    st.markdown("<h1 style='color: #2196F3;'>AI Nutrition - Login</h1>", unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.success(f"Welcome back, {user_data[username]['name']}!")
        else:
            st.error("Invalid credentials. Please try again.")
