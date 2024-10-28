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

def show_characteristic_analysis(analysis):
    """Display detailed analysis of characteristics"""
    if not analysis:
        st.warning("Análise de características não disponível")
        return

    # Create radar chart for characteristics
    characteristics = list(analysis.keys())
    values = list(analysis.values())

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=characteristics,
        fill='toself',
        name='Características'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values)]
            )
        ),
        showlegend=True,
        title="Análise de Características"
    )
    st.plotly_chart(fig)

def show_detailed_recommendation(recommendation):
    """Display detailed recommendation with multiple tabs"""
    st.header("Recomendação Final")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Grupo de Algoritmos")
        st.info(recommendation['consensus_group'])
        st.markdown("### DLT Recomendada")
        st.info(recommendation['dlt'])
        st.markdown("### Algoritmo de Consenso")
        st.info(recommendation['consensus'])
    
    with col2:
        st.subheader("Características Priorizadas")
        for char, score in recommendation.get('characteristic_scores', {}).items():
            st.metric(char, f"{score:.2f}")
    
    # Show evaluation matrix
    if 'evaluation_matrix' in recommendation:
        st.subheader("Matriz de Avaliação")
        matrix_df = pd.DataFrame.from_dict(
            {k: v['metrics'] for k, v in recommendation['evaluation_matrix'].items()},
            orient='index'
        )
        st.dataframe(
            matrix_df.style.background_gradient(cmap='RdYlGn', axis=None),
            use_container_width=True
        )
    
    # Show confidence and validation
    confidence = recommendation.get('confidence_value', 0)
    st.metric("Índice de Confiança", f"{confidence:.1%}")
    
    if confidence > 0.7:
        st.success("Alta confiabilidade na recomendação")
    else:
        st.warning("Confiabilidade moderada - considere revisar os requisitos")
    
    # Show academic validation if available
    if 'academic_validation' in recommendation:
        st.subheader("Validação Acadêmica")
        validation = recommendation['academic_validation']
        st.write(f"**Score**: {validation.get('score', 0.0)}/5.0")
        st.write(f"**Referência**: {validation.get('reference', '')}")
        st.write(f"**Validação**: {validation.get('validation', '')}")

def run_decision_tree():
    """Main function to run the decision tree interface"""
    st.title("Framework de Seleção de DLT")
    
    # Initialize session state
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = "Aplicação"
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    try:
        # Show current phase and progress
        st.subheader(f"Fase Atual: {st.session_state.current_phase}")
        current_step = len(st.session_state.answers) + 1
        
        # Create progress visualization
        phases = ["Aplicação", "Consenso", "Infraestrutura", "Internet"]
        progress = phases.index(st.session_state.current_phase) / len(phases)
        st.progress(progress)
        
        # Get current question
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
            
            if st.button("Próxima Pergunta"):
                # Store response
                st.session_state.answers[current_question['id']] = {
                    'response': response,
                    'phase': st.session_state.current_phase,
                    'characteristics': current_question['characteristics']
                }
                
                # Update characteristic scores
                update_characteristic_scores(response, current_question['characteristics'])
                
                # Move to next phase if needed
                if len(st.session_state.answers) % 2 == 0:
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
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Ver Métricas Detalhadas"):
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
