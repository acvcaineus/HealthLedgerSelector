import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao, get_metric_interpretation)
from utils import init_session_state

def show_metrics():
    """Display enhanced metrics and analysis"""
    st.title("Métricas do Processo de Decisão")
    
    if 'recommendation' not in st.session_state:
        st.warning("Complete o processo de recomendação primeiro para ver as métricas.")
        if st.button("Ir para o Framework"):
            st.session_state.page = "Framework Proposto"
            st.experimental_rerun()
        return
    
    try:
        rec = st.session_state.recommendation
        
        # Accuracy metrics
        with st.expander("Precisão (Accuracy)", expanded=True):
            st.write("### Métricas de Precisão")
            if 'evaluation_matrix' in rec:
                scores = [float(data['score']) for data in rec['evaluation_matrix'].values()]
                correct_decisions = sum(1 for score in scores if score > 0.7)
                total_decisions = len(scores)
                
                col1, col2 = st.columns(2)
                with col1:
                    fig = go.Figure(data=[
                        go.Bar(name='Decisões Corretas', x=['Precisão'], y=[correct_decisions]),
                        go.Bar(name='Total', x=['Precisão'], y=[total_decisions])
                    ])
                    fig.update_layout(title="Precisão das Recomendações")
                    st.plotly_chart(fig)
                    
                    accuracy = correct_decisions / total_decisions if total_decisions > 0 else 0
                    st.metric("Precisão", f"{accuracy:.2%}")
                
                with col2:
                    st.write('''
                    A precisão mede a proporção de decisões corretas em relação ao total.
                    
                    **Interpretação:**
                    - Valores altos (>70%): Sistema confiável
                    - Valores médios (40-70%): Sistema adequado
                    - Valores baixos (<40%): Necessita ajustes
                    ''')
            else:
                st.warning("Dados de avaliação não disponíveis")
        
        # Detailed metrics analysis
        with st.expander("Análise Detalhada de Métricas"):
            st.write("### Métricas de Avaliação")
            
            col1, col2 = st.columns(2)
            with col1:
                # Calculate and display metrics with explanations
                if 'answers' in st.session_state:
                    depth = len(st.session_state.answers)
                    total_nodes = depth * 2 + 1
                    pruned_nodes = total_nodes - depth - 1
                    pruning_ratio = calcular_pruning(total_nodes, pruned_nodes)
                    
                    metrics_data = {
                        "depth": depth,
                        "pruning": pruning_ratio,
                        "confidence": rec.get('confidence_value', 0)
                    }
                    
                    for metric_name, value in metrics_data.items():
                        interpretation = get_metric_interpretation(metric_name, value)
                        if interpretation:
                            st.metric(interpretation["title"], f"{value:.2f}")
                            st.info(interpretation["description"])
                            st.success(interpretation["interpretation"])
            
            with col2:
                # Visualization of metrics
                if 'evaluation_matrix' in rec:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=float(rec.get('confidence_value', 0)) * 100,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Confiabilidade da Recomendação"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'steps': [
                                {'range': [0, 40], 'color': "lightgray"},
                                {'range': [40, 70], 'color': "gray"},
                                {'range': [70, 100], 'color': "darkgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 70
                            }
                        }
                    ))
                    st.plotly_chart(fig)
        
        # Add navigation buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Retornar ao Framework"):
                st.session_state.page = "Framework Proposto"
                st.experimental_rerun()
        with col2:
            if st.button("Voltar ao Início"):
                st.session_state.page = "Início"
                st.experimental_rerun()
    
    except Exception as e:
        st.error(f"Erro ao processar métricas: {str(e)}")
        st.info("Por favor, tente reiniciar o processo de recomendação")
        if st.button("Reiniciar"):
            st.session_state.page = "Framework Proposto"
            st.experimental_rerun()

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    
    st.markdown("""
    ### Bem-vindo ao SeletorDLTSaude
    
    Este sistema ajuda você a escolher a melhor tecnologia de ledger distribuído (DLT) 
    e algoritmo de consenso para seu projeto na área de saúde.
    
    #### Como funciona:
    1. Responda a perguntas sobre seus requisitos
    2. Receba recomendações personalizadas
    3. Analise métricas detalhadas
    4. Compare diferentes soluções
    """)
    
    if st.button("Iniciar Seleção"):
        st.session_state.page = "Framework Proposto"
        st.experimental_rerun()

def show_user_profile():
    if not is_authenticated():
        st.warning("Faça login para ver seu perfil")
        return
        
    st.header(f"Perfil do Usuário: {st.session_state.username}")
    recommendations = get_user_recommendations(st.session_state.username)
    
    if recommendations:
        st.subheader("Suas Recomendações")
        for rec in recommendations:
            with st.expander(f"Recomendação - {rec['timestamp']}", expanded=False):
                st.write(f"**DLT:** {rec['dlt']}")
                st.write(f"**Algoritmo:** {rec['consensus']}")
                st.write("---")
    else:
        st.info("Você ainda não tem recomendações salvas.")

def main():
    st.set_page_config(
        page_title="SeletorDLTSaude",
        page_icon="🏥",
        layout="wide"
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
        pages = {
            "Início": show_home_page,
            "Framework Proposto": run_decision_tree,
            "Métricas": show_metrics,
            "Perfil": show_user_profile,
            "Logout": logout
        }
        
        page = st.sidebar.selectbox("Navegação", list(pages.keys()))
        
        if page != "Logout":
            pages[page]()
        else:
            logout()
            st.experimental_rerun()

if __name__ == "__main__":
    main()
