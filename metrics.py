import math
import numpy as np
import plotly.graph_objects as go
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

def calcular_peso_caracteristica(caracteristica, pesos_base, respostas):
    """
    Calcula o peso ajustado de uma característica específica com base nas respostas.
    """
    if not pesos_base or caracteristica not in pesos_base:
        return {
            'peso_ajustado': 0,
            'impacto_respostas': 0,
            'confianca': 0
        }
    
    total_pesos = sum(pesos_base.values())
    peso_base = pesos_base[caracteristica] / total_pesos if total_pesos > 0 else 0
    
    relacionadas = {
        'security': ['privacy', 'network_security'],
        'scalability': ['data_volume', 'integration'],
        'energy_efficiency': ['energy_efficiency'],
        'governance': ['governance_flexibility', 'interoperability']
    }
    
    respostas_relacionadas = [
        resp for q_id, resp in respostas.items()
        if q_id in relacionadas.get(caracteristica, [])
    ]
    
    num_respostas_positivas = sum(1 for resp in respostas_relacionadas if resp == "Sim")
    total_perguntas_relacionadas = len(relacionadas.get(caracteristica, []))
    
    impacto_respostas = num_respostas_positivas / total_perguntas_relacionadas if total_perguntas_relacionadas > 0 else 0
    peso_ajustado = peso_base * (1 + impacto_respostas * 0.5)
    confianca = len(respostas_relacionadas) / total_perguntas_relacionadas if total_perguntas_relacionadas > 0 else 0
    
    return {
        'peso_ajustado': peso_ajustado,
        'impacto_respostas': impacto_respostas,
        'confianca': confianca
    }

def show_metrics():
    """Display metrics and analysis."""
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
        
        # Adequação da Recomendação section
        st.header("Adequação da Recomendação")
        st.write("O framework proposto realiza uma análise multifatorial considerando:")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Características Avaliadas")
            st.write("• Segurança (40%)")
            st.write("• Escalabilidade (25%)")
            st.write("• Eficiência Energética (20%)")
            st.write("• Governança (15%)")

        with col2:
            st.subheader("Diferenciais do Framework")
            st.write("• Análise baseada em evidências acadêmicas")
            st.write("• Validação por métricas quantitativas")
            st.write("• Consideração de casos reais")
            st.write("• Recomendação personalizada")

        # Metrics visualization
        st.subheader("Visualização de Métricas")
        col3, col4 = st.columns(2)
        
        with col3:
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

        with col4:
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

        # Analysis conclusion
        with st.expander("Conclusão da Análise"):
            st.write("A recomendação é considerada adequada quando:")
            st.write("1. O índice de consistência é superior a 0.7")
            st.write("2. A distribuição de pesos reflete as prioridades do usuário")
            st.write("3. Os casos de uso alinham-se com o cenário proposto")
            st.write("4. As métricas técnicas atendem aos requisitos mínimos")

            # Calculate recommendation confidence
            weights = {
                "security": 0.4,
                "scalability": 0.25,
                "energy_efficiency": 0.20,
                "governance": 0.15
            }
            
            characteristic_weights = {
                char: calcular_peso_caracteristica(char, weights, answers)
                for char in weights.keys()
            }
            
            consistency_index = sum(
                weights[char] * characteristic_weights[char]['confianca'] 
                for char in weights.keys()
            )
            
            st.metric(
                label="Confiança da Recomendação",
                value=f"{consistency_index:.2%}",
                help="Baseado na consistência das respostas e alinhamento com requisitos"
            )

        # Generate downloadable report
        st.subheader("Relatório Completo")
        report_data = {
            "Métricas Técnicas": {
                "Índice de Gini": gini,
                "Entropia": entropy,
                "Profundidade": depth,
                "Taxa de Poda": pruning_metrics['pruning_ratio']
            },
            "Pesos das Características": {
                char: weights[char] for char in weights.keys()
            },
            "Índices de Confiança": {
                char: characteristic_weights[char]['confianca'] 
                for char in weights.keys()
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

def create_metrics_radar_chart(metrics_data):
    """Creates a radar chart for metrics visualization with tooltips."""
    fig = go.Figure()
    
    categories = list(metrics_data.keys())
    values = list(metrics_data.values())
    
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Métricas Atuais',
        hovertemplate="<b>%{theta}</b><br>" +
                     "Valor: %{r:.3f}<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        title="Visão Geral das Métricas"
    )
    return fig
