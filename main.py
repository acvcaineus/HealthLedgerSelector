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
import numpy as np

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
    
    st.header("Tabela de Referência de DLTs")
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
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)

    if st.button("Iniciar Seleção de DLT", type="primary"):
        st.session_state.page = 'Framework Proposto'
        st.experimental_rerun()

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

def show_metrics_explanation():
    """Display enhanced metrics explanations with interactive visualizations"""
    st.header("Métricas Técnicas do Framework")
    
    answers = st.session_state.get('answers', {})
    if not answers:
        st.warning("Complete o processo de seleção para ver as métricas detalhadas.")
        return
        
    weights = {"security": 0.4, "scalability": 0.25, "energy_efficiency": 0.2, "governance": 0.15}
    recommendation = get_recommendation(answers, weights)
    classes = {k: v['score'] for k, v in recommendation['evaluation_matrix'].items()}
    
    gini_values = calcular_gini(classes)
    depth = calcular_profundidade_decisoria(list(range(len(answers))))
    total_nos = len(answers) * 2 + 1
    nos_podados = total_nos - len(answers) - 1
    pruning_ratio = calcular_pruning(total_nos, nos_podados)
    confidence = recommendation.get('confidence_value', 0.0)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Evaluation Matrix
        if 'evaluation_matrix' in recommendation:
            st.subheader("Matriz de Avaliação")
            matrix_data = []
            y_labels = []
            
            for dlt, data in recommendation['evaluation_matrix'].items():
                y_labels.append(dlt)
                row = []
                for metric, value in data['metrics'].items():
                    if metric != 'academic_validation':
                        try:
                            row.append(float(value))
                        except (ValueError, TypeError):
                            row.append(0.0)
                matrix_data.append(row)
            
            metrics = [m for m in recommendation['evaluation_matrix'][y_labels[0]]['metrics'].keys() 
                      if m != 'academic_validation']
            
            fig = go.Figure(data=go.Heatmap(
                z=matrix_data,
                x=metrics,
                y=y_labels,
                colorscale='RdYlGn',
                hoverongaps=False
            ))
            
            fig.update_layout(
                height=350,
                margin=dict(l=50, r=30, t=80, b=50),
                title="Comparação Detalhada das DLTs"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Metrics Summary
        st.subheader("Resumo das Métricas")
        metrics_summary = {
            "Índice de Gini": f"{gini_values:.2f}",
            "Profundidade": f"{depth:.1f}",
            "Taxa de Poda": f"{pruning_ratio:.1%}",
            "Confiança": f"{confidence:.1%}"
        }
        
        for metric, value in metrics_summary.items():
            st.metric(label=metric, value=value)

def main():
    """Main application with improved error handling and state management"""
    try:
        st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
        init_session_state()

        if st.session_state.error:
            st.error("Ocorreu um erro ao carregar o conteúdo")
            if st.button("Tentar Novamente"):
                st.experimental_rerun()
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
                if st.button("Tentar Novamente"):
                    st.experimental_rerun()

    except Exception as e:
        st.error(f"Critical error: {str(e)}")
        st.code(traceback.format_exc())
        st.session_state.error = str(e)
        if st.button("Reiniciar Aplicação"):
            st.session_state.clear()
            st.experimental_rerun()

if __name__ == "__main__":
    main()
