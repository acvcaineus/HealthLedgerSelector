import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def get_question_for_phase(phase):
    """Get appropriate question for the current phase"""
    questions_by_phase = {
        "Aplicação": [
            {
                "id": "privacy",
                "text": "A privacidade dos dados do paciente é crítica?",
                "explanation": "Avalia a necessidade de controle sobre dados sensíveis de pacientes",
                "characteristics": ["security", "privacy"],
                "impact": "Influencia a escolha de DLTs com maior foco em privacidade e segurança"
            },
            {
                "id": "integration",
                "text": "É necessária integração com outros sistemas de saúde?",
                "explanation": "Avalia a necessidade de interoperabilidade entre sistemas",
                "characteristics": ["scalability", "interoperability"],
                "impact": "Afeta a escolha de DLTs com suporte à integração de sistemas"
            }
        ],
        "Consenso": [
            {
                "id": "data_volume",
                "text": "O sistema precisa lidar com grandes volumes de registros?",
                "explanation": "Avalia a capacidade de processamento necessária",
                "characteristics": ["scalability", "efficiency"],
                "impact": "Determina a escolha de DLTs com alta capacidade de processamento"
            },
            {
                "id": "energy_efficiency",
                "text": "A eficiência energética é uma preocupação importante?",
                "explanation": "Avalia o impacto ambiental e custos operacionais",
                "characteristics": ["energy_efficiency"],
                "impact": "Influencia a seleção de algoritmos de consenso eficientes"
            }
        ],
        "Infraestrutura": [
            {
                "id": "network_security",
                "text": "A segurança da rede é uma prioridade alta?",
                "explanation": "Avalia requisitos de segurança da infraestrutura",
                "characteristics": ["security"],
                "impact": "Afeta a escolha de DLTs com maior foco em segurança"
            },
            {
                "id": "scalability",
                "text": "A escalabilidade é uma característica chave?",
                "explanation": "Avalia o potencial de crescimento do sistema",
                "characteristics": ["scalability"],
                "impact": "Determina a escolha de DLTs mais escaláveis"
            }
        ],
        "Internet": [
            {
                "id": "governance_flexibility",
                "text": "A governança do sistema precisa ser flexível?",
                "explanation": "Avalia necessidades de administração e controle",
                "characteristics": ["governance"],
                "impact": "Influencia a escolha de DLTs com governança flexível"
            },
            {
                "id": "interoperability",
                "text": "A interoperabilidade com outros sistemas é importante?",
                "explanation": "Avalia a capacidade de comunicação entre sistemas",
                "characteristics": ["interoperability"],
                "impact": "Afeta a escolha de DLTs com maior interoperabilidade"
            }
        ]
    }
    return questions_by_phase[phase][len(st.session_state.answers) % 2]

def update_characteristic_scores(response, characteristics):
    """Update scores for characteristics based on user response"""
    if 'characteristic_scores' not in st.session_state:
        st.session_state.characteristic_scores = {}
    
    for char in characteristics:
        if char not in st.session_state.characteristic_scores:
            st.session_state.characteristic_scores[char] = 0.0
        
        if response == "Sim":
            st.session_state.characteristic_scores[char] += 1.0

