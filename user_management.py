import streamlit as st
import bcrypt
from database import create_user, get_user

def register():
    st.subheader("Criar uma Conta")
    new_username = st.text_input("Nome de Usuário", key="register_username")
    new_password = st.text_input("Senha", type="password", key="register_password")
    confirm_password = st.text_input("Confirmar Senha", type="password", key="register_confirm_password")

    if st.button("Registrar", key="register_button"):
        if not new_username or not new_password:
            st.error("Por favor, preencha todos os campos")
            return
        
        # Verificação das senhas
        if new_password != confirm_password:
            st.error("As senhas não coincidem")
        elif len(new_password) < 6:
            st.error("A senha deve ter pelo menos 6 caracteres")
        else:
            # Hash da senha usando bcrypt
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            if create_user(new_username, hashed_password):
                st.success("Conta criada com sucesso. Você pode fazer login agora.")
            else:
                st.error("Nome de usuário já existe. Por favor, escolha um nome de usuário diferente.")

def login():
    try:
        st.subheader("Login")
        username = st.text_input("Nome de Usuário", key="login_username")
        password = st.text_input("Senha", type="password", key="login_password")

        if st.button("Entrar", key="login_button"):
            if not username or not password:
                st.error("Por favor, preencha todos os campos")
                return
            
            user = get_user(username)
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                # Initialize session state if not already done
                if 'authenticated' not in st.session_state:
                    st.session_state.authenticated = False
                if 'username' not in st.session_state:
                    st.session_state.username = None
                if 'page' not in st.session_state:
                    st.session_state.page = 'Início'
                
                # Update session state
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login realizado com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Nome de usuário ou senha inválidos")
    except Exception as e:
        st.error(f"Erro durante o login: {str(e)}")
        print(f"Login error: {str(e)}")

def is_authenticated():
    return bool(st.session_state.get('authenticated', False))

def logout():
    try:
        # Clear all session state variables
        st.session_state.clear()
        # Reinitialize essential session state variables
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.page = 'Início'
        st.success("Logout realizado com sucesso!")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Erro durante o logout: {str(e)}")
        print(f"Logout error: {str(e)}")
