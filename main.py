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

def show_metrics():
    st.header("Métricas Técnicas do Processo de Decisão")
    
    # Gini Index Section
    st.subheader("1. Índice de Gini")
    st.markdown("""
    O Índice de Gini mede a impureza de um conjunto de dados. Em nossa árvore de decisão, 
    ele indica quão bem as características distinguem entre diferentes DLTs.
    """)
    
    # LaTeX formula for Gini Index
    st.latex(r"Gini = 1 - \sum_{i=1}^{n} p_i^2")
    
    st.markdown("""
    Onde:
    - $p_i$ é a proporção de cada classe no conjunto
    - Valores próximos a 0 indicam melhor separação
    - Valores próximos a 1 indicam maior mistura
    """)
    
    # Example calculation
    if 'recommendation' in st.session_state:
        rec = st.session_state.recommendation
        if 'evaluation_matrix' in rec:
            classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
            gini = calcular_gini(classes)
            
            st.metric(
                label="Índice de Gini Atual",
                value=f"{gini:.3f}",
                help="Quanto menor, melhor a separação entre as classes"
            )
    
    # Entropy Section
    st.subheader("2. Entropia")
    st.markdown("""
    A Entropia mede a aleatoriedade ou incerteza em nosso conjunto de decisões.
    Uma menor entropia indica decisões mais consistentes e confiáveis.
    """)
    
    # LaTeX formula for Entropy
    st.latex(r"Entropia = -\sum_{i=1}^{n} p_i \log_2(p_i)")
    
    st.markdown("""
    Onde:
    - $p_i$ é a probabilidade de cada classe
    - Logaritmo na base 2 é usado para medir em bits
    - Menor entropia indica maior certeza na decisão
    """)
    
    if 'recommendation' in st.session_state:
        rec = st.session_state.recommendation
        if 'evaluation_matrix' in rec:
            classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
            entropy = calcular_entropia(classes)
            
            st.metric(
                label="Entropia Atual",
                value=f"{entropy:.3f} bits",
                help="Quanto menor, mais certeza na decisão"
            )
    
    # Decision Tree Metrics
    st.subheader("3. Métricas da Árvore de Decisão")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'answers' in st.session_state:
            depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
            st.metric(
                label="Profundidade da Árvore",
                value=f"{depth:.1f}",
                help="Número médio de decisões necessárias"
            )
    
    with col2:
        if 'recommendation' in st.session_state:
            total_nos = len(st.session_state.answers) * 2 + 1
            nos_podados = total_nos - len(st.session_state.answers) - 1
            pruning_ratio = calcular_pruning(total_nos, nos_podados)
            st.metric(
                label="Taxa de Poda",
                value=f"{pruning_ratio:.2%}",
                help="Porcentagem de nós removidos para simplificação"
            )

def show_reference_table():
    # Updated table structure with data from the provided file
    dlt_data = {
        'DLT': [
            'Hyperledger Fabric', 'Corda', 'Quorum', 'VeChain', 'IOTA',
            'Ripple (XRP Ledger)', 'Stellar', 'Bitcoin', 'Ethereum (PoW)',
            'Ethereum 2.0 (PoS)'
        ],
        'Tipo de DLT': [
            'DLT Permissionada Privada', 'DLT Permissionada Simples', 'DLT Híbrida',
            'DLT Híbrida', 'DLT com Consenso Delegado', 'DLT com Consenso Delegado',
            'DLT com Consenso Delegado', 'DLT Pública', 'DLT Pública',
            'DLT Pública Permissionless'
        ],
        'Grupo de Algoritmo': [
            'Alta Segurança e Controle dos dados sensíveis',
            'Alta Segurança e Controle dos dados sensíveis',
            'Escalabilidade e Governança Flexível',
            'Alta Eficiência Operacional em redes locais',
            'Alta Escalabilidade em Redes IoT',
            'Alta Eficiência Operacional em redes locais',
            'Alta Eficiência Operacional em redes locais',
            'Alta Segurança e Descentralização de dados críticos',
            'Alta Segurança e Descentralização de dados críticos',
            'Escalabilidade e Governança Flexível'
        ],
        'Algoritmo de Consenso': [
            'RAFT/IBFT', 'RAFT', 'RAFT/IBFT', 'PoA', 'Tangle',
            'Ripple Consensus Algorithm', 'SCP', 'PoW', 'PoW', 'PoS'
        ],
        'Principais Características': [
            'Alta tolerância a falhas, consenso rápido em ambientes permissionados',
            'Consenso baseado em líderes, adequado para redes privadas',
            'Flexibilidade de governança, consenso eficiente para redes híbridas',
            'Alta eficiência, baixa latência, consenso delegado a validadores autorizados',
            'Escalabilidade alta, arquitetura sem blocos, adequada para IoT',
            'Consenso rápido, baixa latência, baseado em validadores confiáveis',
            'Consenso baseado em quórum, alta eficiência, tolerância a falhas',
            'Segurança alta, descentralização, consumo elevado de energia',
            'Segurança alta, descentralização, escalabilidade limitada, alto custo',
            'Eficiência energética, incentivo à participação, redução da centralização'
        ],
        'Estudos de Uso': [
            'Guardtime: Aplicado em sistemas de saúde da Estônia',
            'ProCredEx: Validação de credenciais de profissionais de saúde nos EUA',
            'Chronicled (Mediledger Project): Rastreamento de medicamentos',
            'FarmaTrust: Rastreamento de medicamentos e combate à falsificação',
            'Patientory: Compartilhamento de dados de pacientes via IoT',
            'Change Healthcare: Gestão de ciclo de receita',
            'MedicalChain: Controle de dados e consultas telemédicas',
            'Guardtime: Rastreamento de dados de saúde em redes públicas',
            'Embleema: Desenvolvimento de medicamentos e ensaios clínicos',
            'MTBC: Gestão de registros eletrônicos de saúde (EHR)'
        ]
    }
    
    df = pd.DataFrame(dlt_data)
    st.table(df)

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")

    st.markdown("## Referência de DLTs e Algoritmos")
    st.write("Abaixo está uma tabela detalhada com as principais DLTs e suas características para aplicações em saúde:")
    show_reference_table()

    st.markdown("---")
    st.subheader("Iniciar o Processo de Seleção de DLT")
    if st.button("Iniciar Questionário", key="start_questionnaire", help="Clique aqui para começar o processo de seleção de DLT"):
        st.session_state.page = "Framework Proposto"
        st.experimental_rerun()

def show_user_profile():
    st.header(f"Perfil do Usuário: {st.session_state.username}")
    recommendations = get_user_recommendations(st.session_state.username)
    if recommendations:
        st.subheader("Últimas Recomendações")
        for rec in recommendations:
            st.write(f"DLT: {rec['dlt']}")
            st.write(f"Consenso: {rec['consensus']}")
            st.write(f"Data: {rec['timestamp']}")
            st.markdown("---")

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
