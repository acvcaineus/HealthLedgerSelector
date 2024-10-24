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
    
    # Visual Scales
    st.subheader("4. Escalas Visuais de Métricas")
    
    if 'recommendation' in st.session_state:
        rec = st.session_state.recommendation
        if 'evaluation_matrix' in rec:
            metrics = rec['evaluation_matrix'][rec['dlt']]['metrics']
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=[float(metrics[m]) for m in metrics.keys()],
                theta=list(metrics.keys()),
                fill='toself',
                name=rec['dlt'],
                line_color='#2ecc71'
            ))
            
            avg_metrics = {}
            for metric in metrics.keys():
                values = [float(data['metrics'][metric]) 
                         for data in rec['evaluation_matrix'].values()]
                avg_metrics[metric] = sum(values) / len(values)
            
            fig.add_trace(go.Scatterpolar(
                r=[avg_metrics[m] for m in metrics.keys()],
                theta=list(metrics.keys()),
                fill='toself',
                name='Média',
                line_color='#3498db'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )
                ),
                showlegend=True,
                title="Comparação com Média das DLTs"
            )
            
            st.plotly_chart(fig, use_container_width=True)

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")

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
