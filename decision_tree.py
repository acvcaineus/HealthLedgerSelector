import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def create_progress_animation(current_phase, answers, questions):
    # [Previous animation code remains unchanged]
    pass

def show_recommendation(answers, weights, questions):
    # [Previous recommendation code remains unchanged]
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação Final")
    
    # [Previous recommendation display code remains unchanged]
    
    # Add metrics navigation button at the bottom
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ver Métricas Detalhadas"):
            st.session_state.page = "Métricas"
            st.experimental_rerun()
    with col2:
        if st.button("Reiniciar Processo"):
            st.session_state.answers = {}
            st.experimental_rerun()
    
    return recommendation

def run_decision_tree():
    # [Previous code remains unchanged]
    pass

def restart_decision_tree():
    # [Previous code remains unchanged]
    pass
