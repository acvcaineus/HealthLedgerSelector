import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def create_tree_visualization(answers, current_phase):
    """Create a visual representation of the decision tree progress"""
    fig = go.Figure()
    
    phases = ["Aplicação", "Consenso", "Infraestrutura", "Internet"]
    colors = {
        "Aplicação": "#1f77b4",
        "Consenso": "#ff7f0e",
        "Infraestrutura": "#2ca02c",
        "Internet": "#d62728"
    }
    
    # Add nodes for each phase
    for i, phase in enumerate(phases):
        fig.add_trace(go.Scatter(
            x=[i], y=[0],
            mode='markers+text',
            name=phase,
            text=[phase],
            textposition="bottom center",
            marker=dict(size=30, color=colors[phase] if phase == current_phase else 'lightgray'),
            showlegend=False
        ))
    
    # Add connecting lines
    fig.add_trace(go.Scatter(
        x=list(range(len(phases))),
        y=[0] * len(phases),
        mode='lines',
        line=dict(color='gray', dash='dash'),
        showlegend=False
    ))
    
    fig.update_layout(
        title="Progresso da Seleção de DLT",
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False),
        height=200
    )
    
    return fig

def show_recommendation(answers, weights, questions):
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação Final")
    
    # Create tabs for different sections of the recommendation
    tab1, tab2, tab3 = st.tabs(["Recomendação", "Análise Detalhada", "Métricas"])
    
    with tab1:
        st.subheader("DLT Recomendada")
        st.info(f"**{recommendation['dlt']}**")
        st.write(recommendation.get('dlt_explanation', ''))
        
        st.subheader("Algoritmo de Consenso Recomendado")
        st.info(f"**{recommendation['consensus']}**")
        st.write(recommendation.get('consensus_explanation', ''))
        
        # Add confidence indicator
        confidence = recommendation.get('confidence_value', 0)
        st.metric("Índice de Confiança", f"{confidence:.1%}")
    
    with tab2:
        st.subheader("Matriz de Avaliação")
        if 'evaluation_matrix' in recommendation:
            df = pd.DataFrame.from_dict(
                {k: v['metrics'] for k, v in recommendation['evaluation_matrix'].items()},
                orient='index'
            )
            st.dataframe(df)
            
            # Create radar chart
            fig = go.Figure()
            for dlt, data in recommendation['evaluation_matrix'].items():
                fig.add_trace(go.Scatterpolar(
                    r=[float(v) for v in data['metrics'].values()],
                    theta=list(data['metrics'].keys()),
                    fill='toself',
                    name=dlt
                ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=True,
                title="Comparação de Características"
            )
            st.plotly_chart(fig)
    
    with tab3:
        st.subheader("Métricas de Decisão")
        col1, col2 = st.columns(2)
        
        with col1:
            # Calculate and display metrics
            depth = len(answers)
            pruning = calcular_pruning(depth * 2 + 1, depth + 1)
            st.metric("Profundidade da Árvore", depth)
            st.metric("Taxa de Poda", f"{pruning:.1%}")
        
        with col2:
            # Display academic validation if available
            if 'academic_validation' in recommendation:
                st.metric("Validação Acadêmica", 
                         f"{recommendation['academic_validation'].get('score', 0):.1f}/5.0")
                st.write(f"Referência: {recommendation['academic_validation'].get('reference', '')}")
    
    # Save recommendation to database
    if 'username' in st.session_state:
        save_recommendation(st.session_state.username, "Healthcare", recommendation)
    
    # Add navigation buttons
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
    st.title("Framework de Seleção de DLT")
    
    # Initialize session state if needed
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    # Define phases and questions
    phases = {
        1: "Aplicação",
        2: "Consenso", 
        3: "Infraestrutura",
        4: "Internet"
    }
    
    questions = [
        {
            "phase": "Aplicação",
            "id": "privacy",
            "text": "A privacidade dos dados do paciente é crítica?",
            "characteristic": "Privacidade"
        },
        {
            "phase": "Aplicação",
            "id": "integration",
            "text": "É necessária integração com outros sistemas de saúde?",
            "characteristic": "Integração"
        },
        {
            "phase": "Consenso",
            "id": "data_volume",
            "text": "O sistema precisa lidar com grandes volumes de registros?",
            "characteristic": "Volume de Dados"
        },
        {
            "phase": "Consenso",
            "id": "energy_efficiency",
            "text": "A eficiência energética é uma preocupação importante?",
            "characteristic": "Eficiência Energética"
        },
        {
            "phase": "Infraestrutura",
            "id": "network_security",
            "text": "A segurança da rede é uma prioridade alta?",
            "characteristic": "Segurança"
        },
        {
            "phase": "Infraestrutura",
            "id": "scalability",
            "text": "A escalabilidade é uma característica chave?",
            "characteristic": "Escalabilidade"
        },
        {
            "phase": "Internet",
            "id": "governance_flexibility",
            "text": "A governança do sistema precisa ser flexível?",
            "characteristic": "Governança"
        },
        {
            "phase": "Internet",
            "id": "interoperability",
            "text": "A interoperabilidade com outros sistemas é importante?",
            "characteristic": "Interoperabilidade"
        }
    ]
    
    # Show progress
    current_step = len(st.session_state.answers) + 1
    if current_step <= len(questions):
        current_question = questions[current_step - 1]
        current_phase = current_question["phase"]
        
        # Show tree visualization
        st.plotly_chart(create_tree_visualization(st.session_state.answers, current_phase))
        
        # Show progress bar
        progress = current_step / len(questions)
        st.progress(progress)
        
        # Show current phase and characteristic
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Fase Atual:** {current_phase}")
        with col2:
            st.markdown(f"**Característica:** {current_question['characteristic']}")
        
        # Show question
        answer = st.radio(
            current_question["text"],
            ["Sim", "Não"],
            key=f"question_{current_step}"
        )
        
        # Show explanation based on the phase
        phase_explanations = {
            "Aplicação": "Esta fase avalia requisitos fundamentais relacionados à privacidade e integração dos dados.",
            "Consenso": "Nesta fase, consideramos aspectos de processamento e eficiência do sistema.",
            "Infraestrutura": "Avaliamos requisitos técnicos de segurança e escalabilidade.",
            "Internet": "Por fim, analisamos aspectos de governança e interoperabilidade."
        }
        st.info(phase_explanations[current_phase])
        
        # Handle next button
        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question["id"]] = answer
            st.experimental_rerun()
    
    # Show recommendation when all questions are answered
    if len(st.session_state.answers) == len(questions):
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights, questions)
        
    # Show restart button
    if len(st.session_state.answers) > 0:
        if st.button("Reiniciar"):
            st.session_state.answers = {}
            st.experimental_rerun()

def restart_decision_tree():
    st.session_state.answers = {}
    st.session_state.step = 1
    st.experimental_rerun()
