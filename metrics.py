import math
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
from decision_logic import get_recommendation

def calcular_gini(classes):
    """
    Calcula a impureza de Gini para um conjunto de classes.
    """
    total = sum(classes.values())
    gini = 1 - sum((count / total) ** 2 for count in classes.values())
    return gini

def calcular_entropia(classes):
    """
    Calcula a entropia de Shannon para um conjunto de classes.
    """
    total = sum(classes.values())
    entropia = -sum((count / total) * math.log2(count / total) 
                   for count in classes.values() if count != 0)
    return entropia

def calcular_profundidade_decisoria(decisoes):
    """
    Calcula a profundidade média da árvore de decisão.
    """
    if not decisoes:
        return 0
    profundidade_total = sum(decisoes)
    return profundidade_total / len(decisoes)

def calcular_pruning(total_nos, nos_podados):
    """
    Calcula o pruning ratio e métricas relacionadas.
    """
    if total_nos == 0:
        return {
            'pruning_ratio': 0,
            'eficiencia_poda': 0,
            'impacto_complexidade': 0
        }
    
    pruning_ratio = (total_nos - nos_podados) / total_nos
    eficiencia_poda = 1 - (nos_podados / total_nos)
    impacto_complexidade = math.log2(total_nos / (total_nos - nos_podados + 1))
    
    return {
        'pruning_ratio': pruning_ratio,
        'eficiencia_poda': eficiencia_poda,
        'impacto_complexidade': impacto_complexidade
    }

def calculate_consistency_score(metrics, answers):
    """
    Calculate consistency score based on user answers and metrics.
    """
    if not answers or not metrics:
        return 0.0
    
    weights = {
        'security': 0.4,
        'scalability': 0.25,
        'energy_efficiency': 0.20,
        'governance': 0.15
    }
    
    score = 0
    total_weight = 0
    
    for key, weight in weights.items():
        if key in metrics:
            if answers.get('privacy') == 'Sim' and key == 'security':
                score += metrics[key] * weight * 1.2
            elif answers.get('scalability') == 'Sim' and key == 'scalability':
                score += metrics[key] * weight * 1.2
            elif answers.get('energy_efficiency') == 'Sim' and key == 'energy_efficiency':
                score += metrics[key] * weight * 1.2
            elif answers.get('governance_flexibility') == 'Sim' and key == 'governance':
                score += metrics[key] * weight * 1.2
            else:
                score += metrics[key] * weight
            total_weight += weight
    
    return score / total_weight if total_weight > 0 else 0

def create_metrics_radar_chart(metrics_data, recommendation=None, answers=None):
    """Creates a radar chart for metrics visualization with enhanced tooltips."""
    fig = go.Figure()
    
    if recommendation and answers:
        # Update metrics data with current recommendation values
        metrics_data.update(recommendation['metrics'])
        consistency_score = calculate_consistency_score(metrics_data, answers)
        
        # Add consistency score annotation
        fig.add_annotation(
            text=f"Índice de Consistência: {consistency_score:.2f}",
            xref="paper", yref="paper",
            x=0.5, y=1.1,
            showarrow=False,
            font=dict(size=14)
        )
    
    categories = list(metrics_data.keys())
    values = list(metrics_data.values())
    
    # Add main metrics
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Métricas Atuais',
        line=dict(color='#3498db', width=2),
        fillcolor='rgba(52, 152, 219, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showline=True,
                linewidth=1,
                linecolor='lightgray',
                tickfont=dict(size=10)
            )
        ),
        showlegend=True,
        title="Visão Geral das Métricas"
    )
    return fig

