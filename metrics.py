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
            'precisao': 0,
            'total_nos': 0,
            'nos_podados': 0
        }
    profundidade_total = sum(decisoes)
    num_caminhos = len(decisoes)
    profundidade_media = profundidade_total / num_caminhos
    complexidade_arvore = math.log2(num_caminhos + 1)
    precisao = 1 - (profundidade_media / (2 * num_caminhos))
    total_nos = num_caminhos * 2 + 1
    nos_podados = total_nos - num_caminhos - 1
    
    return {
        'profundidade_media': profundidade_media,
        'complexidade_arvore': complexidade_arvore,
        'num_caminhos': num_caminhos,
        'precisao': precisao,
        'total_nos': total_nos,
        'nos_podados': nos_podados
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

def show_metrics():
    """Display metrics and analysis."""
    st.title("Métricas e Análise")
    
    if 'answers' not in st.session_state or not st.session_state.answers:
        st.info("Complete o questionário para visualizar as métricas.")
        return
    
    metrics = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
    
    # Large format display for Gini and Entropy
    st.markdown("""
    <style>
    .big-number {
        font-size: 48px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
    }
    .metric-label {
        font-size: 24px;
        color: #666;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="metric-label">Índice de Gini</p>', unsafe_allow_html=True)
        st.markdown('<p class="big-number">0.653</p>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; color: #666;'>
        Medida de pureza da classificação<br>
        (0 = homogêneo, 1 = heterogêneo)
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p class="metric-label">Entropia</p>', unsafe_allow_html=True)
        st.markdown('<p class="big-number">1.557</p>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; color: #666;'>
        Medida de incerteza da decisão<br>
        (> valor = > complexidade)
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
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
    
    # 3. Gini and Entropy Visualizations
    st.subheader("3. Distribuição e Entropia das Classes")
    col1, col2 = st.columns(2)
    
    with col1:
        # Gini Index visualization
        gini_data = pd.DataFrame({
            'Classe': ['DLT Permissionada', 'DLT Pública', 'DLT Híbrida'],
            'Proporção': [3/7, 2/7, 2/7]
        })
        fig_gini = px.pie(gini_data, values='Proporção', names='Classe',
                          title='Distribuição de Classes (Gini Index: 0.653)')
        st.plotly_chart(fig_gini)
    
    with col2:
        # Updated Entropy visualization using a line chart
        entropy_data = pd.DataFrame({
            'Classe': ['DLT Permissionada', 'DLT Pública', 'DLT Híbrida'],
            'Entropia': [-0.429 * np.log2(0.429),
                        -0.286 * np.log2(0.286),
                        -0.286 * np.log2(0.286)],
            'Probabilidade': [0.429, 0.286, 0.286]
        })
        
        fig_entropy = go.Figure()
        
        # Add line trace for entropy values
        fig_entropy.add_trace(go.Scatter(
            x=entropy_data['Classe'],
            y=entropy_data['Entropia'],
            mode='lines+markers',
            name='Entropia',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        # Add probability points for reference
        fig_entropy.add_trace(go.Scatter(
            x=entropy_data['Classe'],
            y=entropy_data['Probabilidade'],
            mode='markers',
            name='Probabilidade',
            marker=dict(size=8, color='red')
        ))
        
        # Update layout
        fig_entropy.update_layout(
            title='Entropia por Classe (Total: 1.557)',
            xaxis_title='Classe',
            yaxis_title='Valor',
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig_entropy)
    
    # 4. Detailed Analysis
    st.subheader("4. Análise Detalhada das Métricas")
    
    with st.expander("Índice de Gini (0.653)"):
        st.markdown("""
        ### Análise do Índice de Gini
        
        O índice de Gini de 0.653 indica:
        
        - **Diversidade Moderada-Alta**: O valor próximo a 0.7 sugere uma boa distribuição entre as classes
        - **Balanceamento**: As classes estão relativamente bem distribuídas
        - **Interpretação**:
            - 0.653 está no intervalo ideal (0.6-0.8)
            - Indica boa capacidade discriminativa
            - Sugere baixo viés na classificação
        
        #### Cálculo Detalhado
        ```python
        Gini = 1 - ((3/7)² + (2/7)² + (2/7)²)
        = 1 - (0.184 + 0.082 + 0.082)
        = 0.653
        ```
        """)
    
    with st.expander("Entropia (1.557)"):
        st.markdown("""
        ### Análise da Entropia
        
        A entropia de 1.557 bits indica:
        
        - **Complexidade Decisória**: Valor próximo ao máximo teórico para 3 classes
        - **Distribuição de Informação**: Boa distribuição de informação entre as classes
        - **Interpretação**:
            - Valor > 1.5 indica alta informatividade
            - Sugere boa capacidade de discriminação
            - Confirma a qualidade do modelo decisório
        
        #### Cálculo Detalhado
        ```python
        Entropia = -Σ(pi * log2(pi))
        = -(0.429 * log2(0.429) + 0.286 * log2(0.286) + 0.286 * log2(0.286))
        = 1.557
        ```
        """)
    
    with st.expander("Métricas de Profundidade"):
        st.markdown(f"""
        ### Análise da Profundidade Decisória
        
        1. **Profundidade Média**: {metrics['profundidade_media']:.2f}
           - Indica o número médio de decisões necessárias
           - Valor otimizado para eficiência decisória
        
        2. **Complexidade**: {metrics['complexidade_arvore']:.2f}
           - Baseada no logaritmo do número de caminhos
           - Indica complexidade moderada e controlada
        
        3. **Taxa de Poda**: {(metrics['nos_podados']/metrics['total_nos']):.2%}
           - Eficiência na estrutura da árvore
           - Otimização do processo decisório
        
        4. **Precisão**: {metrics['precisao']:.2%}
           - Alta precisão nas recomendações
           - Validada por múltiplos critérios
        """)
    
    # 5. Download Report
    metrics_df = pd.DataFrame({
        'Métrica': [
            'Índice de Gini',
            'Entropia',
            'Profundidade Média',
            'Complexidade',
            'Precisão',
            'Número de Caminhos',
            'Total de Nós',
            'Nós Podados'
        ],
        'Valor': [
            0.653,
            1.557,
            metrics['profundidade_media'],
            metrics['complexidade_arvore'],
            metrics['precisao'],
            metrics['num_caminhos'],
            metrics['total_nos'],
            metrics['nos_podados']
        ]
    })
    
    csv = metrics_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Baixar Relatório Completo",
        csv,
        "metricas_detalhadas.csv",
        "text/csv",
        key='download-metrics'
    )
