import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from user_management import login, register, is_authenticated, logout
from database import get_user_recommendations, save_recommendation, save_feedback
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm, get_scenario_pros_cons
from dlt_data import scenarios, questions, dlt_classes, consensus_algorithms
from utils import init_session_state

# ... [Keep all existing functions] ...

def show_correlation_table():
    st.subheader("Tabela de Correlação DLT, Grupo de Algoritmo e Algoritmo de Consenso")
    data = {
        'DLT': ['Hyperledger Fabric', 'Corda', 'Quorum', 'VeChain', 'IOTA', 'Ripple (XRP Ledger)', 'Stellar', 'Bitcoin', 'Ethereum (PoW)', 'Ethereum 2.0 (PoS)', 'Cardano', 'Algorand', 'Tezos', 'Polkadot', 'IOTA (Recomendação)'],
        'Tipo de DLT': ['DLT Permissionada Privada', 'DLT Permissionada Simples', 'DLT Híbrida', 'DLT Híbrida', 'DLT com Consenso Delegado', 'DLT com Consenso Delegado', 'DLT com Consenso Delegado', 'DLT Pública', 'DLT Pública', 'DLT Pública Permissionless', 'DLT Pública Permissionless', 'DLT Pública Permissionless', 'DLT Pública Permissionless', 'DLT Pública Permissionless', 'DLT com Consenso Delegado'],
        'Grupo de Algoritmo': ['Alta Segurança e Controle dos dados sensíveis', 'Alta Segurança e Controle dos dados sensíveis', 'Escalabilidade e Governança Flexível', 'Alta Eficiência Operacional em redes locais', 'Alta Escalabilidade em Redes IoT', 'Alta Eficiência Operacional em redes locais', 'Alta Eficiência Operacional em redes locais', 'Alta Segurança e Descentralização de dados críticos', 'Alta Segurança e Descentralização de dados críticos', 'Escalabilidade e Governança Flexível', 'Escalabilidade e Governança Flexível', 'Escalabilidade e Governança Flexível', 'Escalabilidade e Governança Flexível', 'Escalabilidade e Governança Flexível', 'Alta Escalabilidade em Redes IoT'],
        'Algoritmo de Consenso': ['RAFT/IBFT', 'RAFT', 'RAFT/IBFT', 'PoA', 'Tangle', 'Ripple Consensus Algorithm', 'SCP', 'PoW', 'PoW', 'PoS', 'Liquid PoS', 'Pure PoS', 'Liquid PoS', 'NPoS', 'Tangle'],
        'Principais Características do Algoritmo': [
            'Alta tolerância a falhas, consenso rápido em ambientes permissionados',
            'Consenso baseado em líderes, adequado para redes privadas',
            'Flexibilidade de governança, consenso eficiente para redes híbridas',
            'Alta eficiência, baixa latência, consenso delegado a validadores autorizados',
            'Escalabilidade alta, arquitetura sem blocos, adequada para IoT',
            'Consenso rápido, baixa latência, baseado em validadores confiáveis',
            'Consenso baseado em quórum, alta eficiência, tolerância a falhas',
            'Segurança alta, descentralização, consumo elevado de energia',
            'Segurança alta, descentralização, escalabilidade limitada, alto custo',
            'Eficiência energética, incentivo à participação, redução da centralização',
            'Alta escalabilidade, participação líquida, foco em sustentabilidade',
            'Rápido tempo de confirmação, participação aberta, segurança elevada',
            'Consenso dinâmico, alta adaptabilidade, foco em governança',
            'Consenso eficiente, interoperabilidade entre parachains, segurança robusta',
            'Ideal para alta escalabilidade e eficiência em redes IoT, arquitetura leve'
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)

def show_home_page():
    st.header("Bem-vindo ao SeletorDLTSaude")
    st.write("""
    O SeletorDLTSaude é uma ferramenta interativa projetada para ajudar profissionais e pesquisadores 
    da área de saúde a escolher a melhor solução de Tecnologia de Ledger Distribuído (DLT) e o algoritmo 
    de consenso mais adequado para seus projetos.
    """)
    show_correlation_table()
    if st.button("Iniciar Questionário"):
        st.session_state.page = "questionnaire"
        st.rerun()

def show_questionnaire():
    st.header("Questionário de Seleção de DLT")
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    current_question = questions["Registros Médicos Eletrônicos (EMR)"][st.session_state.step]
    st.subheader(current_question['text'])
    answer = st.radio("Escolha uma opção:", current_question['options'])

    if st.button("Próxima Pergunta"):
        st.session_state.answers[current_question['id']] = answer
        st.session_state.step += 1
        if st.session_state.step >= len(questions["Registros Médicos Eletrônicos (EMR)"]):
            st.session_state.page = "recommendation"
            st.rerun()
        else:
            st.rerun()

def show_decision_tree():
    st.header("Árvore de Decisão")
    # We'll implement this later

def show_framework_comparison():
    st.header("Comparação de Frameworks")
    # We'll implement this later

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
        menu_option = st.sidebar.selectbox("Escolha uma opção", ["Início", "Questionário", "Recomendações", "Árvore de Decisão", "Comparação de Frameworks", "Logout"])

        if menu_option == "Início":
            show_home_page()
        elif menu_option == "Questionário":
            st.session_state.page = "questionnaire"
            show_questionnaire()
        elif menu_option == "Recomendações":
            show_recommendation()
        elif menu_option == "Árvore de Decisão":
            show_decision_tree()
        elif menu_option == "Comparação de Frameworks":
            show_framework_comparison()
        elif menu_option == "Logout":
            logout()

if __name__ == "__main__":
    main()
