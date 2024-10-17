import streamlit as st
import bcrypt
from database import create_user, get_user

def register():
    st.subheader("Create an Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters long")
        else:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            if create_user(new_username, hashed_password):
                st.success("Account created successfully. You can now log in.")
            else:
                st.error("Username already exists. Please choose a different username.")

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def is_authenticated():
    return st.session_state.get('authenticated', False)
