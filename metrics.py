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
    Calcula a profundidade média e máxima da árvore de decisão.
    """
    if not decisoes:
        return {'media': 0, 'maxima': 0, 'caminhos': []}
    
    profundidades = []
    caminho_atual = 0
    caminhos = []
    
    for i, decisao in enumerate(decisoes):
        if decisao == 'Sim':
            caminho_atual += 1
        profundidades.append(caminho_atual)
        caminhos.append(f"Nível {caminho_atual}: Decisão {i+1}")
    
    return {
        'media': sum(profundidades) / len(profundidades),
        'maxima': max(profundidades),
        'caminhos': caminhos
    }

def calcular_pruning(total_nos, nos_podados):
    """
    Calcula o pruning ratio e métricas relacionadas.
    """
    pruning_ratio = (total_nos - nos_podados) / total_nos if total_nos > 0 else 0
    eficiencia_poda = 1 - (nos_podados / total_nos) if total_nos > 0 else 0
    impacto_complexidade = math.log2(total_nos / (total_nos - nos_podados + 1))
    
    return {
        'pruning_ratio': pruning_ratio,
        'eficiencia_poda': eficiencia_poda,
        'impacto_complexidade': impacto_complexidade
    }

def calculate_precision_metrics(true_positives, false_positives, false_negatives, total_cases):
    """Calculate precision, sensitivity, and accuracy metrics."""
    try:
        precision = true_positives / (true_positives + false_positives)
    except ZeroDivisionError:
        precision = 0

    try:
        sensitivity = true_positives / (true_positives + false_negatives)
    except ZeroDivisionError:
        sensitivity = 0

    try:
        accuracy = (true_positives + (total_cases - (true_positives + false_positives + false_negatives))) / total_cases
    except ZeroDivisionError:
        accuracy = 0

    return {
        'precision': precision,
        'sensitivity': sensitivity,
        'accuracy': accuracy
    }

def calculate_consistency_score(metrics, answers):
    """Calculate consistency score based on user answers and metrics."""
    if not answers or not metrics:
        return 0.0
    
    weights = {
        'security': 0.25,
        'scalability': 0.25,
        'energy_efficiency': 0.25,
        'governance': 0.25
    }
    
    score = 0
    total_weight = 0
    
    for key, weight in weights.items():
        if key in metrics:
            score += metrics[key] * weight
            total_weight += weight
    
    return score / total_weight if total_weight > 0 else 0

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
        
        # Calculate tree depth metrics with visualization
        profundidade_metrics = calcular_profundidade_decisoria(list(answers.values()))
        
        # Tree Depth Analysis Section
        st.subheader("Análise de Profundidade da Árvore")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Profundidade Média", f"{profundidade_metrics['media']:.2f}")
            st.metric("Profundidade Máxima", f"{profundidade_metrics['maxima']}")
        
        with col2:
            # Create visualization of tree depth
            depth_fig = go.Figure()
            x_values = list(range(1, len(profundidade_metrics['caminhos']) + 1))
            y_values = [int(caminho.split(':')[0].split()[-1]) for caminho in profundidade_metrics['caminhos']]
            
            depth_fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines+markers',
                name='Profundidade',
                line=dict(color='#3498db', width=2),
                marker=dict(size=8)
            ))
            
            depth_fig.update_layout(
                title="Visualização da Profundidade da Árvore",
                xaxis_title="Número da Decisão",
                yaxis_title="Nível de Profundidade",
                showlegend=False
            )
            
            st.plotly_chart(depth_fig, use_container_width=True)
        
        with st.expander("Detalhes da Profundidade"):
            st.markdown("""
            ### Fórmulas de Profundidade
            ```python
            Profundidade Média = Σ(profundidade_nós) / total_nós
            Profundidade Máxima = max(profundidade_nós)
            ```
            
            ### Interpretação
            - **Profundidade Média**: Indica o número médio de decisões necessárias
            - **Profundidade Máxima**: Mostra o caminho mais longo na árvore
            - **Caminhos**: Sequência de decisões tomadas
            """)
            
            st.write("### Caminhos de Decisão")
            for caminho in profundidade_metrics['caminhos']:
                st.write(f"• {caminho}")
        
        # Calculate precision metrics
        true_positives = len([a for a in answers.values() if a == 'Sim'])
        false_positives = len([a for a in answers.values() if a == 'Não'])
        false_negatives = nos_podados
        precision_metrics = calculate_precision_metrics(true_positives, false_positives, false_negatives, total_nos)
        
        # Display formulas
        with st.expander("Fórmulas das Métricas"):
            st.markdown("""
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
            
            ### Precisão
            ```
            precisao = verdadeiros_positivos / (verdadeiros_positivos + falsos_positivos)
            ```
            
            ### Sensibilidade
            ```
            sensibilidade = verdadeiros_positivos / (verdadeiros_positivos + falsos_negativos)
            ```
            
            ### Acurácia
            ```
            acuracia = (verdadeiros_positivos + verdadeiros_negativos) / total_casos
            ```
            """)
        
        # Display other metrics
        st.subheader("Métricas de Qualidade")
        col3, col4 = st.columns(2)
        with col3:
            st.metric("Índice de Gini", f"{gini:.3f}")
            st.metric("Entropia", f"{entropy:.3f}")
        with col4:
            st.metric("Taxa de Poda", f"{pruning_metrics['pruning_ratio']:.2%}")
            if current_recommendation and 'metrics' in current_recommendation:
                consistency_index = calculate_consistency_score(current_recommendation['metrics'], answers)
                st.metric("Índice de Consistência", f"{consistency_index:.2f}")
        
        # Precision Analysis Section
        st.subheader("Análise de Precisão")
        col5, col6 = st.columns(2)
        with col5:
            st.metric("Precisão", f"{precision_metrics['precision']:.3f}")
            st.metric("Sensibilidade", f"{precision_metrics['sensitivity']:.3f}")
        with col6:
            st.metric("Acurácia", f"{precision_metrics['accuracy']:.3f}")
        
        # Generate downloadable report
        report_data = {
            "Métricas da Árvore": {
                "Profundidade Média": profundidade_metrics['media'],
                "Profundidade Máxima": profundidade_metrics['maxima'],
                "Índice de Gini": gini,
                "Entropia": entropy,
                "Taxa de Poda": pruning_metrics['pruning_ratio']
            },
            "Métricas de Precisão": {
                "Precisão": precision_metrics['precision'],
                "Sensibilidade": precision_metrics['sensitivity'],
                "Acurácia": precision_metrics['accuracy']
            }
        }
        
        if current_recommendation:
            report_data["Recomendação"] = {
                "DLT": current_recommendation.get('dlt', 'N/A'),
                "Tipo": current_recommendation.get('dlt_type', 'N/A'),
                "Grupo": current_recommendation.get('group', 'N/A'),
                "Consistência": calculate_consistency_score(current_recommendation.get('metrics', {}), answers)
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
