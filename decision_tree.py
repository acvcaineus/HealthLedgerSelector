import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation

def show_interactive_decision_tree():
    # Iniciar estado de sessão se não existir
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    # Título do app
    st.title("Framework de Seleção de DLT")

    # Definição das perguntas
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

    # Encontrar a próxima pergunta
    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    # Exibir a próxima pergunta
    if current_question:
        st.subheader(f"Pergunta {len(st.session_state.answers) + 1} de {len(questions)}")
        response = st.radio(current_question["text"], current_question["options"])

        # Botão de próxima pergunta
        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question["id"]] = response
            st.experimental_set_query_params()  # Atualizado para forçar a página a recarregar

    # Mostrar recomendação quando todas as perguntas forem respondidas
    if len(st.session_state.answers) == len(questions):
        weights = {
            "security": 0.4,
            "scalability": 0.25,
            "energy_efficiency": 0.20,
            "governance": 0.15
        }
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights)

def show_recommendation(answers, weights):
    # Obter recomendação baseada nas respostas
    recommendation = get_recommendation(answers, weights)

    # Mostrar a recomendação final
    st.header("Recomendação")
    st.write(f"**DLT Recomendada:** {recommendation['dlt']}")
    st.write(f"**Grupo de Consenso:** {recommendation['consensus_group']}")
    st.write(f"**Algoritmo de Consenso:** {recommendation['consensus']}")

    # Mostrar a matriz de avaliação
    st.subheader("Matriz de Avaliação")
    if 'evaluation_matrix' in recommendation:
        for dlt, data in recommendation['evaluation_matrix'].items():
            with st.expander(f"Ver detalhes para {dlt}"):
                for metric, value in data['metrics'].items():
                    st.write(f"{metric}: {float(value):.2f}")

    # Mostrar pontuações dos algoritmos de consenso
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

        # Exibir gráfico de barras das pontuações
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

    # Botão de salvar com estilo pequeno e transparente
    st.markdown("""
        <style>
        .save-button {
            background-color: rgba(255, 75, 75, 0.3);  /* Cor vermelha com transparência */
            color: white;
            font-size: 14px;  /* Tamanho de fonte menor */
            padding: 5px 15px;  /* Reduzido para deixar o botão pequeno */
            border-radius: 5px;
            border: none;
            cursor: pointer;
            margin-top: 10px;
        }
        .save-button:hover {
            background-color: rgba(255, 75, 75, 0.6);  /* Aumentar opacidade ao passar o mouse */
        }
        </style>
        <button class="save-button" onclick="saveRecommendation()">Salvar Recomendação</button>
    """, unsafe_allow_html=True)

    return recommendation

def restart_decision_tree():
    # Reiniciar a árvore de decisão
    if st.button("Reiniciar"):
        st.session_state.answers = {}
        st.experimental_set_query_params()  # Forçar recarregamento da página

def run_decision_tree():
    # Executar a árvore de decisão
    show_interactive_decision_tree()
    st.markdown("---")
    restart_decision_tree()

# Função JavaScript para salvar recomendação
def saveRecommendation():
    save_recommendation(st.session_state.recommendation)
