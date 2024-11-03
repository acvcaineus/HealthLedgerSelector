import math
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
from decision_logic import get_recommendation

def calcular_gini(classes):
    """Calcula a impureza de Gini para um conjunto de classes."""
    if not classes or sum(classes.values()) == 0:
        return 0
    total = sum(classes.values())
    gini = 1 - sum((count / total) ** 2 for count in classes.values())
    return gini

def calcular_entropia(classes):
    """Calcula a entropia de Shannon para um conjunto de classes."""
    if not classes or sum(classes.values()) == 0:
        return 0
    total = sum(classes.values())
    entropia = -sum((count / total) * math.log2(count / total) 
                   for count in classes.values() if count > 0)
    return entropia

def calcular_profundidade_decisoria(decisoes):
    """Calcula a profundidade média da árvore de decisão e métricas relacionadas."""
    if not decisoes:
        return {
            'profundidade_media': 0,
            'complexidade_arvore': 0,
            'num_caminhos': 0,
            'precisao': 0
        }
    profundidade_total = sum(decisoes)
    num_caminhos = len(decisoes)
    profundidade_media = profundidade_total / num_caminhos
    complexidade_arvore = math.log2(num_caminhos + 1)
    precisao = 1 - (profundidade_media / (2 * num_caminhos))
    
    return {
        'profundidade_media': profundidade_media,
        'complexidade_arvore': complexidade_arvore,
        'num_caminhos': num_caminhos,
        'precisao': precisao
    }

def create_metrics_visualization(metrics):
    """Creates a visualization for metrics."""
    fig = go.Figure()
    
    categories = ['Profundidade', 'Complexidade', 'Precisão', 'Cobertura']
    values = [
        metrics['profundidade_media'] / max(1, metrics['num_caminhos']),
        metrics['complexidade_arvore'] / 5,  # Normalized by typical max value
        metrics['precisao'],
        metrics['num_caminhos'] / 10  # Normalized coverage
    ]
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Métricas'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        title="Visualização de Métricas"
    )
    
    return fig

def create_evaluation_matrix(metrics):
    """Creates an evaluation matrix heatmap."""
    matrix_data = np.array([
        [metrics['precisao'], metrics['profundidade_media'] / max(1, metrics['num_caminhos'])],
        [metrics['complexidade_arvore'] / 5, metrics['num_caminhos'] / 10]
    ])
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix_data,
        x=['Precisão', 'Profundidade'],
        y=['Complexidade', 'Cobertura'],
        colorscale='RdBu',
        text=[[f'{val:.2f}' for val in row] for row in matrix_data],
        texttemplate='%{text}',
        textfont={"size": 14},
    ))
    
    fig.update_layout(
        title='Matriz de Avaliação',
        width=500,
        height=500
    )
    
    return fig

def show_metrics():
    """Display metrics and analysis."""
    st.title("Métricas e Análise")
    
    if 'answers' not in st.session_state or not st.session_state.answers:
        st.info("Complete o questionário para visualizar as métricas.")
        return
    
    metrics = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
    
    # 1. Metrics Overview
    st.subheader("1. Visão Geral das Métricas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Profundidade Média",
            f"{metrics['profundidade_media']:.2f}",
            help="Média de decisões necessárias"
        )
    with col2:
        st.metric(
            "Precisão",
            f"{metrics['precisao']:.2%}",
            help="Precisão do modelo"
        )
    with col3:
        st.metric(
            "Complexidade",
            f"{metrics['complexidade_arvore']:.2f}",
            help="Complexidade da árvore"
        )
    
    # 2. Metrics Visualization
    st.subheader("2. Visualização das Métricas")
    metrics_fig = create_metrics_visualization(metrics)
    st.plotly_chart(metrics_fig, use_container_width=True)
    
    # 3. Evaluation Matrix
    st.subheader("3. Matriz de Avaliação")
    matrix_fig = create_evaluation_matrix(metrics)
    st.plotly_chart(matrix_fig, use_container_width=True)
    
    # 4. Detailed Analysis
    with st.expander("Análise Detalhada"):
        st.markdown(f"""
        ### Métricas Detalhadas
        
        1. **Profundidade da Árvore**
           - Profundidade Média: {metrics['profundidade_media']:.2f}
           - Número de Caminhos: {metrics['num_caminhos']}
           
        2. **Precisão do Modelo**
           - Precisão: {metrics['precisao']:.2%}
           - Complexidade: {metrics['complexidade_arvore']:.2f}
        
        3. **Interpretação**
           - A profundidade média indica o número típico de decisões necessárias
           - A precisão indica a qualidade das recomendações
           - A complexidade reflete a sofisticação do modelo
        """)
    
    # 5. Download Report
    metrics_df = pd.DataFrame({
        'Métrica': ['Profundidade Média', 'Complexidade', 'Precisão', 'Número de Caminhos'],
        'Valor': [
            metrics['profundidade_media'],
            metrics['complexidade_arvore'],
            metrics['precisao'],
            metrics['num_caminhos']
        ]
    })
    
    csv = metrics_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Baixar Relatório",
        csv,
        "metricas.csv",
        "text/csv",
        key='download-metrics'
    )
