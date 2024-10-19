import streamlit as st

def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'scenario' not in st.session_state:
        st.session_state.scenario = None
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'weights' not in st.session_state:
        st.session_state.weights = {}

def main():
    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥")
    init_session_state()

    if not st.session_state.authenticated:
        st.write("Por favor, faça login.")
    else:
        st.write(f"Bem-vindo, {st.session_state.username}")
