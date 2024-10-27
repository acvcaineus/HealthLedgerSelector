import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from decision_logic import get_recommendation, compare_algorithms, consensus_algorithms, reference_data
from database import save_recommendation
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def show_phase_progress(current_phase, total_phases=4):
    """Display progress bar and phase information"""
    progress = current_phase / total_phases
    st.progress(progress, text=f"Fase {current_phase} de {total_phases}")
    
    phases = {
        1: "📝 Aplicação",
        2: "🔒 Consenso",
        3: "🏗️ Infraestrutura",
        4: "🌐 Internet"
    }
    
    st.markdown(f"### Fase Atual: {phases.get(current_phase, 'Completo')}")

def get_phase_questions(phase):
    """Get questions for the current phase"""
    questions = {
        1: [  # Application Phase
            {
                "id": "privacy",
                "characteristic": "Privacidade",
                "text": "A privacidade dos dados do paciente é crítica?",
                "tooltip": "Considere requisitos de LGPD e HIPAA"
            },
            {
                "id": "integration",
                "characteristic": "Integração",
                "text": "É necessária integração com outros sistemas de saúde?",
                "tooltip": "Considere interoperabilidade com sistemas existentes"
            }
        ],
        2: [  # Consensus Phase
            {
                "id": "network_security",
                "characteristic": "Segurança",
                "text": "É necessário alto nível de segurança na rede?",
                "tooltip": "Considere requisitos de segurança"
            },
            {
                "id": "scalability",
                "characteristic": "Escalabilidade",
                "text": "A escalabilidade é uma característica chave?",
                "tooltip": "Considere necessidades futuras de crescimento"
            }
        ],
        3: [  # Infrastructure Phase
            {
                "id": "data_volume",
                "characteristic": "Volume de Dados",
                "text": "O sistema precisa lidar com grandes volumes de registros?",
                "tooltip": "Considere o volume de transações esperado"
            },
            {
                "id": "energy_efficiency",
                "characteristic": "Eficiência Energética",
                "text": "A eficiência energética é uma preocupação importante?",
                "tooltip": "Considere o consumo de energia do sistema"
            }
        ],
        4: [  # Internet Phase
            {
                "id": "governance_flexibility",
                "characteristic": "Governança",
                "text": "A governança do sistema precisa ser flexível?",
                "tooltip": "Considere necessidades de adaptação"
            },
            {
                "id": "interoperability",
                "characteristic": "Interoperabilidade",
                "text": "A interoperabilidade com outros sistemas é importante?",
                "tooltip": "Considere integração com outras redes"
            }
        ]
    }
    return questions.get(phase, [])

def run_decision_tree():
    """Main function for the decision tree with improved navigation and state management"""
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 1

    st.title("Framework de Seleção de DLT")
    
    # Show framework phases explanation
    st.markdown("""
        ### Fases do Processo de Seleção
        O processo está dividido em 4 fases principais:
        1. **Aplicação**: Avaliação de requisitos de privacidade e integração
        2. **Consenso**: Análise de segurança e eficiência
        3. **Infraestrutura**: Avaliação de escalabilidade e performance
        4. **Internet**: Considerações sobre governança e interoperabilidade
    """)

    # Show current phase progress
    show_phase_progress(st.session_state.current_phase)

    # Get questions for current phase
    current_phase_questions = get_phase_questions(st.session_state.current_phase)
    
    if current_phase_questions:
        # Display questions for current phase
        for question in current_phase_questions:
            if question["id"] not in st.session_state.answers:
                with st.expander(f"ℹ️ {question['characteristic']}", expanded=True):
                    st.info(f"💡 Dica: {question['tooltip']}")
                    response = st.radio(
                        question["text"],
                        ["Sim", "Não"],
                        key=f"question_{question['id']}"
                    )
                    
                    # Navigation buttons
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.session_state.current_phase > 1:
                            if st.button("⬅️ Fase Anterior"):
                                st.session_state.current_phase -= 1
                                st.experimental_rerun()
                    
                    with col2:
                        if st.button("Próxima Pergunta ➡️", type="primary"):
                            st.session_state.answers[question["id"]] = response
                            # Check if all questions in current phase are answered
                            phase_complete = all(q["id"] in st.session_state.answers 
                                              for q in current_phase_questions)
                            if phase_complete and st.session_state.current_phase < 4:
                                st.session_state.current_phase += 1
                            st.experimental_rerun()
                break  # Show only one unanswered question at a time
    
    # Check if all questions are answered
    all_questions = []
    for phase in range(1, 5):
        all_questions.extend(get_phase_questions(phase))
    
    if len(st.session_state.answers) == len(all_questions):
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        
        # Show recommendation
        recommendation = get_recommendation(st.session_state.answers, weights)
        st.session_state.recommendation = recommendation
        
        # Display recommendation summary
        st.success("✅ Questionário completo! Gerando recomendação...")
        
        # Allow user to review or modify answers
        if st.button("📝 Revisar Respostas"):
            st.session_state.current_phase = 1
            st.experimental_rerun()
        
        # Navigate to metrics page
        if st.button("📊 Ver Métricas Detalhadas"):
            st.session_state.page = 'Métricas'
            st.experimental_rerun()

        # Display recommendation details
        show_recommendation(st.session_state.answers, weights, all_questions)

def show_recommendation(answers, weights, questions):
    """Display recommendation with enhanced visualization"""
    recommendation = get_recommendation(answers, weights)
    
    with st.spinner('Carregando recomendação...'):
        st.header("Recomendação Final")
        
        # Main recommendation display with improved styling
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("DLT Recomendada")
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
                <h3 style='color: #1f77b4;'>{recommendation['dlt']}</h3>
                <p><strong>Grupo de Consenso:</strong> {recommendation['consensus_group']}</p>
                <p><strong>Algoritmo:</strong> {recommendation['consensus']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show explanation with improved styling
            with st.expander("🔍 Ver Explicação Detalhada"):
                st.write(f"### Por que {recommendation['dlt']}?")
                st.write("\n### Características Principais:")
                st.markdown(recommendation['characteristics'])
                st.write("\n### Casos de Uso:")
                st.markdown(recommendation['use_cases'])
        
        with col2:
            # Show confidence metrics
            st.subheader("Índices de Confiança")
            confidence_value = recommendation.get('confidence_value', 0.0)
            st.metric(
                label="Confiança da Recomendação",
                value=f"{confidence_value:.2%}",
                delta=f"{'Alta' if confidence_value > 0.7 else 'Média'}",
                help="Baseado na análise das respostas e métricas"
            )
        
        # Save recommendation button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💾 Salvar Recomendação", type="primary"):
                if st.session_state.get('username'):
                    save_recommendation(
                        st.session_state.username,
                        'Healthcare DLT Selection',
                        recommendation
                    )
                    st.success("✅ Recomendação salva com sucesso!")
                else:
                    st.warning("⚠️ Faça login para salvar a recomendação.")
    
    return recommendation
