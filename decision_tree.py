import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def get_question_for_phase(phase):
    """Get appropriate question for the current phase"""
    questions_by_phase = {
        "Aplicação": [
            {
                "id": "privacy",
                "text": "A privacidade dos dados do paciente é crítica?",
                "explanation": "Esta questão avalia a necessidade de controle sobre dados sensíveis",
                "characteristics": ["security", "privacy"],
                "impact": "Influencia a escolha do grupo de algoritmos de Alta Segurança e Controle"
            },
            {
                "id": "integration",
                "text": "É necessária integração com outros sistemas de saúde?",
                "explanation": "Avalia necessidade de interoperabilidade",
                "characteristics": ["scalability", "interoperability"],
                "impact": "Afeta a escolha entre grupos de Alta Eficiência Operacional ou Escalabilidade"
            }
        ],
        "Consenso": [
            {
                "id": "data_volume",
                "text": "O sistema lida com grandes volumes de dados?",
                "explanation": "Avalia a necessidade de processamento de grandes volumes",
                "characteristics": ["scalability"],
                "impact": "Influencia escolha entre PBFT, PoS ou Tangle"
            },
            {
                "id": "energy_efficiency",
                "text": "A eficiência energética é importante?",
                "explanation": "Avalia impacto do consumo energético",
                "characteristics": ["energy_efficiency"],
                "impact": "Direciona para PoS, PoA ou Tangle vs PoW"
            }
        ],
        "Infraestrutura": [
            {
                "id": "security",
                "text": "A segurança da rede é uma prioridade alta?",
                "explanation": "Avalia requisitos de segurança",
                "characteristics": ["security"],
                "impact": "Prioriza PBFT ou PoW para maior segurança"
            },
            {
                "id": "scalability",
                "text": "A escalabilidade é uma característica chave?",
                "explanation": "Avalia necessidade de crescimento",
                "characteristics": ["scalability"],
                "impact": "Favorece PoS, DPoS ou Tangle"
            }
        ],
        "Internet": [
            {
                "id": "governance",
                "text": "A governança precisa ser flexível?",
                "explanation": "Avalia necessidade de controle administrativo",
                "characteristics": ["governance"],
                "impact": "Direciona para DPoS ou PoA"
            },
            {
                "id": "interoperability",
                "text": "A interoperabilidade é importante?",
                "explanation": "Avalia comunicação entre sistemas",
                "characteristics": ["interoperability"],
                "impact": "Favorece soluções híbridas ou PoA"
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
            if char in ["security", "privacy"]:
                st.session_state.characteristic_scores[char] += 2.0  # Higher weight for security
            else:
                st.session_state.characteristic_scores[char] += 1.0

def show_detailed_recommendation(recommendation):
    """Display detailed recommendation with enhanced metrics"""
    st.header("Recomendação Final")
    
    # Show the selected DLT group and explanation
    st.subheader("Grupo de DLT Selecionado")
    col1, col2 = st.columns(2)
    with col1:
        st.info(recommendation['consensus_group'])
        st.markdown("### DLT Recomendada")
        st.info(recommendation['dlt'])
    with col2:
        st.markdown("### Algoritmo de Consenso")
        st.info(recommendation['consensus'])
        if 'algorithms' in recommendation:
            st.markdown("#### Algoritmos Compatíveis")
            for algo in recommendation['algorithms']:
                st.write(f"- {algo}")
    
    # Show characteristics and metrics
    st.markdown("---")
    st.subheader("Análise de Características")
    
    # Display characteristic scores in a radar chart
    if 'evaluation_matrix' in recommendation and recommendation['dlt'] in recommendation['evaluation_matrix']:
        metrics = recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']
        
        fig = go.Figure(data=go.Scatterpolar(
            r=list(metrics.values()),
            theta=list(metrics.keys()),
            fill='toself',
            name='Características'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title="Análise de Características da DLT"
        )
        st.plotly_chart(fig)
    
    # Show confidence metrics
    st.markdown("---")
    st.subheader("Métricas de Confiança")
    
    conf_col1, conf_col2 = st.columns(2)
    with conf_col1:
        confidence = recommendation.get('confidence_value', 0)
        st.metric("Índice de Confiança", f"{confidence:.1%}")
        
        if confidence > 0.7:
            st.success("Alta confiabilidade na recomendação")
        else:
            st.warning("Confiabilidade moderada - considere revisar os requisitos")
    
    with conf_col2:
        if 'academic_validation' in recommendation:
            validation = recommendation['academic_validation']
            st.metric("Score Acadêmico", f"{validation.get('score', 0)}/5.0")
            st.write(f"**Referência**: {validation.get('reference', '')}")
            st.write(f"**Validação**: {validation.get('validation', '')}")
    
    # Show use cases
    if 'use_cases' in recommendation:
        st.markdown("---")
        st.subheader("Casos de Uso Recomendados")
        st.write(recommendation['use_cases'])

def run_decision_tree():
    """Main function to run the decision tree interface"""
    st.title("Framework de Seleção de DLT")
    
    # Initialize session state
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = "Aplicação"
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'characteristic_scores' not in st.session_state:
        st.session_state.characteristic_scores = {}
    
    try:
        # Show current phase and progress
        st.subheader(f"Fase Atual: {st.session_state.current_phase}")
        progress = len(st.session_state.answers) / 8  # Total of 8 questions
        st.progress(progress)
        
        # Get current question
        current_question = get_question_for_phase(st.session_state.current_phase)
        
        if current_question:
            # Show question with context
            st.markdown(f"### {current_question['text']}")
            st.info(current_question['explanation'])
            
            # Get user response with clear options
            col1, col2 = st.columns(2)
            with col1:
                response = st.radio(
                    "Selecione sua resposta:",
                    ["Sim", "Não"],
                    key=f"question_{len(st.session_state.answers) + 1}"
                )
            
            with col2:
                st.markdown("#### Impacto desta escolha:")
                st.write(current_question['impact'])
            
            # Show progress indicators
            st.markdown("---")
            st.markdown(f"**Fase atual:** {st.session_state.current_phase}")
            st.markdown(f"**Pergunta:** {len(st.session_state.answers) + 1}/8")
            
            if st.button("Próxima Pergunta"):
                # Store response
                st.session_state.answers[current_question['id']] = response
                
                # Update characteristics
                update_characteristic_scores(response, current_question['characteristics'])
                
                # Move to next phase if needed
                if len(st.session_state.answers) % 2 == 0 and len(st.session_state.answers) < 8:
                    phases = ["Aplicação", "Consenso", "Infraestrutura", "Internet"]
                    current_index = phases.index(st.session_state.current_phase)
                    if current_index < len(phases) - 1:
                        st.session_state.current_phase = phases[current_index + 1]
                
                st.experimental_rerun()
        
        # Show recommendation when all questions are answered
        if len(st.session_state.answers) == 8:
            weights = {
                "security": float(0.4),
                "scalability": float(0.25),
                "energy_efficiency": float(0.20),
                "governance": float(0.15)
            }
            
            recommendation = get_recommendation(st.session_state.answers, weights)
            st.session_state.recommendation = recommendation
            show_detailed_recommendation(recommendation)
            
            # Add navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Ver Métricas"):
                    st.session_state.page = "Métricas"
                    st.experimental_rerun()
            with col2:
                if st.button("Reiniciar"):
                    restart_decision_tree()
    
    except Exception as e:
        st.error(f"Erro no processamento: {str(e)}")
        st.info("Por favor, tente reiniciar o processo")
        if st.button("Reiniciar"):
            restart_decision_tree()

def restart_decision_tree():
    """Reset the decision tree state"""
    st.session_state.answers = {}
    st.session_state.current_phase = "Aplicação"
    st.session_state.characteristic_scores = {}
    st.experimental_rerun()
