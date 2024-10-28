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
    
    # Enhanced header with more detailed explanation
    st.header("Objetivo do Framework")
    st.markdown('''
        O SeletorDLTSaude é uma aplicação interativa desenvolvida para ajudar profissionais 
        e pesquisadores a escolherem a melhor solução de Distributed Ledger Technology (DLT) 
        e o algoritmo de consenso mais adequado para projetos de saúde.

        ### Como Funciona
        A aplicação guia você através de um processo estruturado em quatro fases:
        1. **Fase de Aplicação**: 
           - Avalia requisitos de privacidade
           - Analisa necessidades de integração
           - Define controles de acesso
        
        2. **Fase de Consenso**: 
           - Determina requisitos de segurança
           - Avalia eficiência do consenso
           - Define tolerância a falhas
        
        3. **Fase de Infraestrutura**: 
           - Considera escalabilidade
           - Analisa performance
           - Avalia requisitos técnicos
        
        4. **Fase de Internet**: 
           - Define governança
           - Estabelece interoperabilidade
           - Determina acessibilidade
    ''')

    # Enhanced reference table with visual separation
    st.subheader("Tabela de Referência de DLTs e Algoritmos")
    st.markdown("""
        <style>
        .highlight {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
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

    # Create enhanced table with styling
    df = pd.DataFrame(data)
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced start button with clear explanation
    st.markdown("### Iniciar Processo de Seleção")
    st.info("🔍 Ao clicar no botão abaixo, você iniciará o processo guiado de seleção de DLT.")
    
    if st.button("Iniciar Seleção de DLT", type="primary"):
        st.session_state.page = 'Framework Proposto'
        st.session_state.answers = {}  # Reset answers
        st.session_state.current_phase = 1  # Reset phase
        st.session_state.recommendation = None  # Reset recommendation
        st.experimental_rerun()

def show_metrics():
    """Display enhanced metrics and recommendation results"""
    st.header("Métricas - Resultados da Recomendação")
    
    if 'recommendation' not in st.session_state or st.session_state.recommendation is None:
        st.warning("Por favor, complete o questionário primeiro para visualizar as métricas.")
        if st.button("Ir para o Questionário"):
            st.session_state.page = 'Framework Proposto'
            st.experimental_rerun()
        return

    recommendation = st.session_state.recommendation
    
    # Enhanced metrics display with explanations
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Métricas de Avaliação")
        metrics_df = pd.DataFrame({
            'Métrica': ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
            'Valor': [
                recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['security'],
                recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['scalability'],
                recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['energy_efficiency'],
                recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['governance']
            ],
            'Explicação': [
                'Nível de proteção e controle de acesso',
                'Capacidade de crescimento e adaptação',
                'Consumo e otimização de recursos',
                'Flexibilidade e controle administrativo'
            ]
        })
        st.table(metrics_df)
        
        # Add academic validation score
        if 'academic_validation' in recommendation:
            st.subheader("🎓 Validação Acadêmica")
            academic_data = recommendation['academic_validation']
            st.markdown(f"""
                - **Score Acadêmico**: {academic_data.get('score', 'N/A')}/5.0
                - **Citações**: {academic_data.get('citations', 'N/A')}
                - **Referência**: {academic_data.get('reference', 'N/A')}
                - **Validação**: {academic_data.get('validation', 'N/A')}
            """)
    
    with col2:
        st.subheader("🎯 Índices de Confiabilidade")
        confidence_value = recommendation.get('confidence_value', 0.0)
        st.metric(
            label="Confiança da Recomendação",
            value=f"{confidence_value:.2%}",
            delta=f"{'Alta' if confidence_value > 0.7 else 'Média'} Confiabilidade",
            help="Baseado na análise das respostas e métricas acadêmicas"
        )
        
        # Add explanation of metrics
        st.markdown("""
            ### 📝 Interpretação das Métricas
            
            - **0-40%**: Confiança Baixa
            - **41-70%**: Confiança Média
            - **71-100%**: Confiança Alta
            
            A confiabilidade é calculada considerando:
            1. Consistência das respostas
            2. Validação acadêmica
            3. Casos de uso similares
        """)

def show_profile():
    """Display enhanced user profile and saved recommendations"""
    st.header(f"👤 Perfil do Usuário: {st.session_state.username}")
    st.subheader("📋 Recomendações Anteriores")
    
    recommendations = get_user_recommendations(st.session_state.username)
    if recommendations:
        for rec in recommendations:
            with st.expander(f"Recomendação de {rec['timestamp']}", expanded=False):
                st.markdown(f"""
                    ### 🔍 Detalhes da Recomendação
                    - **DLT Recomendada**: {rec['dlt']}
                    - **Algoritmo de Consenso**: {rec['consensus']}
                    - **Data**: {rec['timestamp']}
                    
                    #### 📊 Métricas Principais
                    - Segurança
                    - Escalabilidade
                    - Eficiência
                """)
                st.write("---")
    else:
        st.info("📭 Nenhuma recomendação salva.")

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
        # Enhanced navigation menu
        menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Perfil', 'Logout']
        menu_option = st.sidebar.selectbox("Escolha uma opção", menu_options)

        if menu_option == 'Logout':
            logout()
            st.experimental_rerun()
        else:
            st.session_state.page = menu_option

        # Display current page content with loading indicators
        if st.session_state.page == 'Início':
            show_home_page()
        elif st.session_state.page == 'Framework Proposto':
            from decision_tree import run_decision_tree
            with st.spinner('Carregando questionário...'):
                run_decision_tree()
        elif st.session_state.page == 'Métricas':
            show_metrics()
        elif st.session_state.page == 'Perfil':
            show_profile()

if __name__ == "__main__":
    main()
