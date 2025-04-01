import streamlit as st
from pages.login import login_page
from pages.registration import registration_page
from pages.user_data import user_data_page

def main():
    st.title("AI-Driven Personalized Nutrition")

    # Check if the user is authenticated (i.e., logged in)
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        # If not logged in, show the login page
        st.warning("Please login to access the app.")
        login_page()  # Calls the login page function
    else:
        # If logged in, show the user data page
        user_data_page()  # Calls the user data page function

if __name__ == '__main__':
    main()
