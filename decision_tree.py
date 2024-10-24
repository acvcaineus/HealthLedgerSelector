import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation

def show_interactive_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    st.title("Framework de Seleção de DLT")
    
    questions = [
        {
            "id": "privacy",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"]
        },
        {
            "id": "integration",
            "text": "É necessária integração com outros sistemas de saúde?",
            "options": ["Sim", "Não"]
        },
        {
            "id": "data_volume",
            "text": "O sistema precisa lidar com grandes volumes de registros médicos?",
            "options": ["Sim", "Não"]
        },
        {
            "id": "energy_efficiency",
            "text": "A eficiência energética é uma preocupação importante?",
            "options": ["Sim", "Não"]
        }
    ]
    
    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break
    
    if current_question:
        st.subheader(f"Pergunta {len(st.session_state.answers) + 1} de {len(questions)}")
        response = st.radio(current_question["text"], current_question["options"])
        
        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question["id"]] = response
            st.experimental_rerun()
    
    if len(st.session_state.answers) == len(questions):
        weights = {
            "security": 0.4,
            "scalability": 0.25,
            "energy_efficiency": 0.20,
            "governance": 0.15
        }
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights)

def show_recommendation(answers, weights):
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação")
    st.write(f"**DLT Recomendada:** {recommendation['dlt']}")
    st.write(f"**Grupo de Consenso:** {recommendation['consensus_group']}")
    st.write(f"**Algoritmo de Consenso:** {recommendation['consensus']}")
    
    # Show evaluation matrix
    st.subheader("Matriz de Avaliação")
    if 'evaluation_matrix' in recommendation:
        for dlt, data in recommendation['evaluation_matrix'].items():
            with st.expander(f"Ver detalhes para {dlt}"):
                for metric, value in data['metrics'].items():
                    st.write(f"{metric}: {float(value):.2f}")
    
    # Show algorithm scores
    st.subheader("Pontuações dos Algoritmos de Consenso")
    if 'algorithms' in recommendation:
        consensus_scores = {}
        for alg in recommendation['algorithms']:
            if alg in consensus_algorithms:
                total_score = 0.0
                for metric, value in consensus_algorithms[alg].items():
                    try:
                        metric_weight = float(weights.get(metric, 0.25))
                        total_score += float(value) * metric_weight
                    except (ValueError, TypeError):
                        continue
                consensus_scores[alg] = float(total_score)
        
        if consensus_scores:
            fig = go.Figure(data=[
                go.Bar(
                    x=list(consensus_scores.keys()),
                    y=[float(score) for score in consensus_scores.values()]
                )
            ])
            fig.update_layout(
                title="Pontuação dos Algoritmos de Consenso",
                xaxis_title="Algoritmos",
                yaxis_title="Pontuação"
            )
            st.plotly_chart(fig)
    
    return recommendation

def restart_decision_tree():
    if st.button("Reiniciar"):
        st.session_state.answers = {}
        st.experimental_rerun()

def run_decision_tree():
    show_interactive_decision_tree()
    st.markdown("---")
    restart_decision_tree()
