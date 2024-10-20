import streamlit as st
import graphviz
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm

# Cache the questions to avoid reloading them every time
@st.cache_data
def get_questions():
    return {
        "Fase 1: Aplicação": [
            {
                "text": "A aplicação exige alta privacidade e controle centralizado?",
                "options": ["Sim", "Não"]
            },
            {
                "text": "A aplicação precisa de alta escalabilidade e eficiência energética?",
                "options": ["Sim", "Não"]
            }
        ],
        "Fase 2: Consenso": [
            {
                "text": "A rede exige alta resiliência contra ataques e falhas bizantinas?",
                "options": ["Sim", "Não"]
            },
            {
                "text": "A eficiência energética é um fator crucial para a rede?",
                "options": ["Sim", "Não"]
            }
        ],
        "Fase 3: Infraestrutura": [
            {
                "text": "A rede precisa integrar-se a sistemas legados de saúde (ex: EHRs, bancos de dados hospitalares)?",
                "options": ["Sim", "Não"]
            },
            {
                "text": "A infraestrutura precisa lidar com grandes volumes de dados ou dispositivos IoT?",
                "options": ["Sim", "Não"]
            }
        ],
        "Fase 4: Governança": [
            {
                "text": "A rede precisa de governança centralizada?",
                "options": ["Sim", "Não"]
            },
            {
                "text": "A validação de consenso deve ser delegada a um subconjunto de validadores (DPoS)?",
                "options": ["Sim", "Não"]
            }
        ]
    }

def init_session_state():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = list(get_questions().keys())[0]
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

@st.cache_data
def calculate_metrics(answers):
    num_yes = answers.count("Sim")
    num_no = answers.count("Não")
    total = len(answers)
    probs = [num_yes / total, num_no / total]

    gini = 1 - np.sum(np.square(probs))
    entropy = -np.sum(probs * np.log2(probs + 1e-9))
    depth = len(get_questions()) + sum(len(q_list) for q_list in get_questions().values())
    pruning = (len(answers) - (len(answers) - 5)) / len(answers)
    complexity = len(answers)

    return {
        "Impureza de Gini": f"{gini:.2f}",
        "Entropia": f"{entropy:.2f}",
        "Profundidade Decisória": depth,
        "Redução de Redundância (Pruning)": f"{pruning:.2%}",
        "Complexidade Estrutural": f"{complexity} nós"
    }

@st.cache_data
def generate_decision_tree(answers):
    decision_tree = graphviz.Digraph()
    decision_tree.node('A', 'Início')

    previous_node = 'A'
    for phase, question_list in get_questions().items():
        for idx, q in enumerate(question_list):
            answer = answers.get(f"{phase}_{idx}")
            if answer:
                node_label = f"{phase} - Pergunta {idx + 1}: {answer}"
                current_node = f"{phase}_{idx}_{answer}"
                decision_tree.node(current_node, node_label)
                decision_tree.edge(previous_node, current_node)
                previous_node = current_node

    return decision_tree

def show_interactive_decision_tree():
    st.header("Árvore de Decisão Interativa para Contextos de Saúde")

    questions = get_questions()
    current_phase = st.session_state.current_phase
    current_question_index = st.session_state.current_question_index
    questions_in_phase = questions[current_phase]

    current_question = questions_in_phase[current_question_index]["text"]
    options = questions_in_phase[current_question_index]["options"]

    st.subheader(f"{current_phase} - Pergunta {current_question_index + 1}")
    answer = st.radio(current_question, options, key=f"{current_phase}_{current_question_index}")

    st.session_state.answers[f"{current_phase}_{current_question_index}"] = answer

    decision_tree = generate_decision_tree(st.session_state.answers)
    st.graphviz_chart(decision_tree)

    if current_question_index < len(questions_in_phase) - 1:
        if st.button("Próxima Pergunta"):
            st.session_state.current_question_index += 1
    else:
        next_phase_index = list(questions.keys()).index(current_phase) + 1
        if next_phase_index < len(questions):
            st.session_state.current_phase = list(questions.keys())[next_phase_index]
            st.session_state.current_question_index = 0

    all_answers = list(st.session_state.answers.values())
    if len(all_answers) == len([q for qs in questions.values() for q in qs]):
        st.subheader("Métricas da Árvore de Decisão")
        metrics = calculate_metrics(all_answers)
        for metric, value in metrics.items():
            st.write(f"{metric}: {value}")

        st.subheader("Recomendação de DLT e Algoritmo de Consenso")

        st.write("Defina os pesos para as características:")
        weights = {}
        weights["security"] = st.slider("Segurança", 1, 5, 3, key="security_weight")
        weights["scalability"] = st.slider("Escalabilidade", 1, 5, 3, key="scalability_weight")
        weights["energy_efficiency"] = st.slider("Eficiência Energética", 1, 5, 3, key="energy_efficiency_weight")
        weights["governance"] = st.slider("Governança", 1, 5, 3, key="governance_weight")

        if st.button("Gerar Recomendação"):
            recommendation = get_recommendation(st.session_state.answers, weights)
            
            st.write(f"DLT Recomendada: {recommendation['dlt']}")
            st.write(f"Grupo de Algoritmo de Consenso: {recommendation['consensus_group']}")
            st.write(f"Algoritmos Recomendados: {', '.join(recommendation['algorithms'])}")

            st.subheader("Comparação de Algoritmos de Consenso")
            comparison_data = compare_algorithms(recommendation['consensus_group'])
            df = pd.DataFrame(comparison_data)
            st.table(df)

            st.subheader("Avalie os Algoritmos")
            user_ratings = {}
            for alg in recommendation['algorithms']:
                user_ratings[alg] = st.slider(f"Avalie {alg}", 1, 5, 3, key=f"rating_{alg}")

            if st.button("Selecionar Algoritmo Final"):
                final_algorithm = select_final_algorithm(recommendation['consensus_group'], user_ratings)
                st.subheader("Algoritmo de Consenso Final Recomendado:")
                st.write(final_algorithm)

def run_decision_tree():
    init_session_state()
    show_interactive_decision_tree()
