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
    except Exception as e:
        st.error(f"Error initializing session state: {str(e)}")
        st.session_state.error = str(e)

def show_home_page():
    """Display home page with framework explanation and reference table"""
    st.title("SeletorDLTSaude")
    st.write("Bem-vindo ao sistema de seleção de DLT para saúde.")
    st.header("Objetivo do Framework")
    st.markdown('''
        O SeletorDLTSaude é uma aplicação interativa desenvolvida para ajudar profissionais 
        e pesquisadores a escolherem a melhor solução de Distributed Ledger Technology (DLT) 
        e o algoritmo de consenso mais adequado para projetos de saúde.

        A aplicação guia o usuário através de um processo estruturado em quatro fases:
        - **Fase de Aplicação**: Avalia requisitos de privacidade e integração
        - **Fase de Consenso**: Analisa necessidades de segurança e eficiência
        - **Fase de Infraestrutura**: Considera escalabilidade e performance
        - **Fase de Internet**: Avalia governança e interoperabilidade
    ''')

    st.subheader("Tabela de Referência de DLTs e Algoritmos")
    data = {
        'Grupo': [
            'Alta Segurança e Controle', 'Alta Segurança e Controle',
            'Alta Eficiência Operacional', 'Alta Eficiência Operacional',
            'Escalabilidade e Governança Flexível', 'Alta Escalabilidade em Redes IoT'
        ],
        'Tipo DLT': [
            'DLT Permissionada Privada', 'DLT Pública Permissionless',
            'DLT Permissionada Simples', 'DLT Híbrida',
            'DLT com Consenso Delegado', 'DLT Pública'
        ],
        'Nome DLT': [
            'Hyperledger Fabric', 'Bitcoin', 'Quorum', 'Ethereum 2.0', 'EOS', 'IOTA'
        ],
        'Algoritmo de Consenso': [
            'PBFT', 'PoW', 'RAFT/PoA', 'PoS', 'DPoS', 'Tangle'
        ],
        'Principais Características': [
            'Alta segurança e resiliência contra falhas bizantinas', 
            'Alta segurança e descentralização total',
            'Simplicidade e eficiência em redes locais',
            'Alta escalabilidade e eficiência energética',
            'Governança flexível e alta performance',
            'Escalabilidade para IoT e dados em tempo real'
        ]
    }

    # Create table
    df = pd.DataFrame(data)
    st.table(df)

    # Button to start questionnaire with proper navigation
    if st.button("Iniciar Seleção de DLT", type="primary"):
        st.session_state.page = 'Framework Proposto'
        st.experimental_rerun()

def show_metrics():
    """Display metrics and recommendation results"""
    st.header("Métricas - Resultados da Recomendação")
    
    if 'recommendation' not in st.session_state or st.session_state.recommendation is None:
        st.warning("Por favor, complete o questionário primeiro para visualizar as métricas.")
        if st.button("Ir para o Questionário"):
            st.session_state.page = 'Framework Proposto'
            st.experimental_rerun()
        return

    # Display recommendation metrics
    recommendation = st.session_state.recommendation
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Métricas de Avaliação")
        metrics_df = pd.DataFrame({
            'Métrica': ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
            'Valor': [
                recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['security'],
                recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['scalability'],
                recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['energy_efficiency'],
                recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['governance']
            ]
        })
        st.table(metrics_df)
    
    with col2:
        st.subheader("Confiabilidade da Recomendação")
        confidence_value = recommendation.get('confidence_value', 0.0)
        st.metric(
            label="Índice de Confiança",
            value=f"{confidence_value:.2%}",
            delta=f"{'Alta' if confidence_value > 0.7 else 'Média'} Confiabilidade"
        )

def show_profile():
    """Display user profile and saved recommendations"""
    st.header(f"Perfil do Usuário: {st.session_state.username}")
    st.subheader("Recomendações Anteriores")
    
    recommendations = get_user_recommendations(st.session_state.username)
    if recommendations:
        for rec in recommendations:
            with st.expander(f"Recomendação de {rec['timestamp']}", expanded=False):
                st.write(f"**DLT Recomendada:** {rec['dlt']}")
                st.write(f"**Algoritmo de Consenso:** {rec['consensus']}")
                st.write("---")
    else:
        st.info("Nenhuma recomendação salva.")

def main():
    """Main function with improved navigation and authentication"""
    init_session_state()

    # Handle authentication
    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        # Show navigation menu only when authenticated
        menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Perfil', 'Logout']
        menu_option = st.sidebar.selectbox("Escolha uma opção", menu_options)

        if menu_option == 'Logout':
            logout()
            st.experimental_rerun()
        else:
            st.session_state.page = menu_option

        # Display current page content
        if st.session_state.page == 'Início':
            show_home_page()
        elif st.session_state.page == 'Framework Proposto':
            from decision_tree import run_decision_tree
            run_decision_tree()
        elif st.session_state.page == 'Métricas':
            show_metrics()
        elif st.session_state.page == 'Perfil':
            show_profile()

if __name__ == "__main__":
    main()
