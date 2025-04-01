import streamlit as st
from utils import load_user_data, save_user_data

def user_data_page():
    username = st.session_state['username']
    user_data = load_user_data()

    st.subheader("Your Details")
    st.write(f"Name: {user_data[username]['name']}")
    st.write(f"Email: {user_data[username]['email']}")
    st.write(f"Phone: {user_data[username]['phone']}")
    
    # Show user's last diet if available
    last_diet = user_data[username].get('last_diet', None)
    if last_diet:
        st.write("Last Diet Plan: ")
        st.write(last_diet)
    else:
        st.write("No diet plan available.")

    # Show stats if available
    stats = user_data[username].get('stats', None)
    if stats:
        st.write("Your Stats: ")
        st.write(stats)
    else:
        st.write("No stats available.")
