import streamlit as st
import bcrypt
from database import create_user, get_user

def register():
    st.subheader("Criar uma Conta")
    new_username = st.text_input("Nome de Usuário", key="register_username")
    new_password = st.text_input("Senha", type="password", key="register_password")
    confirm_password = st.text_input("Confirmar Senha", type="password", key="register_confirm_password")

    if st.button("Registrar", key="register_button"):
        if new_password != confirm_password:
            st.error("As senhas não coincidem")
        elif len(new_password) < 6:
            st.error("A senha deve ter pelo menos 6 caracteres")
        else:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            if create_user(new_username, hashed_password):
                st.success("Conta criada com sucesso. Você pode fazer login agora.")
            else:
                st.error("Nome de usuário já existe. Por favor, escolha um nome de usuário diferente.")

def login():
    st.subheader("Login")
    username = st.text_input("Nome de Usuário", key="login_username")
    password = st.text_input("Senha", type="password", key="login_password")

    if st.button("Entrar", key="login_button"):
        user = get_user(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Nome de usuário ou senha inválidos")

def is_authenticated():
    return st.session_state.get('authenticated', False)
