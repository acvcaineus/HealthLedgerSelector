import streamlit as st
import pandas as pd
import traceback
from datetime import datetime
from user_management import login, register, logout
from decision_logic import get_recommendation
from database import get_user_recommendations, save_recommendation
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def init_session_state():
    """Initialize all required session state variables with error handling"""
    try:
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.page = 'Início'
            st.session_state.answers = {}
            st.session_state.error = None
            st.session_state.loading = False
            st.session_state.recommendation = None
            st.session_state.current_phase = 1
            st.session_state.phase_complete = False
            st.session_state.questionnaire_started = False
    except Exception as e:
        st.error(f"Error initializing session state: {str(e)}")
        st.session_state.error = str(e)

def show_home_page():
    """Display home page with framework explanation and start button"""
    st.title("SeletorDLTSaude")
    st.write("Bem-vindo ao sistema de seleção de DLT para saúde.")
    
    # Framework explanation
    st.markdown("""
        ### Como Funciona
        A aplicação guia você através de um processo estruturado em quatro fases:
        1. **Fase de Aplicação**: Avalia requisitos de privacidade e integração
        2. **Fase de Consenso**: Determina requisitos de segurança
        3. **Fase de Infraestrutura**: Considera escalabilidade e performance
        4. **Fase de Internet**: Define governança e interoperabilidade
    """)
    
    # Simple start button
    if st.button("Iniciar Seleção de DLT"):
        st.session_state.page = 'Framework Proposto'
        st.session_state.answers = {}
        st.session_state.current_phase = 1
        st.session_state.recommendation = None
        st.session_state.questionnaire_started = True
        st.experimental_rerun()

def show_metrics():
    """Display metrics and recommendation results"""
    st.title("Métricas e Resultados")
    if not st.session_state.recommendation:
        st.warning("Complete o questionário primeiro para ver as métricas.")
        return
    
    # Display metrics from recommendation
    st.write(st.session_state.recommendation)

def show_profile():
    """Display user profile and recommendations"""
    st.title(f"Perfil - {st.session_state.username}")
    recommendations = get_user_recommendations(st.session_state.username)
    
    if recommendations:
        for rec in recommendations:
            st.write(f"Recomendação: {rec}")
    else:
        st.info("Nenhuma recomendação encontrada.")

def main():
    """Main application function"""
    init_session_state()

    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        menu = ['Início', 'Framework Proposto', 'Métricas', 'Perfil', 'Logout']
        choice = st.sidebar.selectbox("Menu", menu)
        
        if choice == 'Logout':
            logout()
            st.experimental_rerun()
        else:
            st.session_state.page = choice
            
        if st.session_state.page == 'Início':
            show_home_page()
        elif st.session_state.page == 'Framework Proposto':
            from decision_tree import run_decision_tree
            if st.session_state.questionnaire_started:
                run_decision_tree()
            else:
                st.warning("Clique em 'Iniciar Seleção de DLT' na página inicial.")
        elif st.session_state.page == 'Métricas':
            show_metrics()
        elif st.session_state.page == 'Perfil':
            show_profile()

if __name__ == "__main__":
    main()