def show_characteristic_analysis(analysis):
    """Display detailed analysis of characteristics"""
    if not analysis:
        st.warning("Análise de características não disponível")
        return
    
    # Create radar chart for characteristics
    fig = go.Figure()
    
    for characteristic, score in analysis.items():
        fig.add_trace(go.Scatterpolar(
            r=[score],
            theta=[characteristic],
            fill='toself',
            name=characteristic
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        title="Análise de Características"
    )
    st.plotly_chart(fig)
    
    # Show detailed explanation
    st.write("### Detalhamento das Características")
    for char, score in analysis.items():
        st.write(f"**{char}**: {score:.2f}")
        st.info(f"Impacto na decisão: {'Alto' if score > 0.7 else 'Médio' if score > 0.4 else 'Baixo'}")

def show_decision_metrics(metrics):
    """Display decision metrics with explanations"""
    if not metrics:
        st.warning("Métricas não disponíveis")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        for metric, value in metrics.items():
            st.metric(metric, f"{value:.2f}")
    
    with col2:
        st.write("### Interpretação das Métricas")
        for metric, value in metrics.items():
            st.write(f"**{metric}**")
            if value > 0.7:
                st.success("Alta confiabilidade")
            elif value > 0.4:
                st.warning("Confiabilidade moderada")
            else:
                st.error("Baixa confiabilidade")

def show_academic_validation(validation):
    """Display academic validation information"""
    if not validation:
        st.warning("Validação acadêmica não disponível")
        return
    
    st.write("### Referência Acadêmica")
    st.write(f"**Score**: {validation.get('score', 0.0)}/5.0")
    st.write(f"**Referência**: {validation.get('reference', '')}")
    st.write(f"**Validação**: {validation.get('validation', '')}")

def show_detailed_recommendation(recommendation):
    """Display detailed recommendation with multiple tabs"""
    st.header("Recomendação Final")
    
    tabs = st.tabs(["Recomendação", "Análise Detalhada", "Métricas", "Validação Acadêmica"])
    
    with tabs[0]:
        st.subheader("DLT Recomendada")
        st.info(recommendation['dlt'])
        st.markdown("### Justificativa")
        st.write(recommendation.get('justification', 'Baseada nas características e requisitos informados'))
        
        st.subheader("Algoritmo de Consenso")
        st.info(recommendation['consensus'])
        st.markdown("### Grupo de Algoritmos")
        st.write(recommendation['consensus_group'])
    
    with tabs[1]:
        st.subheader("Análise de Características")
        show_characteristic_analysis(recommendation.get('analysis', {}))
    
    with tabs[2]:
        st.subheader("Métricas de Decisão")
        show_decision_metrics(recommendation.get('metrics', {}))
    
    with tabs[3]:
        st.subheader("Validação Acadêmica")
        show_academic_validation(recommendation.get('academic_validation', {}))

def run_decision_tree():
    """Main function to run the decision tree interface"""
    st.title("Framework de Seleção de DLT")
    
    # Initialize session state
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = "Aplicação"
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'characteristics' not in st.session_state:
        st.session_state.characteristics = {}
    
    # Show current phase and progress
    st.subheader(f"Fase Atual: {st.session_state.current_phase}")
    current_step = len(st.session_state.answers) + 1
    
    # Create progress visualization
    phases = ["Aplicação", "Consenso", "Infraestrutura", "Internet"]
    progress = phases.index(st.session_state.current_phase) / len(phases)
    st.progress(progress)
    
    # Get current question based on phase
    current_question = get_question_for_phase(st.session_state.current_phase)
    
    if current_question:
        # Show question with explanation
        st.markdown(f"### {current_question['text']}")
        st.info(current_question['explanation'])
        
        # Get user response
        response = st.radio(
            "Selecione sua resposta:",
            ["Sim", "Não"],
            key=f"question_{current_step}"
        )
        
        # Show characteristic impact
        st.markdown("#### Impacto desta escolha:")
        st.write(current_question['impact'])
        
        # Handle response
        if st.button("Próxima Pergunta"):
            # Store response with metadata
            st.session_state.answers[current_question['id']] = {
                'response': response,
                'phase': st.session_state.current_phase,
                'characteristics': current_question['characteristics']
            }
            
            # Update characteristics scores
            update_characteristic_scores(response, current_question['characteristics'])
            
            # Move to next phase if needed
            if len(st.session_state.answers) % 2 == 0:
                current_index = phases.index(st.session_state.current_phase)
                if current_index < len(phases) - 1:
                    st.session_state.current_phase = phases[current_index + 1]
            
            st.experimental_rerun()
    
    # Show recommendation when all questions are answered
    if len(st.session_state.answers) == 8:  # Total number of questions
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        
        # Get recommendation
        recommendation = get_recommendation(st.session_state.answers, weights)
        
        # Store recommendation for metrics
        st.session_state.recommendation = recommendation
        
        # Show detailed recommendation
        show_detailed_recommendation(recommendation)

def restart_decision_tree():
    """Reset the decision tree state"""
    st.session_state.answers = {}
    st.session_state.current_phase = "Aplicação"
    st.session_state.characteristics = {}
    st.session_state.characteristic_scores = {}
    st.experimental_rerun()
