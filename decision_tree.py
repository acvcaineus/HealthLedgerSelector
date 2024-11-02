import streamlit as st
import plotly.graph_objects as go
import math
import pandas as pd
from decision_logic import get_recommendation, consensus_algorithms, consensus_groups, compare_algorithms
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_peso_caracteristica, get_metric_explanation)

def create_progress_animation(current_phase, answers, questions):
    """Create an animated progress visualization."""
    phases = ["Aplicação", "Consenso", "Infraestrutura", "Internet"]
    
    # Create base figure
    fig = go.Figure()
    
    # Calculate progress for each phase
    phase_progress = {phase: 0 for phase in phases}
    questions_per_phase = {phase: 0 for phase in phases}
    
    # Count total questions per phase
    for q in questions:
        questions_per_phase[q["phase"]] += 1
    
    # Calculate answered questions per phase
    for q in questions:
        if q["id"] in answers:
            phase_progress[q["phase"]] += 1
    
    # Convert to percentages
    for phase in phases:
        if questions_per_phase[phase] > 0:
            phase_progress[phase] = (phase_progress[phase] / questions_per_phase[phase]) * 100
    
    # Colors for different phases
    colors = {
        "Aplicação": "#1f77b4",  # Blue
        "Consenso": "#2ca02c",   # Green
        "Infraestrutura": "#ff7f0e",  # Orange
        "Internet": "#d62728"    # Red
    }
    
    # Add bars for each phase
    for i, phase in enumerate(phases):
        fig.add_trace(go.Bar(
            name=phase,
            x=[phase],
            y=[phase_progress[phase]],
            marker_color=colors[phase],
            text=f"{phase_progress[phase]:.0f}%",
            textposition='auto',
        ))
    
    # Update layout
    fig.update_layout(
        title="Progresso por Fase",
        yaxis_title="Progresso (%)",
        yaxis=dict(range=[0, 100]),
        showlegend=True,
        barmode='group',
        height=300
    )
    
    # Add phase descriptions
    descriptions = {
        "Aplicação": "Questões sobre privacidade e integração",
        "Consenso": "Questões sobre segurança e escalabilidade",
        "Infraestrutura": "Questões sobre volume de dados e eficiência",
        "Internet": "Questões sobre governança e interoperabilidade"
    }
    
    # Add annotations for current phase
    if current_phase in phases:
        fig.add_annotation(
            x=current_phase,
            y=phase_progress[current_phase],
            text="Fase Atual",
            showarrow=True,
            arrowhead=1
        )
    
    return fig

def create_evaluation_matrices(recommendation):
    """Create and display evaluation matrices for DLTs, algorithm groups, and consensus algorithms."""
    if not recommendation or 'evaluation_matrix' not in recommendation:
        return
    
    st.subheader("🎯 Matrizes de Avaliação")
    
    # DLT Matrix
    st.markdown("### Matriz de DLTs")
    dlt_matrix = pd.DataFrame.from_dict(
        {k: v['metrics'] for k, v in recommendation['evaluation_matrix'].items()},
        orient='index'
    )
    st.dataframe(dlt_matrix)
    
    # Create radar chart for DLT comparison
    fig_dlt = go.Figure()
    metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
    
    for dlt, data in recommendation['evaluation_matrix'].items():
        values = [data['metrics'].get(m, 0) for m in metrics]
        values.append(values[0])  # Close the polygon
        fig_dlt.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics + [metrics[0]],
            name=dlt,
            fill='toself'
        ))
    
    fig_dlt.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True,
        title="Comparação de DLTs"
    )
    st.plotly_chart(fig_dlt)
    
    # Algorithm Groups Matrix
    if 'consensus_group' in recommendation and recommendation['consensus_group'] in consensus_groups:
        st.markdown("### Matriz de Grupos de Algoritmos")
        group_data = consensus_groups[recommendation['consensus_group']]['characteristics']
        group_df = pd.DataFrame([group_data])
        st.dataframe(group_df)
    
    # Consensus Algorithms Matrix
    if 'consensus' in recommendation:
        st.markdown("### Matriz de Algoritmos de Consenso")
        consensus_data = {
            alg: metrics for alg, metrics in consensus_algorithms.items()
            if alg in consensus_groups[recommendation['consensus_group']]['algorithms']
        }
        consensus_df = pd.DataFrame.from_dict(consensus_data, orient='index')
        st.dataframe(consensus_df)

