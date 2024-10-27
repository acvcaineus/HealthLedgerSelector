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
            st.session_state.update({
                'initialized': True,
                'authenticated': False,
                'username': None,
                'page': 'Início',
                'answers': {},
                'error': None,
                'loading': False,
                'recommendation': None
            })
    except Exception as e:
        st.error(f"Error initializing session state: {str(e)}")
        st.session_state.error = str(e)


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
        with st.sidebar:
            st.title("Menu")
            menu_options = [
                'Início', 'Framework Proposto', 'Métricas', 'Comparações Benchs',
                'Perfil', 'Logout'
            ]

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

            if menu_option == 'Início':
                show_home_page()
            elif menu_option == 'Framework Proposto':
                run_decision_tree()
            elif menu_option == 'Métricas':
                show_metrics()
            elif menu_option == 'Comparações Benchs':
                show_bench_comparisons()
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

if __name__ == "__main__":
    main()
def show_home_page():
    """Display home page with framework explanation and reference table"""
    st.title("SeletorDLTSaude")
    st.write("Bem-vindo ao sistema de seleção de DLT para saúde.")

    # Framework explanation section
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

    # Reference table section
    st.subheader("Tabela de Referência de DLTs e Algoritmos")
    data = {
        'Grupo': [
            'Alta Segurança e Controle',
            'Alta Segurança e Descentralização',
            'Alta Segurança e Descentralização',
            'Alta Eficiência Operacional',
            'Alta Eficiência Operacional',
            'Escalabilidade e Governança Flexível',
            'Escalabilidade e Governança Flexível',
            'Alta Escalabilidade em Redes IoT'
        ],
        'Tipo de DLT': [
            'DLT Permissionada Privada',
            'DLT Pública Permissionless',
            'DLT Pública Permissionless',
            'DLT Permissionada Simples',
            'DLT Permissionada Simples',
            'DLT Híbrida',
            'DLT com Consenso Delegado',
            'DLT Pública'
        ],
        'Nome DLT': [
            'Hyperledger Fabric',
            'Bitcoin',
            'Ethereum',
            'Quorum',
            'VeChain',
            'Ethereum 2.0',
            'EOS',
            'IOTA'
        ],
        'Algoritmo de Consenso': [
            'PBFT',
            'PoW',
            'PoS (em transição)',
            'RAFT/PoA',
            'PoA',
            'PoS',
            'DPoS',
            'Tangle'
        ],
        'Características': [
            'Segurança elevada e resiliência contra falhas bizantinas; adequada para ambientes altamente controlados e permissionados.',
            'Oferece segurança máxima e total descentralização, essencial para redes abertas onde a integridade dos dados é crucial.',
            'Com transição para PoS, oferece alta segurança e eficiência energética para aplicações que exigem menos processamento intensivo.',
            'Alta eficiência em redes permissionadas; consenso baseado em autoridade ideal para redes empresariais.',
            'Alta eficiência e controle simplificado para gestão de cadeias de suprimento em redes permissionadas.',
            'Alta escalabilidade e eficiência energética, ideal para redes de saúde regionalizadas.',
            'Governança flexível e performance otimizada com arquitetura semi-descentralizada.',
            'Alta escalabilidade e processamento em tempo real para redes de dispositivos IoT em saúde.'
        ],
        'Casos de Uso': [
            'Prontuários eletrônicos, integração de dados sensíveis entre instituições de saúde',
            'Sistemas de pagamento descentralizados, dados críticos de saúde pública',
            'Dados críticos de saúde pública, governança participativa',
            'Redes locais de hospitais, rastreamento de medicamentos',
            'Rastreamento de medicamentos, gestão de insumos hospitalares',
            'Monitoramento de saúde pública, integração de EHRs',
            'Aplicativos de telemedicina, redes de colaboração em pesquisa',
            'Monitoramento de dispositivos IoT hospitalares, dados em tempo real'
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)

    # Implementation details section
    with st.expander("Ver Detalhes de Implementação e Referências"):
        st.markdown('''
            ### Casos de Implementação Real
            - **MyClinic**: Dados descentralizados em clínicas privadas (Hyperledger Fabric)
            - **MediLedger**: Rastreamento de medicamentos na cadeia farmacêutica (Bitcoin)
            - **Patientory**: Armazenamento seguro de dados de pacientes (Ethereum)
            - **PharmaLedger**: Rede permissionada para suprimentos farmacêuticos (Quorum)
            - **VeChain ToolChain**: Rastreabilidade de produtos médicos
            - **Ethereum-based Health Chain**: Integração de EHRs para hospitais regionais
            - **Telos Blockchain**: Rede colaborativa para dados de saúde em telemedicina
            - **IOTA Healthcare IoT**: Monitoramento IoT de dispositivos médicos

            ### Referências Acadêmicas
            - MEHMOOD et al. (2025) - BLPCA-ledger: A lightweight plenum consensus protocols
            - POPOOLA et al. (2024) - Security and privacy in smart home healthcare schemes
            - AKOH ATADOGA et al. (2024) - Blockchain in healthcare: A comprehensive review
            - DHINGRA et al. (2024) - Blockchain Technology Applications in Healthcare
            - AL-NBHANY et al. (2024) - Blockchain-IoT Healthcare Applications and Trends
        ''')

    # Navigation button with enhanced styling
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #4CAF50;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
            border: none;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Iniciar Seleção de DLT", type="primary"):
        st.session_state.page = 'Framework Proposto'
        st.experimental_rerun()
