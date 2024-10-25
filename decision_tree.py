import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation

def get_questions():
    return [
        {
            "id": "privacy",
            "characteristic": "Privacidade",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere requisitos de LGPD e HIPAA"
        },
        {
            "id": "integration",
            "characteristic": "Integração",
            "text": "É necessária integração com outros sistemas de saúde?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere interoperabilidade com sistemas existentes"
        },
        {
            "id": "data_volume",
            "characteristic": "Volume de Dados",
            "text": "O sistema precisa lidar com grandes volumes de registros?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere o volume de transações esperado"
        },
        {
            "id": "energy_efficiency",
            "characteristic": "Eficiência Energética",
            "text": "A eficiência energética é uma preocupação importante?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere o consumo de energia do sistema"
        },
        {
            "id": "network_security",
            "characteristic": "Segurança",
            "text": "É necessário alto nível de segurança na rede?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere requisitos de segurança"
        },
        {
            "id": "scalability",
            "characteristic": "Escalabilidade",
            "text": "A escalabilidade é uma característica chave?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere necessidades futuras de crescimento"
        },
        {
            "id": "governance_flexibility",
            "characteristic": "Governança",
            "text": "A governança do sistema precisa ser flexível?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere necessidades de adaptação"
        },
        {
            "id": "interoperability",
            "characteristic": "Interoperabilidade",
            "text": "A interoperabilidade com outros sistemas é importante?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere integração com outras redes"
        }
    ]

def show_recommendation(answers, weights):
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação")
    
    # Display recommendation and confidence side by side
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(f"**DLT Recomendada:** {recommendation['dlt']}")
        st.write(f"**Grupo de Consenso:** {recommendation['consensus_group']}")
        st.write(f"**Algoritmo de Consenso:** {recommendation['consensus']}")
    
    with col2:
        confidence_score = recommendation.get('confidence', False)
        st.metric(
            label="Índice de Confiança",
            value="Alto" if confidence_score else "Médio",
            delta="↑" if confidence_score else "→"
        )
    
    # Display academic validation if available
    if 'academic_validation' in recommendation and recommendation['academic_validation']:
        st.markdown("### Validação Acadêmica")
        validation = recommendation['academic_validation']
        st.write(f"**Score Acadêmico:** {validation.get('score', 'N/A')}")
        st.write(f"**Citações:** {validation.get('citations', 'N/A')}")
        st.write(f"**Referência:** {validation.get('reference', 'N/A')}")
        st.write(f"**Validação:** {validation.get('validation', 'N/A')}")

    # Save recommendation button
    if st.button("Salvar Recomendação"):
        if st.session_state.get('username'):
            save_recommendation(
                st.session_state.username,
                'Healthcare DLT Selection',
                recommendation
            )
            st.success("Recomendação salva com sucesso!")
        else:
            st.warning("Faça login para salvar a recomendação.")

    return recommendation

def show_interactive_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    st.title("Framework de Seleção de DLT")
    
    # Show progress visualization with diamonds
    questions = get_questions()
    current_phase = len(st.session_state.answers) + 1
    
    # Show interactive progress
    total_questions = len(questions)
    answered_questions = len(st.session_state.answers)
    
    st.progress(answered_questions / total_questions)
    st.markdown(f"**Progresso:** {answered_questions}/{total_questions} perguntas respondidas")
    
    # Create visual flow with diamond shapes
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### Fase {current_phase} de {len(questions)}")
    
    current_question = next((q for q in questions if q["id"] not in st.session_state.answers), None)
    
    if current_question:
        # Show diamond shape question box
        st.markdown(f'''
        <div style="border: 2px solid #1f77b4; padding: 20px; border-radius: 10px; margin: 10px 0;">
            <p style="color: #1f77b4; font-weight: bold;">{current_question["text"]}</p>
            <p style="color: #666; font-size: 0.9em;">{current_question["tooltip"]}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        response = st.radio("", current_question["options"])
        
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
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights)

def restart_decision_tree():
    if st.button("Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

def run_decision_tree():
    show_interactive_decision_tree()
    st.markdown("---")
    restart_decision_tree()