def show_metrics():
    st.header("Métricas Técnicas do Processo de Decisão")
    
    if 'recommendation' in st.session_state and 'answers' in st.session_state:
        rec = st.session_state.recommendation
        answers = st.session_state.answers
        
        # Calculate all metrics
        if 'evaluation_matrix' in rec:
            classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
            gini = calcular_gini(classes)
            entropy = calcular_entropia(classes)
            depth = calcular_profundidade_decisoria(list(range(len(answers))))
            
            # Calculate pruning metrics
            total_nos = len(answers) * 2 + 1
            nos_podados = total_nos - len(answers) - 1
            pruning_metrics = calcular_pruning(total_nos, nos_podados)
            
            # Display metrics in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Métricas de Classificação")
                st.metric(
                    label="Índice de Gini",
                    value=f"{gini:.3f}",
                    help="Medida de pureza da classificação"
                )
                st.metric(
                    label="Entropia",
                    value=f"{entropy:.3f} bits",
                    help="Medida de incerteza na decisão"
                )
            
            with col2:
                st.subheader("🌳 Métricas da Árvore")
                st.metric(
                    label="Profundidade da Árvore",
                    value=f"{depth:.1f}",
                    help="Número médio de decisões necessárias"
                )
                st.metric(
                    label="Taxa de Poda",
                    value=f"{pruning_metrics['pruning_ratio']:.2%}",
                    help="Proporção de nós removidos"
                )
            
            # Pruning Metrics Details
            with st.expander("🔍 Detalhes das Métricas de Poda"):
                st.markdown(f"""
                ### Métricas de Poda Detalhadas
                
                1. **Taxa de Poda:** {pruning_metrics['pruning_ratio']:.2%}
                   - Proporção de nós removidos do modelo
                
                2. **Eficiência da Poda:** {pruning_metrics['eficiencia_poda']:.2%}
                   - Medida de quão eficiente foi o processo de poda
                
                3. **Impacto na Complexidade:** {pruning_metrics['impacto_complexidade']:.3f}
                   - Redução logarítmica na complexidade do modelo
                """)
            
            # Characteristic Weights Visualization
            st.subheader("⚖️ Pesos das Características")
            weights = {
                "security": 0.4,
                "scalability": 0.25,
                "energy_efficiency": 0.20,
                "governance": 0.15
            }
            
            characteristic_weights = {}
            for char in weights.keys():
                weight_metrics = calcular_peso_caracteristica(char, weights, answers)
                characteristic_weights[char] = weight_metrics
            
            # Create radar chart for characteristic weights
            fig = go.Figure()
            
            # Prepare data for radar chart
            chars = list(characteristic_weights.keys())
            values = [characteristic_weights[char]['peso_ajustado'] for char in chars]
            values.append(values[0])  # Close the polygon
            chars.append(chars[0])  # Close the polygon
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=chars,
                fill='toself',
                name='Pesos Ajustados'
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=True,
                title="Distribuição dos Pesos das Características"
            )
            
            st.plotly_chart(fig)
            
            # Display evaluation matrices
            create_evaluation_matrices(rec)

def run_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")

    st.warning("⚠️ Atenção: Reiniciar o processo irá apagar todas as respostas já fornecidas!")
    if st.button("🔄 Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

    st.markdown("---")
    
    questions = [
        {
            "id": "privacy",
            "phase": "Aplicação",
            "characteristic": "Privacidade",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere requisitos de LGPD e HIPAA"
        },
        {
            "id": "integration",
            "phase": "Aplicação",
            "characteristic": "Integração",
            "text": "É necessária integração com outros sistemas de saúde?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere interoperabilidade com sistemas existentes"
        },
        {
            "id": "data_volume",
            "phase": "Infraestrutura",
            "characteristic": "Volume de Dados",
            "text": "O sistema precisa lidar com grandes volumes de registros?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere o volume de transações esperado"
        },
        {
            "id": "energy_efficiency",
            "phase": "Infraestrutura",
            "characteristic": "Eficiência Energética",
            "text": "A eficiência energética é uma preocupação importante?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere o consumo de energia do sistema"
        },
        {
            "id": "network_security",
            "phase": "Consenso",
            "characteristic": "Segurança",
            "text": "É necessário alto nível de segurança na rede?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere requisitos de segurança"
        },
        {
            "id": "scalability",
            "phase": "Consenso",
            "characteristic": "Escalabilidade",
            "text": "A escalabilidade é uma característica chave?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere necessidades futuras de crescimento"
        },
        {
            "id": "governance_flexibility",
            "phase": "Internet",
            "characteristic": "Governança",
            "text": "A governança do sistema precisa ser flexível?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere necessidades de adaptação"
        },
        {
            "id": "interoperability",
            "phase": "Internet",
            "characteristic": "Interoperabilidade",
            "text": "A interoperabilidade com outros sistemas é importante?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere integração com outras redes"
        }
    ]

    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    progress = len(st.session_state.answers) / len(questions)
    
    progress_fig = create_progress_animation(current_phase, st.session_state.answers, questions)
    st.plotly_chart(progress_fig, use_container_width=True)
    
    st.markdown(f"### Fase Atual: {current_phase}")
    st.progress(progress)

    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    if current_question:
        st.subheader(f"Característica: {current_question['characteristic']}")
        st.info(f"Dica: {current_question['tooltip']}")
        response = st.radio(
            current_question["text"],
            current_question["options"]
        )

        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question["id"]] = response
            st.experimental_rerun()

    if len(st.session_state.answers) == len(questions):
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        st.session_state.recommendation = get_recommendation(st.session_state.answers, weights)
        
        if st.session_state.recommendation["confidence"]:
            show_metrics()