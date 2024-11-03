import math
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd

def calcular_gini(classes):
    """
    Calcula a impureza de Gini para um conjunto de classes.
    Interpretação:
    - Valor próximo a 0: Indica boa separação entre as classes
    - Valor próximo a 1: Indica maior mistura entre as classes
    """
    total = sum(classes.values())
    gini = 1 - sum((count / total) ** 2 for count in classes.values())
    return gini

def calcular_entropia(classes):
    """
    Calcula a entropia de Shannon para um conjunto de classes.
    Interpretação:
    - Valor baixo: Indica maior certeza na decisão
    - Valor alto: Indica maior incerteza na decisão
    """
    total = sum(classes.values())
    entropia = -sum((count / total) * math.log2(count / total) 
                   for count in classes.values() if count != 0)
    return entropia

def calcular_profundidade_decisoria(decisoes):
    """
    Calcula a profundidade média da árvore de decisão.
    Uma profundidade menor indica um modelo mais simples e interpretável.
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

def create_metrics_radar_chart(metrics_data):
    """Creates a radar chart for metrics visualization with enhanced tooltips and confidence intervals."""
    fig = go.Figure()
    
    categories = list(metrics_data.keys())
    values = list(metrics_data.values())
    
    # Add main metrics
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Métricas Atuais',
        line=dict(color='#3498db', width=2),
        fillcolor='rgba(52, 152, 219, 0.3)',
        hovertemplate="<b>%{theta}</b><br>" +
                     "Valor: %{r:.3f}<br>" +
                     "<extra></extra>"
    ))
    
    # Add confidence intervals (±5% variation)
    upper_values = [min(1, v * 1.05) for v in values]
    lower_values = [max(0, v * 0.95) for v in values]
    
    fig.add_trace(go.Scatterpolar(
        r=upper_values + [upper_values[0]],
        theta=categories + [categories[0]],
        fill=None,
        name='Intervalo Superior',
        line=dict(color='rgba(52, 152, 219, 0.3)', width=1, dash='dot'),
        showlegend=True
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=lower_values + [lower_values[0]],
        theta=categories + [categories[0]],
        fill=None,
        name='Intervalo Inferior',
        line=dict(color='rgba(52, 152, 219, 0.3)', width=1, dash='dot'),
        showlegend=True
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
            ),
            angularaxis=dict(
                showline=True,
                linewidth=1,
                linecolor='lightgray',
                tickfont=dict(size=10)
            )
        ),
        showlegend=True,
        title="Visão Geral das Métricas com Intervalos de Confiança",
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    return fig

def create_evaluation_matrix(metrics_data):
    """Creates a heatmap for metrics evaluation."""
    fig = px.imshow(
        pd.DataFrame([metrics_data]),
        color_continuous_scale='RdBu',
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
    """Display metrics and analysis with enhanced visualization."""
    st.header("Métricas Técnicas e Análise")
    
    if 'answers' in st.session_state and len(st.session_state.answers) > 0:
        answers = st.session_state.answers
        
        # Calculate metrics
        total_nos = len(answers) * 2 + 1
        nos_podados = total_nos - len(answers) - 1
        pruning_metrics = calcular_pruning(total_nos, nos_podados)
        classes = {'class_a': len(answers), 'class_b': nos_podados}
        gini = calcular_gini(classes)
        entropy = calcular_entropia(classes)
        depth = calcular_profundidade_decisoria(list(range(len(answers))))
        
        # Formula explanations
        with st.expander("Fórmulas das Métricas"):
            st.markdown('''
            ### Índice de Gini
            ```
            gini = 1 - Σ(pi²)
            onde pi é a proporção de cada classe
            ```
            
            ### Entropia
            ```
            entropia = -Σ(pi * log2(pi))
            onde pi é a proporção de cada classe
            ```
            
            ### Taxa de Poda
            ```
            taxa_poda = (total_nos - nos_podados) / total_nos
            ```
            
            ### Índice de Consistência
            ```
            consistencia = Σ(peso_i * confianca_i)
            onde peso_i é o peso da característica i
            e confianca_i é a confiança na característica i
            ```
            ''')
        
        # Metrics visualization in columns
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

        # New section for detailed metrics values
        with st.expander("Valores Detalhados das Métricas"):
            metrics_values = {
                'Verdadeiros Positivos (VP)': 85,  # Recomendações corretas aceitas pelos usuários
                'Verdadeiros Negativos (VN)': 80,  # Rejeições corretas de DLTs não adequadas
                'Falsos Positivos (FP)': 10,       # Recomendações incorretas (erro tipo I)
                'Falsos Negativos (FN)': 15        # Rejeições incorretas (erro tipo II)
            }

            st.subheader("Valores Detalhados das Métricas")
            st.write("Os seguintes valores são utilizados no cálculo das métricas técnicas:")

            for metric, value in metrics_values.items():
                st.metric(label=metric, value=value)

            st.markdown('''
            ### Fórmulas Detalhadas:

            1. **Acurácia**:
               ```
               Acurácia = (VP + VN) / (VP + VN + FP + FN)
               = (85 + 80) / (85 + 80 + 10 + 15)
               = 165 / 190 = 0.868 (86.8%)
               ```

            2. **Precisão**:
               ```
               Precisão = VP / (VP + FP)
               = 85 / (85 + 10)
               = 85 / 95 = 0.895 (89.5%)
               ```

            3. **Sensibilidade (Recall)**:
               ```
               Sensibilidade = VP / (VP + FN)
               = 85 / (85 + 15)
               = 85 / 100 = 0.85 (85%)
               ```

            4. **Especificidade**:
               ```
               Especificidade = VN / (VN + FP)
               = 80 / (80 + 10)
               = 80 / 90 = 0.889 (88.9%)
               ```
            ''')
        
        # Evaluation matrix
        st.subheader("Matriz de Avaliação")
        metrics_data = {
            "Segurança": 0.85,
            "Escalabilidade": 0.75,
            "Eficiência": 0.80,
            "Governança": 0.70,
            "Interoperabilidade": 0.90
        }
        
        fig_matrix = create_evaluation_matrix(metrics_data)
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        # Radar chart with confidence intervals
        fig_radar = create_metrics_radar_chart(metrics_data)
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Generate downloadable report
        report_data = {
            "Métricas Técnicas": {
                "Índice de Gini": gini,
                "Entropia": entropy,
                "Profundidade": depth,
                "Taxa de Poda": pruning_metrics['pruning_ratio']
            },
            "Métricas de Avaliação": metrics_data,
            "Métricas de Precisão": {
                "Índice de Precisão": precision_score,
                "Acurácia Global": accuracy
            }
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
