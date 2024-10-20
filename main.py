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
        st.session_state.step = 0
        st.session_state.answers = {}
        st.experimental_rerun()

def show_questionnaire():
    st.header("Questionário de Seleção de DLT")
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    scenario = "Registros Médicos Eletrônicos (EMR)"
    if st.session_state.step < len(questions[scenario]):
        current_question = questions[scenario][st.session_state.step]
        st.subheader(current_question['text'])
        st.write(f"Camada: {current_question['shermin_layer']}")
        st.write(f"Característica principal: {current_question['main_characteristic']}")
        answer = st.radio("Escolha uma opção:", current_question['options'])

        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question['id']] = answer
            st.session_state.step += 1
            if st.session_state.step >= len(questions[scenario]):
                st.session_state.page = "weights"
            st.experimental_rerun()
    else:
        st.session_state.page = "weights"
        st.experimental_rerun()

def show_weights():
    st.header("Definir Pesos das Características")
    st.write("Atribua um peso de 1 a 5 para cada característica, onde 1 é menos importante e 5 é mais importante.")
    
    weights = {}
    weights["segurança"] = st.slider("Segurança", 1, 5, 3)
    weights["escalabilidade"] = st.slider("Escalabilidade", 1, 5, 3)
    weights["eficiência energética"] = st.slider("Eficiência Energética", 1, 5, 3)
    weights["governança"] = st.slider("Governança", 1, 5, 3)
    weights["descentralização"] = st.slider("Descentralização", 1, 5, 3)

    if st.button("Gerar Recomendação"):
        st.session_state.weights = weights
        st.session_state.page = "recommendation"
        st.experimental_rerun()

def show_recommendation():
    st.header("Recomendação de DLT e Algoritmo de Consenso")
    
    if 'recommendation' not in st.session_state:
        recommendation = get_recommendation(st.session_state.answers, st.session_state.weights)
        st.session_state.recommendation = recommendation
    else:
        recommendation = st.session_state.recommendation

    st.subheader("DLT Recomendada:")
    st.write(recommendation["dlt"])
    st.subheader("Grupo de Algoritmo de Consenso Recomendado:")
    st.write(recommendation["consensus_group"])

    st.subheader("Comparação de Algoritmos de Consenso:")
    comparison_data = compare_algorithms(recommendation["consensus_group"])
    df = pd.DataFrame(comparison_data)
    st.table(df)

    st.subheader("Selecione as Prioridades para o Algoritmo Final:")
    priorities = {}
    priorities["Segurança"] = st.slider("Segurança", 1, 5, 3)
    priorities["Escalabilidade"] = st.slider("Escalabilidade", 1, 5, 3)
    priorities["Eficiência Energética"] = st.slider("Eficiência Energética", 1, 5, 3)
    priorities["Governança"] = st.slider("Governança", 1, 5, 3)

    if st.button("Selecionar Algoritmo Final"):
        final_algorithm = select_final_algorithm(recommendation["consensus_group"], priorities)
        st.subheader("Algoritmo de Consenso Final Recomendado:")
        st.write(final_algorithm)

        pros_cons = get_scenario_pros_cons(recommendation["dlt"], final_algorithm)
        if pros_cons:
            st.subheader("Cenários Aplicáveis:")
            for scenario, details in pros_cons.items():
                st.write(f"**{scenario}**")
                st.write("Pros:")
                for pro in details["pros"]:
                    st.write(f"- {pro}")
                st.write("Cons:")
                for con in details["cons"]:
                    st.write(f"- {con}")
                st.write(f"Aplicabilidade do Algoritmo: {details['algorithm_applicability']}")

def show_decision_tree():
    st.header("Árvore de Decisão")
    # Implementação futura da árvore de decisão

def show_framework_comparison():
    st.header("Comparação de Frameworks")
    # Implementação futura da comparação de frameworks

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
        elif menu_option == "Questionário" or st.session_state.get('page') == "questionnaire":
            show_questionnaire()
        elif menu_option == "Recomendações" or st.session_state.page == "weights":
            show_weights()
        elif st.session_state.page == "recommendation":
            show_recommendation()
        elif menu_option == "Árvore de Decisão":
            show_decision_tree()
        elif menu_option == "Comparação de Frameworks":
            show_framework_comparison()
        elif menu_option == "Logout":
            logout()

if __name__ == "__main__":
    main()
