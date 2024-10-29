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

def create_metrics_radar_chart(gini, entropy, depth, pruning):
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[gini, entropy, depth, pruning],
        theta=['Índice de Gini', 'Entropia', 'Profundidade', 'Taxa de Poda'],
        fill='toself',
        name='Métricas Atuais'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True
    )
    return fig

def show_metrics():
    st.header("Métricas Técnicas do Processo de Decisão")
    
    if 'recommendation' in st.session_state:
        rec = st.session_state.recommendation
        if 'evaluation_matrix' in rec:
            classes = {k: float(v['score']) for k, v in rec['evaluation_matrix'].items()}
            gini = calcular_gini(classes)
            entropy = calcular_entropia(classes)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Índice de Gini Atual",
                    value=f"{gini:.3f}",
                    help="Quanto menor, melhor a separação entre as classes"
                )
            
            with col2:
                st.metric(
                    label="Entropia Atual",
                    value=f"{entropy:.3f} bits",
                    help="Quanto menor, mais certeza na decisão"
                )
            
            if 'answers' in st.session_state:
                depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
                total_nos = len(st.session_state.answers) * 2 + 1
                nos_podados = total_nos - len(st.session_state.answers) - 1
                pruning_ratio = calcular_pruning(total_nos, nos_podados)
                
                fig_radar = create_metrics_radar_chart(
                    gini,
                    entropy,
                    depth / 10,
                    pruning_ratio
                )
                st.plotly_chart(fig_radar, use_container_width=True)

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")

    st.markdown("## Referência de DLTs e Algoritmos")
    st.write("Abaixo está uma tabela detalhada com as principais DLTs e suas características para aplicações em saúde:")
    
    # Updated button with softer colors
    if st.button(
        "Iniciar Questionário",
        key="start_questionnaire",
        help="Clique para começar o processo de seleção de DLT",
        use_container_width=True,
        type="secondary"  # Using secondary type for softer color
    ):
        st.session_state.page = "Framework Proposto"
        st.experimental_rerun()

def show_user_profile():
    st.header(f"Perfil do Usuário: {st.session_state.username}")
    recommendations = get_user_recommendations(st.session_state.username)
    if recommendations:
        st.subheader("Últimas Recomendações")
        for rec in recommendations:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"DLT: {rec['dlt']}")
                    st.write(f"Consenso: {rec['consensus']}")
                    st.write(f"Data: {rec['timestamp']}")
                st.markdown("---")

def main():
    st.set_page_config(
        page_title="SeletorDLTSaude",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
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
            index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0,
            key="menu_select"
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
            # Updated logout button with softer color
            if st.sidebar.button(
                "Confirmar Logout",
                key="confirm_logout",
                type="secondary",
                use_container_width=True
            ):
                logout()
                st.session_state.page = 'Início'
                st.experimental_rerun()

if __name__ == "__main__":
    main()
