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
    if not classes or sum(classes.values()) == 0:
        return 0
    total = sum(classes.values())
    gini = 1 - sum((count / total) ** 2 for count in classes.values())
    return gini

def calcular_entropia(classes):
    """
    Calcula a entropia de Shannon para um conjunto de classes.
    """
    if not classes or sum(classes.values()) == 0:
        return 0
    total = sum(classes.values())
    entropia = -sum((count / total) * math.log2(count / total) 
                   for count in classes.values() if count > 0)
    return entropia

def calcular_profundidade_decisoria(decisoes):
    """
    Calcula a profundidade média da árvore de decisão.
    """
    if not decisoes:
        return {
            'profundidade_media': 0,
            'complexidade_arvore': 0,
            'num_caminhos': 0
        }
    profundidade_total = sum(decisoes)
    num_caminhos = len(decisoes)
    profundidade_media = profundidade_total / num_caminhos
    complexidade_arvore = math.log2(num_caminhos + 1)
    return {
        'profundidade_media': profundidade_media,
        'complexidade_arvore': complexidade_arvore,
        'num_caminhos': num_caminhos
    }

def create_tree_depth_visualization(depth_metrics):
    """
    Creates a visualization for tree depth metrics.
    """
    fig = go.Figure()
    
    metrics_data = [
        ('Profundidade Média', depth_metrics['profundidade_media'], '#3498db'),
        ('Complexidade', depth_metrics['complexidade_arvore'], '#2ecc71')
    ]
    
    for name, value, color in metrics_data:
        fig.add_trace(go.Bar(
            name=name,
            x=[name],
            y=[value],
            text=[f"{value:.2f}"],
            textposition='auto',
            marker_color=color,
            hovertemplate=f'{name}: %{{y:.2f}}<extra></extra>'
        ))

    fig.update_layout(
        title={
            'text': "Métricas de Profundidade da Árvore",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis_title="Valor",
        barmode='group',
        showlegend=True,
        height=400,
        paper_bgcolor='white',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.1)',
            zerolinecolor='rgba(0,0,0,0.2)'
        )
    )
    
    return fig

def show_metrics():
    """Display metrics and analysis with enhanced visualization."""
    st.header("Métricas Técnicas e Análise")
    
    if 'answers' in st.session_state and st.session_state.answers:
        answers = st.session_state.answers
        
        # Calculate metrics
        total_nos = len(answers) * 2 + 1
        nos_podados = total_nos - len(answers) - 1
        classes = {'class_a': len(answers), 'class_b': nos_podados}
        
        # Calculate all metrics
        gini = calcular_gini(classes)
        entropy = calcular_entropia(classes)
        depth_metrics = calcular_profundidade_decisoria(list(range(len(answers))))
        
        # Display depth metrics
        st.subheader("Análise de Profundidade da Árvore")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Profundidade Média",
                f"{depth_metrics['profundidade_media']:.2f}",
                help="Média do número de decisões necessárias para chegar a uma recomendação"
            )
        with col2:
            st.metric(
                "Complexidade da Árvore",
                f"{depth_metrics['complexidade_arvore']:.2f}",
                help="Medida logarítmica da complexidade total da árvore de decisão"
            )
        
        # Display tree depth visualization
        depth_fig = create_tree_depth_visualization(depth_metrics)
        st.plotly_chart(depth_fig, use_container_width=True)
        
        # Display metrics interpretation
        with st.expander("Interpretação das Métricas"):
            st.markdown(f"""
            ### Métricas Atuais
            
            1. **Profundidade Média: {depth_metrics['profundidade_media']:.2f}**
               - Indica o número médio de perguntas necessárias
               - Valores menores sugerem decisões mais eficientes
            
            2. **Complexidade da Árvore: {depth_metrics['complexidade_arvore']:.2f}**
               - Medida logarítmica do tamanho total da árvore
               - Reflete a diversidade de caminhos possíveis
            
            3. **Índice de Gini: {gini:.3f}**
               - Mede a pureza da classificação
               - Valores próximos a 0 indicam melhor separação
            
            4. **Entropia: {entropy:.3f}**
               - Mede a incerteza na classificação
               - Valores menores indicam maior confiança
            """)
        
        # Generate downloadable report
        report_data = {
            "Métricas de Profundidade": {
                "Profundidade Média": depth_metrics['profundidade_media'],
                "Complexidade da Árvore": depth_metrics['complexidade_arvore'],
                "Número de Caminhos": depth_metrics['num_caminhos']
            },
            "Métricas de Classificação": {
                "Índice de Gini": gini,
                "Entropia": entropy
            }
        }
        
        df_report = pd.DataFrame.from_dict(report_data, orient='index')
        csv = df_report.to_csv().encode('utf-8')
        
        st.download_button(
            label="Baixar Relatório de Métricas",
            data=csv,
            file_name="metricas_detalhadas.csv",
            mime="text/csv",
            help="Baixe o relatório detalhado com todas as métricas"
        )
    else:
        st.info("Complete o questionário para visualizar as métricas detalhadas.")
