import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import get_recommendation, compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)
import traceback

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
        'DLT': [
            'Hyperledger Fabric',
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
            'DLT Permissionada Privada',
            'DLT Permissionada Privada',
            'DLT Permissionada Simples',
            'DLT Híbrida',
            'DLT Pública',
            'DLT Pública Permissionless',
            'DLT Pública Permissionless',
            'DLT Pública',
            'DLT Pública',
            'DLT Pública'
        ],
        'Grupo de Algoritmo': [
            'Alta Segurança e Controle dos dados',
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
            'PBFT',
            'Proof of Authority (PoA)',
            'RAFT/IBFT',
            'Tangle',
            'Ripple Consensus Algorithm',
            'Stellar Consensus Protocol (SCP)',
            'Proof of Work (PoW)',
            'Proof of Work (PoW)',
            'Proof of Stake (PoS)'
        ],
        'Caso de Uso': [
            'Rastreabilidade de medicamentos na cadeia de suprimentos',
            'Compartilhamento de Dados de Pesquisa e Registros de Saúde',
            'Rastreamento de suprimentos médicos e cadeia farmacêutica',
            'Monitoramento e rastreamento de medicamentos',
            'Compartilhamento seguro de dados de pacientes via IoT',
            'Processamento eficiente de transações e segurança de dados',
            'Gerenciamento de transações de pagamentos entre provedores',
            'Armazenamento seguro de dados médicos críticos',
            'Contratos inteligentes e registros médicos eletrônicos',
            'Aceleração de ensaios clínicos e compartilhamento de dados'
        ],
        'Referência Bibliográfica': [
            'NASIR, S.; ALPHABLOCK. Medledger system for monitoring counterfeit drugs. 2019.',
            'NASIR, S.; ALPHABLOCK. Permissioned health data networks for secure data sharing. 2020.',
            "TURK, Z.; KLINC, R. FarmaTrust's VeChain for drug authenticity verification. 2019.",
            'GIL, A. C. Mediledger transparency system for drug monitoring. 2002.',
            'VIEIRA, S. C. V. C. A.; GIOZZA, W. F.; RODRIGUES, C. K. S. Patientory platform for real-time data sharing in IoT. 2023.',
            "HEISKANEN, H. Ripple's fast and secure transactions in healthcare. 2020.",
            'LI, J.; HEISKANEN, H. Stellar protocol for secure healthcare payments. 2019.',
            'GIL, A. C. Immutable data storage in public health networks. 2002.',
            'GIOZZA, W. F.; ALMEIDA, S. C. V. C.; RODRIGUES, C. K. S. Smart contracts for secure health records on Ethereum. 2023.',
            'GIL, A. C. Ethereum-based clinical trial tracking system. 2002.'
        ]
    }

    # Update table display to show all columns
    df = pd.DataFrame(data)
    st.table(df)

    if st.button("Iniciar Seleção de DLT", type="primary"):
        st.session_state.page = 'Framework Proposto'
        st.experimental_rerun()

def show_fallback_ui():
    """Display fallback UI when main content fails to load"""
    st.error("Ocorreu um erro ao carregar o conteúdo")
    if st.button("Tentar Novamente"):
        st.experimental_rerun()

def show_metrics_explanation():
    """Display enhanced metrics explanations"""
    st.header("Métricas do Sistema")
    
    with st.expander("Explicação das Métricas de Avaliação"):
        st.markdown("""
        ### 1. Índice de Confiança
        Mede a confiabilidade da recomendação baseado em:
        - Diferença entre o score mais alto e a média dos scores
        - Consistência das respostas fornecidas
        - Validação acadêmica das soluções

        ### 2. Matriz de Avaliação
        Apresenta uma visualização detalhada de como cada DLT se comporta em relação a:
        - Segurança (40%)
        - Escalabilidade (25%)
        - Eficiência Energética (20%)
        - Governança (15%)

        ### 3. Compatibilidade DLT-Algoritmo
        Análise da compatibilidade entre DLTs e algoritmos de consenso considerando:
        - Características técnicas
        - Requisitos de implementação
        - Casos de uso validados
        """)

def main():
    """Main application with improved error handling and state management"""
    try:
        st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
        init_session_state()

        if st.session_state.error:
            show_fallback_ui()
            return

        if not is_authenticated():
            st.title("SeletorDLTSaude - Login")
            tab1, tab2 = st.tabs(["Login", "Registrar"])
            with tab1:
                login()
            with tab2:
                register()
        else:
            with st.sidebar:
                st.title("Menu")
                menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Perfil', 'Logout']
                
                try:
                    menu_option = st.selectbox(
                        "Escolha uma opção",
                        menu_options,
                        index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
                    )
                    st.session_state.page = menu_option
                except Exception as e:
                    st.error(f"Error in navigation: {str(e)}")
                    menu_option = 'Início'

            try:
                if menu_option == 'Início':
                    show_home_page()
                elif menu_option == 'Framework Proposto':
                    run_decision_tree()
                elif menu_option == 'Métricas':
                    show_metrics_explanation()
                elif menu_option == 'Perfil':
                    st.header(f"Perfil do Usuário: {st.session_state.username}")
                    recommendations = get_user_recommendations(st.session_state.username)
                    if recommendations:
                        st.subheader("Últimas Recomendações")
                        for rec in recommendations:
                            st.write(f"DLT: {rec['dlt']}")
                            st.write(f"Consenso: {rec['consensus']}")
                            st.write(f"Data: {rec['timestamp']}")
                            st.markdown("---")
                elif menu_option == 'Logout':
                    logout()
                    st.session_state.page = 'Início'
                    st.experimental_rerun()

            except Exception as e:
                st.error(f"Error loading content: {str(e)}")
                show_fallback_ui()

    except Exception as e:
        st.error(f"Critical error: {str(e)}")
        st.code(traceback.format_exc())
        reset_session_state()

if __name__ == "__main__":
    main()
