import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation

def get_questions():
    return [
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

def show_recommendation(answers, weights):
    recommendation = get_recommendation(answers, weights)
    
    # Show decision path
    st.header("Seu Caminho de Decisão")
    phases = {
        "Aplicação": ["privacy", "integration"],
        "Consenso": ["network_security", "scalability"],
        "Infraestrutura": ["data_volume", "energy_efficiency"],
        "Internet": ["governance_flexibility", "interoperability"]
    }

    # Visual decision path with phase colors
    for phase, questions in phases.items():
        phase_color = {
            "Aplicação": "#2ecc71",
            "Consenso": "#3498db",
            "Infraestrutura": "#e74c3c",
            "Internet": "#f1c40f"
        }.get(phase, "#95a5a6")

        with st.expander(f"📋 Fase: {phase}", expanded=True):
            st.markdown(f"""
                <div style='background-color: {phase_color}; padding: 10px; border-radius: 5px; color: white;'>
                    <h4>{phase}</h4>
                </div>
            """, unsafe_allow_html=True)
            
            answered = sum(1 for q in questions if q in answers)
            total = len(questions)
            st.progress(answered / total)
            
            for q_id in questions:
                if q_id in answers:
                    question_text = next((q["text"] for q in get_questions() if q["id"] == q_id), q_id)
                    st.markdown(f"❓ **Pergunta:** {question_text}")
                    st.markdown(f"✅ **Sua resposta:** {answers[q_id]}")
                    st.markdown("---")

    # Show final recommendation
    st.header("Recomendação Final")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3 style='color: #1f77b4;'>{recommendation['dlt']}</h3>
            <p><strong>Grupo de Consenso:</strong> {recommendation['consensus_group']}</p>
            <p><strong>Algoritmo:</strong> {recommendation['consensus']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        confidence_score = recommendation.get('confidence', False)
        st.metric(
            label="Índice de Confiança",
            value=f"{'Alto' if confidence_score else 'Médio'}",
            delta=f"{'↑' if confidence_score else '→'}",
            help="Baseado na diferença entre o score máximo e a média dos scores"
        )

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

def show_metrics():
    st.header("Métricas de Avaliação")
    if 'recommendation' in st.session_state:
        rec = st.session_state.recommendation
        if 'evaluation_matrix' in rec:
            for dlt, data in rec['evaluation_matrix'].items():
                with st.expander(f"📊 {dlt}", expanded=True):
                    for metric, value in data['metrics'].items():
                        st.metric(
                            label=metric.title(),
                            value=f"{value:.2f}",
                            delta=f"{'↑' if value > 3 else '↓'}"
                        )

def show_interactive_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")
    questions = get_questions()
    
    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    progress = len(st.session_state.answers) / len(questions)
    
    # Phase progress visualization
    phase_colors = {
        "Aplicação": "#2ecc71",
        "Consenso": "#3498db",
        "Infraestrutura": "#e74c3c",
        "Internet": "#f1c40f"
    }
    
    st.markdown(f"""
        <div style='background-color: {phase_colors.get(current_phase, "#95a5a6")}; 
             padding: 10px; border-radius: 5px; color: white;'>
            <h3>Fase Atual: {current_phase}</h3>
            <p>Progresso: {int(progress * 100)}%</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.progress(progress)

    current_question = next((q for q in questions if q["id"] not in st.session_state.answers), None)

    if current_question:
        with st.expander("💡 Detalhes da Característica", expanded=True):
            st.subheader(f"Avaliando: {current_question['characteristic']}")
            st.markdown(f"**Fase:** {current_question['phase']}")
            st.markdown(f"**Descrição:** {current_question['tooltip']}")
        
        response = st.radio(
            current_question["text"],
            current_question["options"],
            help=current_question["tooltip"]
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
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights)
        show_metrics()

def restart_decision_tree():
    if st.button("Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

def run_decision_tree():
    show_interactive_decision_tree()
    st.markdown("---")
    restart_decision_tree()
