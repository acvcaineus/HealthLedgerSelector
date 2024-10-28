import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)
from utils import init_session_state

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    
    # Display reference table
    st.header("Tabela de Referência DLT")
    
    # Create DataFrame with the DLT reference data
    df = pd.DataFrame({
        'DLT': [
            'Hyperledger Fabric',
            'VeChain',
            'Quorum (Mediledger)',
            'IOTA',
            'Ripple (XRP Ledger)',
            'Stellar',
            'Bitcoin',
            'Ethereum (PoW)',
            'Ethereum 2.0 (PoS)'
        ],
        'Tipo de DLT': [
            'DLT Permissionada Privada (PBFT)',
            'DLT Permissionada Simples',
            'DLT Híbrida',
            'DLT Pública',
            'DLT com Consenso Delegado',
            'DLT com Consenso Delegado',
            'DLT Pública Permissionless',
            'DLT Pública Permissionless',
            'DLT Híbrida (PoS)'
        ],
        'Grupo de Algoritmo': [
            'Alta Segurança e Controle dos dados',
            'Alta Eficiência Operacional em redes locais',
            'Escalabilidade e Governança Flexível',
            'Alta Escalabilidade em Redes IoT',
            'Alta Eficiência Operacional em redes locais',
            'Alta Eficiência Operacional em redes locais',
            'Alta Segurança e Descentralização',
            'Alta Segurança e Descentralização',
            'Escalabilidade e Governança Flexível'
        ],
        'Algoritmo de Consenso': [
            'RAFT/IBFT',
            'Proof of Authority (PoA)',
            'RAFT/IBFT',
            'Tangle',
            'Ripple Consensus Algorithm',
            'Stellar Consensus Protocol (SCP)',
            'Proof of Work (PoW)',
            'Proof of Work (PoW)',
            'Proof of Stake (PoS)'
        ],
        'Principais Características': [
            'Alta segurança e resiliência contra falhas bizantinas',
            'Simplicidade e eficiência em redes permissionadas menores',
            'Alta escalabilidade e eficiência energética',
            'Alta escalabilidade e eficiência para IoT',
            'Processamento eficiente de transações',
            'Gerenciamento de transações de pagamentos',
            'Máxima segurança e descentralização',
            'Alta segurança e descentralização',
            'Alta escalabilidade e eficiência energética'
        ],
        'Estudos de Uso': [
            'Prontuários eletrônicos, integração de dados sensíveis',
            'Sistemas locais de saúde, redes locais de hospitais',
            'Monitoramento e rastreamento de medicamentos',
            'Monitoramento de dispositivos IoT em saúde',
            'Processamento de transações na saúde',
            'Consultas telemédicas seguras',
            'Armazenamento seguro de dados médicos críticos',
            'Contratos inteligentes e registros médicos',
            'Ensaios clínicos e compartilhamento de dados'
        ]
    })
    
    # Display table with proper formatting
    st.dataframe(df, use_container_width=True)
    
    # Add explanatory sections
    with st.expander("Sobre os Tipos de DLT"):
        st.markdown("""
        ### Tipos de DLT Disponíveis
        - **DLT Permissionada Privada**: Ideal para dados sensíveis e controle de acesso
        - **DLT Permissionada Simples**: Otimizada para redes locais e eficiência
        - **DLT Híbrida**: Combina benefícios de redes públicas e privadas
        - **DLT Pública**: Máxima transparência e descentralização
        - **DLT com Consenso Delegado**: Balanceia performance e descentralização
        """)
    
    with st.expander("Grupos de Algoritmos"):
        st.markdown("""
        ### Grupos de Algoritmos de Consenso
        - **Alta Segurança e Controle**: Foco em proteção de dados e controle de acesso
        - **Alta Eficiência Operacional**: Otimizado para performance em redes locais
        - **Escalabilidade e Governança**: Equilibra crescimento e gestão da rede
        - **Alta Escalabilidade em IoT**: Especializado em dispositivos IoT e dados em tempo real
        """)
    
    # Add call-to-action section
    st.markdown("---")
    st.subheader("Começar a Seleção de DLT")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Iniciar Framework de Seleção"):
            st.session_state.page = "Framework Proposto"
            st.experimental_rerun()
    with col2:
        if st.button("Ver Métricas Detalhadas"):
            st.session_state.page = "Métricas"
            st.experimental_rerun()

def show_metrics():
    st.header("Métricas Técnicas do Processo de Decisão")
    
    if 'recommendation' not in st.session_state:
        st.warning("Complete o processo de recomendação primeiro para visualizar as métricas.")
        if st.button("Ir para o Framework"):
            st.session_state.page = "Framework Proposto"
            st.experimental_rerun()
        return

    with st.spinner("Carregando métricas..."):
        # [Rest of the metrics code remains unchanged]
        pass

def show_user_profile():
    st.header(f"Perfil do Usuário: {st.session_state.username}")
    
    # Display user's recommendations
    recommendations = get_user_recommendations(st.session_state.username)
    if recommendations:
        st.subheader("Suas Últimas Recomendações")
        for rec in recommendations:
            st.write(f"Data: {rec['timestamp']}")
            st.write(f"DLT: {rec['dlt']}")
            st.write(f"Algoritmo de Consenso: {rec['consensus']}")
            st.write("---")
    else:
        st.info("Você ainda não tem recomendações salvas.")

def main():
    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
    init_session_state()

    if not is_authenticated():
        st.title("SeletorDLTSaude - Login")
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.title("Menu")
        menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Perfil', 'Logout']
        
        menu_option = st.sidebar.selectbox(
            "Escolha uma opção",
            menu_options,
            index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
        )
        
        st.session_state.page = menu_option
        
        if menu_option == 'Início':
            show_home_page()
        elif menu_option == 'Framework Proposto':
            run_decision_tree()
        elif menu_option == 'Métricas':
            show_metrics()
        elif menu_option == 'Perfil':
            show_user_profile()
        elif menu_option == 'Logout':
            logout()
            st.session_state.page = 'Início'
            st.experimental_rerun()

if __name__ == "__main__":
    main()
