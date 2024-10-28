import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from decision_logic import get_recommendation, compare_algorithms, consensus_algorithms, reference_data

def get_phase_questions(phase):
    """Get questions for the current phase"""
    questions = {
        1: [  # Application Phase
            {
                "id": "privacy",
                "text": "A privacidade dos dados do paciente é crítica?",
                "tooltip": "Considere requisitos de LGPD e HIPAA"
            },
            {
                "id": "integration",
                "text": "É necessária integração com outros sistemas de saúde?",
                "tooltip": "Considere interoperabilidade com sistemas existentes"
            }
        ],
        2: [  # Consensus Phase
            {
                "id": "network_security",
                "text": "É necessário alto nível de segurança na rede?",
                "tooltip": "Considere requisitos de segurança"
            },
            {
                "id": "scalability",
                "text": "A escalabilidade é uma característica chave?",
                "tooltip": "Considere necessidades futuras de crescimento"
            }
        ],
        3: [  # Infrastructure Phase
            {
                "id": "data_volume",
                "text": "O sistema precisa lidar com grandes volumes de registros?",
                "tooltip": "Considere o volume de transações esperado"
            },
            {
                "id": "energy_efficiency",
                "text": "A eficiência energética é uma preocupação importante?",
                "tooltip": "Considere o consumo de energia do sistema"
            }
        ],
        4: [  # Internet Phase
            {
                "id": "governance_flexibility",
                "text": "A governança do sistema precisa ser flexível?",
                "tooltip": "Considere necessidades de adaptação"
            },
            {
                "id": "interoperability",
                "text": "A interoperabilidade com outros sistemas é importante?",
                "tooltip": "Considere integração com outras redes"
            }
        ]
    }
    return questions.get(phase, [])

def show_phase_progress(current_phase):
    """Display progress bar and phase information"""
    progress = current_phase / 4
    st.progress(progress, text=f"Fase {current_phase} de 4")
    
    phases = {
        1: "📝 Aplicação",
        2: "🔒 Consenso",
        3: "🏗️ Infraestrutura",
        4: "🌐 Internet"
    }
    
    st.markdown(f"### Fase Atual: {phases.get(current_phase, 'Completo')}")

def run_decision_tree():
    """Main function for the decision tree"""
    if not st.session_state.questionnaire_started:
        st.warning("Por favor, inicie o questionário na página inicial.")
        return
        
    st.title("Framework de Seleção de DLT")
    
    # Show current phase progress
    show_phase_progress(st.session_state.current_phase)
    
    # Get questions for current phase
    current_questions = get_phase_questions(st.session_state.current_phase)
    
    if current_questions:
        # Display questions for current phase
        for question in current_questions:
            with st.expander(f"ℹ️ Questão", expanded=True):
                st.info(f"💡 Dica: {question['tooltip']}")
                response = st.radio(
                    question["text"],
                    ["Sim", "Não"],
                    key=f"question_{question['id']}"
                )
                st.session_state.answers[question['id']] = response
        
        # Navigation buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.session_state.current_phase > 1:
                if st.button("⬅️ Fase Anterior"):
                    st.session_state.current_phase -= 1
                    st.experimental_rerun()
        
        with col2:
            if st.session_state.current_phase < 4:
                if st.button("Próxima Fase ➡️"):
                    st.session_state.current_phase += 1
                    st.experimental_rerun()
            else:
                if st.button("Finalizar Questionário"):
                    weights = {
                        "security": 0.4,
                        "scalability": 0.25,
                        "energy_efficiency": 0.20,
                        "governance": 0.15
                    }
                    recommendation = get_recommendation(st.session_state.answers, weights)
                    st.session_state.recommendation = recommendation
                    st.session_state.page = 'Métricas'
                    st.experimental_rerun()
    
    # Show current answers debug
    if st.session_state.answers:
        with st.expander("📝 Respostas Atuais", expanded=False):
            st.json(st.session_state.answers)
