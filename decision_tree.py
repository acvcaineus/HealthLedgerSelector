import streamlit as st
import graphviz
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm

questions = {
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
        st.session_state.current_phase = list(questions.keys())[0]
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

def gini_index(probs):
    return 1 - np.sum(np.square(probs))

def entropy(probs):
    probs = np.array(probs)
    return -np.sum(probs * np.log2(probs + 1e-9))

def calculate_depth(questions_dict):
    return len(questions_dict) + sum(len(q_list) for q_list in questions_dict.values())

def pruning_ratio(n_original, n_pruned):
    return (n_original - n_pruned) / n_original

def calculate_complexity(total_nodes):
    return total_nodes

def show_interactive_decision_tree():
    st.header("Árvore de Decisão Interativa para Contextos de Saúde")

    decision_tree = graphviz.Digraph()
    decision_tree.node('A', 'Início')

    current_phase = st.session_state.current_phase
    current_question_index = st.session_state.current_question_index
    questions_in_phase = questions[current_phase]

    current_question = questions_in_phase[current_question_index]["text"]
    options = questions_in_phase[current_question_index]["options"]

    st.subheader(f"{current_phase} - Pergunta {current_question_index + 1}")
    answer = st.radio(current_question, options, key=f"{current_phase}_{current_question_index}")

    st.session_state.answers[f"{current_phase}_{current_question_index}"] = answer

    previous_node = 'A'
    total_nodes = 1
    all_answers = []

    for phase, question_list in questions.items():
        for idx, q in enumerate(question_list):
            saved_answer = st.session_state.answers.get(f"{phase}_{idx}", None)
            if saved_answer:
                node_label = f"{phase} - Pergunta {idx + 1}: {saved_answer}"
                current_node = f"{phase}_{idx}_{saved_answer}"
                decision_tree.node(current_node, node_label)
                decision_tree.edge(previous_node, current_node)
                previous_node = current_node
                total_nodes += 1
                all_answers.append(saved_answer)

    st.graphviz_chart(decision_tree)

    if current_question_index < len(questions_in_phase) - 1:
        if st.button("Próxima Pergunta"):
            st.session_state.current_question_index += 1
    else:
        next_phase_index = list(questions.keys()).index(current_phase) + 1
        if next_phase_index < len(questions):
            st.session_state.current_phase = list(questions.keys())[next_phase_index]
            st.session_state.current_question_index = 0

    if len(all_answers) == len([q for qs in questions.values() for q in qs]):
        st.subheader("Métricas da Árvore de Decisão")

        num_yes = all_answers.count("Sim")
        num_no = all_answers.count("Não")
        total = len(all_answers)
        probs = [num_yes / total, num_no / total]

        gini = gini_index(probs)
        entropia = entropy(probs)
        profundidade = calculate_depth(questions)
        poda = pruning_ratio(total_nodes, total_nodes - 5)
        complexidade = calculate_complexity(total_nodes)

        st.write(f"Impureza de Gini: {gini:.2f}")
        st.write(f"Entropia: {entropia:.2f}")
        st.write(f"Profundidade Decisória: {profundidade}")
        st.write(f"Redução de Redundância (Pruning): {poda:.2%}")
        st.write(f"Complexidade Estrutural: {complexidade} nós")

        st.subheader("Recomendação de DLT e Algoritmo de Consenso")

        formatted_answers = {f"{phase}_{idx}": answer for phase, qs in questions.items() for idx, (_, answer) in enumerate(st.session_state.answers.items()) if phase in _}

        st.write("Defina os pesos para as características:")
        weights = {}
        weights["security"] = st.slider("Segurança", 1, 5, 3, key="security_weight")
        weights["scalability"] = st.slider("Escalabilidade", 1, 5, 3, key="scalability_weight")
        weights["energy_efficiency"] = st.slider("Eficiência Energética", 1, 5, 3, key="energy_efficiency_weight")
        weights["governance"] = st.slider("Governança", 1, 5, 3, key="governance_weight")

        if st.button("Gerar Recomendação"):
            recommendation = get_recommendation(formatted_answers, weights)
            
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