def create_evaluation_matrix(metrics_data, recommendation=None, answers=None):
    """Creates a heatmap for metrics evaluation with current recommendation data."""
    if recommendation and 'metrics' in recommendation:
        metrics_data.update(recommendation['metrics'])
    
    df = pd.DataFrame([metrics_data])
    
    # Create custom color scale based on user preferences
    if answers:
        color_scale = []
        for metric in df.columns:
            if (metric == 'security' and answers.get('privacy') == 'Sim') or \
               (metric == 'scalability' and answers.get('scalability') == 'Sim') or \
               (metric == 'energy_efficiency' and answers.get('energy_efficiency') == 'Sim') or \
               (metric == 'governance' and answers.get('governance_flexibility') == 'Sim'):
                color_scale.append('darkred')
            else:
                color_scale.append('royalblue')
    else:
        color_scale = 'RdBu'
    
    fig = px.imshow(
        df,
        color_continuous_scale=color_scale,
        aspect='auto',
        title="Matriz de Avaliação de Métricas"
    )
    
    fig.update_layout(
        xaxis_title="Métricas",
        yaxis_title="Avaliação",
        yaxis_visible=False
    )
    
    return fig

def show_metrics():
    """Display metrics and analysis with enhanced visualization and state synchronization."""
    st.header("Métricas Técnicas e Análise")
    
    if 'answers' in st.session_state and len(st.session_state.answers) > 0:
        answers = st.session_state.answers
        current_recommendation = None
        
        if 'current_recommendation' in st.session_state:
            current_recommendation = st.session_state.current_recommendation
        else:
            current_recommendation = get_recommendation(answers)
            st.session_state.current_recommendation = current_recommendation
        
        # Calculate metrics
        total_nos = len(answers) * 2 + 1
        nos_podados = total_nos - len(answers) - 1
        pruning_metrics = calcular_pruning(total_nos, nos_podados)
        classes = {'class_a': len(answers), 'class_b': nos_podados}
        gini = calcular_gini(classes)
        entropy = calcular_entropia(classes)
        depth = calcular_profundidade_decisoria(list(range(len(answers))))
        
        # Display metrics in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Índice de Gini",
                value=f"{gini:.3f}",
                help="Medida de pureza da classificação. Valores próximos a 0 indicam melhor separação."
            )
            st.metric(
                label="Entropia",
                value=f"{entropy:.3f}",
                help="Medida de incerteza na decisão. Valores menores indicam maior certeza."
            )
        
        with col2:
            st.metric(
                label="Profundidade",
                value=f"{depth:.2f}",
                help="Número médio de decisões. Menor profundidade indica processo mais direto."
            )
            st.metric(
                label="Taxa de Poda",
                value=f"{pruning_metrics['pruning_ratio']:.2%}",
                help="Proporção de simplificação do modelo. Maior taxa indica melhor otimização."
            )
        
        # Technical metrics visualization
        st.subheader("Métricas Técnicas")
        metrics_data = {
            "security": 0.85,
            "scalability": 0.75,
            "energy_efficiency": 0.80,
            "governance": 0.70
        }
        
        # Update metrics with current recommendation
        if current_recommendation and 'metrics' in current_recommendation:
            metrics_data.update({k.lower(): v for k, v in current_recommendation['metrics'].items()})
        
        # Create and display evaluation matrix
        fig_matrix = create_evaluation_matrix(metrics_data, current_recommendation, answers)
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        # Create and display radar chart
        fig_radar = create_metrics_radar_chart(metrics_data, current_recommendation, answers)
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Generate downloadable report
        report_data = {
            "Métricas Técnicas": {
                "Índice de Gini": gini,
                "Entropia": entropy,
                "Profundidade": depth,
                "Taxa de Poda": pruning_metrics['pruning_ratio']
            },
            "Métricas de Avaliação": metrics_data
        }
        
        if current_recommendation:
            report_data["Recomendação"] = {
                "DLT": current_recommendation.get('dlt', 'N/A'),
                "Tipo": current_recommendation.get('dlt_type', 'N/A'),
                "Grupo": current_recommendation.get('group', 'N/A'),
                "Consistência": calculate_consistency_score(metrics_data, answers)
            }
        
        df_report = pd.DataFrame.from_dict(report_data, orient='index')
        csv = df_report.to_csv().encode('utf-8')
        
        st.download_button(
            label="Baixar Relatório Completo",
            data=csv,
            file_name="relatorio_metricas.csv",
            mime="text/csv",
            help="Baixe o relatório completo com todas as métricas e análises"
        )
    else:
        st.info("Complete o questionário para visualizar as métricas detalhadas.")
