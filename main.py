import streamlit as st
import pandas as pd
import traceback
from datetime import datetime
from user_management import login, register, is_authenticated, logout
from decision_logic import get_recommendation
from database import get_user_recommendations, save_recommendation
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

# Funções de inicialização e gerenciamento de estado
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
    except Exception as e:
        st.error(f"Error initializing session state: {str(e)}")
        st.session_state.error = str(e)

def reset_session_state():
    """Reset session state on errors"""
    try:
        st.session_state.answers = {}
        st.session_state.error = None
        st.session_state.loading = False
        st.session_state.recommendation = None
    except Exception as e:
        st.error(f"Error resetting session state: {str(e)}")


        # Função de fallback para exibir mensagem de erro
        def show_fallback_ui():
            st.error("Ocorreu um erro ao carregar o conteúdo.")
            if st.button("Tentar Novamente"):
                st.session_state.page = "Início"
                
# Funções para exibir cada página
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

    # Criação da tabela
    df = pd.DataFrame(data)
    st.table(df)

    # Botão para iniciar o questionário
    if st.button("Iniciar Questionário"):
        st.session_state.page = 'Framework Proposto'


def show_framework_proposed():
    """Display the decision tree framework for user selection"""
    st.header("Framework Proposto - Questionário de Seleção de DLT")
    st.write("Responda às perguntas abaixo para obter uma recomendação de DLT.")

    answers = {}
    answers['security'] = st.slider("Nível de segurança necessário (0-100)", 0, 100, 50)
    answers['scalability'] = st.slider("Nível de escalabilidade desejado (0-100)", 0, 100, 50)
    answers['energy_efficiency'] = st.slider("Eficiência energética desejada (0-100)", 0, 100, 50)
    answers['governance'] = st.slider("Nível de governança necessária (0-100)", 0, 100, 50)

    # Verifica o botão para obter a recomendação
    if st.button("Obter Recomendação"):
        try:
            # Armazena as respostas no estado da sessão
            st.session_state.answers = answers
            st.session_state.recommendation = get_recommendation(answers)

            # Salva a recomendação no banco de dados com data e usuário
            if st.session_state.recommendation:
                save_recommendation(st.session_state.username, st.session_state.recommendation, datetime.now())
                st.success("Recomendação calculada e salva com sucesso!")
                # Muda a página para 'Métricas'
                st.session_state.page = 'Métricas'
        except Exception as e:
            st.error(f"Erro ao obter recomendação: {str(e)}")


def show_metrics():
    st.header("Métricas - Resultados da Recomendação")
    st.write("Esta página exibe as métricas calculadas com base na recomendação.")

def show_profile():
    """Display the user's profile with saved recommendations"""
    st.header(f"Perfil do Usuário: {st.session_state.username}")
    st.subheader("Recomendações Anteriores")
    recommendations = get_user_recommendations(st.session_state.username)
    if recommendations:
        for rec in recommendations:
            st.write(f"DLT: {rec['dlt']}, Consenso: {rec['consensus']}, Data: {rec['timestamp']}")
            st.markdown("---")
    else:
        st.info("Nenhuma recomendação salva.")

def show_discussion_conclusion():
    st.header("Discussão e Conclusão")
    st.write("Discussão sobre os resultados e conclusões baseadas nas recomendações e métricas.")

# Função principal para controle de navegação e exibição de conteúdo

def main():
    init_session_state()

    if not st.session_state.authenticated:
        st.title("SeletorDLTSaude - Login")
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            if login():
                st.session_state.authenticated = True
                st.session_state.page = 'Início'
        with tab2:
            register()
    else:
        menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Perfil', 'Logout']
        menu_option = st.sidebar.selectbox("Escolha uma opção", menu_options)

        if menu_option == 'Logout':
            st.session_state.authenticated = False
            st.session_state.page = 'Login'
        else:
            st.session_state.page = menu_option

        # Exibir a página com base no valor de `st.session_state.page`
        if st.session_state.page == 'Início':
            show_home_page()
        elif st.session_state.page == 'Framework Proposto':
            show_framework_proposed()
        elif st.session_state.page == 'Métricas':
            show_metrics()
        elif st.session_state.page == 'Perfil':
            show_profile()

if __name__ == "__main__":
    main()