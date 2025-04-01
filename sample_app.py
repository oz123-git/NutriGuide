import streamlit as st
from pages import login, registration, user_data

# Main app logic
def main_app():
    # Check if the user is authenticated
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.warning("Please login to access the app.")
        login.login_page()  # Call the login page from login.py
        return

    # If authenticated, fetch the username from session state
    if 'username' in st.session_state:
        username = st.session_state['username']
        st.success(f"Welcome back, {username}!")
        user_data.user_data_page(username)  # Show user data from user_data.py

    # Option to logout
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.success("You have been logged out.")

if __name__ == '__main__':
    main_app()
