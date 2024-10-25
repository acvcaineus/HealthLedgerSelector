import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao, get_metric_explanation)
from utils import init_session_state

def show_metrics():
    st.header("Métricas Técnicas do Processo de Decisão")
    
    if 'recommendation' not in st.session_state:
        st.warning("Complete o processo de seleção primeiro para ver as métricas detalhadas.")
        return

    try:
        # Technical Metrics Section
        with st.expander("🔍 Métricas de Classificação", expanded=True):
            st.subheader("1. Índice de Gini")
            st.markdown("""
            O Índice de Gini mede a impureza de um conjunto de dados, indicando quão bem as 
            características distinguem entre diferentes DLTs.
            """)
            
            if 'evaluation_matrix' in st.session_state.recommendation:
                classes = {k: float(v['score']) for k, v in st.session_state.recommendation['evaluation_matrix'].items()}
                gini = calcular_gini(classes)
                st.metric(
                    label="Índice de Gini Atual",
                    value=f"{gini:.3f}",
                    help="Quanto menor, melhor a separação entre as classes"
                )
                
                if gini < 0.3:
                    st.success("✅ Excelente separação entre as classes!")
                elif gini < 0.6:
                    st.info("ℹ️ Boa separação entre as classes")
                else:
                    st.warning("⚠️ Separação moderada entre as classes")

        # Entropy Analysis
        with st.expander("🎯 Análise de Entropia", expanded=True):
            st.subheader("2. Entropia")
            st.markdown("""
            A Entropia mede a aleatoriedade ou incerteza nas decisões. Uma menor entropia 
            indica decisões mais consistentes e confiáveis.
            """)
            
            entropy = calcular_entropia(classes)
            st.metric(
                label="Entropia do Sistema",
                value=f"{entropy:.3f} bits",
                help="Quanto menor, mais certeza na decisão"
            )

        # Evaluation Matrix
        with st.expander("📊 Matriz de Avaliação Detalhada", expanded=True):
            st.subheader("3. Matriz de Avaliação")
            if 'evaluation_matrix' in st.session_state.recommendation:
                matrix_data = []
                y_labels = []
                
                for dlt, data in st.session_state.recommendation['evaluation_matrix'].items():
                    y_labels.append(dlt)
                    row = []
                    for metric, value in data['metrics'].items():
                        if metric != "academic_validation":
                            try:
                                row.append(float(value))
                            except (ValueError, TypeError):
                                row.append(0.0)
                    matrix_data.append(row)
                
                metrics = [m for m in st.session_state.recommendation['evaluation_matrix'][y_labels[0]]['metrics'].keys() 
                          if m != "academic_validation"]
                
                fig = go.Figure(data=go.Heatmap(
                    z=matrix_data,
                    x=metrics,
                    y=y_labels,
                    colorscale=[
                        [0, "#ff0000"],    # Red for low values
                        [0.4, "#ffff00"],  # Yellow for medium values
                        [0.7, "#00ff00"]   # Green for high values
                    ],
                    hoverongaps=False
                ))
                
                fig.update_layout(
                    title="Matriz de Avaliação Comparativa",
                    xaxis_title="Métricas",
                    yaxis_title="DLTs",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao calcular métricas: {str(e)}")
        st.warning("Por favor, reinicie o processo de seleção.")

def show_reference_table():
    dlt_data = pd.DataFrame({
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
            'Alta Segurança e Controle',
            'Alta Segurança e Controle',
            'Escalabilidade e Governança Flexível',
            'Alta Eficiência Operacional',
            'Alta Escalabilidade em Redes IoT',
            'Alta Eficiência Operacional',
            'Alta Eficiência Operacional',
            'Alta Segurança e Descentralização',
            'Alta Segurança e Descentralização',
            'Escalabilidade e Governança Flexível'
        ],
        'Algoritmo de Consenso': [
            'PBFT',
            'RAFT',
            'RAFT/IBFT',
            'PoA',
            'Tangle',
            'Ripple Consensus Protocol',
            'Stellar Consensus Protocol',
            'PoW',
            'PoW',
            'PoS'
        ]
    })
    st.table(dlt_data)

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")

    st.markdown("## Referência de DLTs e Algoritmos")
    st.write("Abaixo está uma tabela detalhada com as principais DLTs e suas características para aplicações em saúde:")
    show_reference_table()

    st.markdown("---")
    st.subheader("Iniciar o Processo de Seleção de DLT")
    if st.button("Iniciar Questionário", help="Clique aqui para começar o processo de seleção de DLT"):
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
