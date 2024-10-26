import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import get_recommendation, compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)
from utils import init_session_state

def create_gini_radar(gini):
    categories = ['Separação de Classes', 'Pureza dos Dados', 'Consistência', 'Precisão']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[1-gini, gini, 1-gini, gini],
        theta=categories,
        fill='toself',
        name='Índice de Gini'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Análise do Índice de Gini"
    )
    return fig

def create_entropy_graph(answers):
    entropy_values = []
    weights = {
        "security": float(0.4),
        "scalability": float(0.25),
        "energy_efficiency": float(0.20),
        "governance": float(0.15)
    }
    for i in range(len(answers)):
        partial_answers = dict(list(answers.items())[:i+1])
        classes = {k: v['score'] for k, v in get_recommendation(partial_answers, weights)['evaluation_matrix'].items()}
        entropy_values.append(calcular_entropia(classes))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(1, len(entropy_values) + 1)),
        y=entropy_values,
        mode='lines+markers',
        name='Evolução da Entropia'
    ))
    fig.update_layout(
        title="Evolução da Entropia Durante o Processo Decisório",
        xaxis_title="Número de Perguntas Respondidas",
        yaxis_title="Entropia (bits)"
    )
    return fig

def create_metrics_dashboard(depth, pruning_ratio, confidence):
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=depth,
        title={'text': "Profundidade da Árvore"},
        gauge={'axis': {'range': [0, 10]},
               'bar': {'color': "darkblue"}},
        domain={'row': 0, 'column': 0}
    ))
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=pruning_ratio * 100,
        title={'text': "Taxa de Poda (%)"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "darkgreen"}},
        domain={'row': 0, 'column': 1}
    ))
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        title={'text': "Confiança (%)"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "darkred"}},
        domain={'row': 0, 'column': 2}
    ))
    fig.update_layout(
        grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
        title="Dashboard de Métricas da Árvore de Decisão"
    )
    return fig

def show_metrics():
    st.header("Métricas Técnicas do Processo de Decisão")
    
    if 'recommendation' in st.session_state:
        rec = st.session_state.recommendation
        if 'evaluation_matrix' in rec:
            classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
            gini = calcular_gini(classes)
            entropy = calcular_entropia(classes)
            
            # Show Gini Index Visualization
            st.subheader("1. Índice de Gini")
            gini_fig = create_gini_radar(gini)
            st.plotly_chart(gini_fig, use_container_width=True)
            
            # Show Entropy Evolution
            st.subheader("2. Evolução da Entropia")
            entropy_fig = create_entropy_graph(st.session_state.answers)
            st.plotly_chart(entropy_fig, use_container_width=True)
            
            # Show Decision Tree Metrics Dashboard
            st.subheader("3. Dashboard de Métricas")
            depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
            total_nos = len(st.session_state.answers) * 2 + 1
            nos_podados = total_nos - len(st.session_state.answers) - 1
            pruning_ratio = calcular_pruning(total_nos, nos_podados)
            confidence = rec.get('confidence_value', 0.0)
            
            metrics_fig = create_metrics_dashboard(depth, pruning_ratio, confidence)
            st.plotly_chart(metrics_fig, use_container_width=True)

def show_reference_table():
    # Reference table implementation remains unchanged
    pass

def show_home_page():
    # Home page implementation remains unchanged
    pass

def show_user_profile():
    # User profile implementation remains unchanged
    pass

def main():
    # Main function implementation remains unchanged
    pass

if __name__ == "__main__":
    main()
