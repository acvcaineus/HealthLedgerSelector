import streamlit as st
from user_management import login, register, is_authenticated, logout
from utils import init_session_state
from decision_tree import run_decision_tree
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm
import pandas as pd

def show_home_page():
    st.title("SeletorDLTSaude")
    st.write("Bem-vindo ao SeletorDLTSaude, um sistema de recomendação de tecnologias de ledger distribuído (DLT) para aplicações em saúde.")
    
    if st.button("Iniciar Questionário"):
        st.session_state.page = "Árvore de Decisão"
        st.rerun()

def main():
    init_session_state()
    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")

    if not is_authenticated():
        st.title("SeletorDLTSaude - Login")
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.title("Menu")

        menu_options = ['Início', 'Árvore de Decisão', 'Logout']
        menu_option = st.sidebar.selectbox(
            "Escolha uma opção",
            menu_options,
            index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
        )

        st.session_state.page = menu_option

        if menu_option == 'Início':
            show_home_page()
        elif menu_option == 'Árvore de Decisão':
            run_decision_tree()
        elif menu_option == 'Logout':
            logout()

if __name__ == "__main__":
    main()
