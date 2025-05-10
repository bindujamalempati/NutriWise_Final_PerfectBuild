import streamlit as st
import requests

def login_section(base_url):
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        try:
            res = requests.post(f"{base_url}/login", json={"username": username, "password": password})
            if res.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.token = res.json().get('token')
                st.success("Login successful!")
                st.session_state.page = "Meal Planner"
            else:
                st.error("Invalid credentials.")
        except Exception as e:
            st.error(f"Login failed: {e}")