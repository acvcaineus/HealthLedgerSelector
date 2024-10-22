import streamlit as st
import graphviz as gv
import plotly.graph_objects as go
from database import save_recommendation
from decision_logic import get_recommendation

def get_questions():
    return {
        'Aplicação': [
            "A aplicação exige alta privacidade e controle centralizado?",
            "A aplicação precisa de alta escalabilidade e eficiência energética?"
        ],
        'Consenso': [
            "A rede exige alta resiliência contra ataques e falhas bizantinas?",
            "A eficiência energética é um fator crucial para a rede?"
        ],
        'Infraestrutura': [
            "A rede precisa integrar-se a sistemas legados de saúde (ex: EHRs, bancos de dados hospitalares)?",
            "A infraestrutura precisa lidar com grandes volumes de dados ou dispositivos IoT?"
        ],
        'Internet': [
            "A rede precisa de governança centralizada?",
            "A validação de consenso deve ser delegada a um subconjunto de validadores (DPoS)?"
        ]
    }

def init_session_state():
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 0
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.recommendation = None

def show_interactive_decision_tree():
    st.header('Framework Proposto para Contextos de Saúde')

    init_session_state()

    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    questions = get_questions()

    if st.session_state.current_phase >= len(phases):
        st.write("Todas as fases foram completadas!")
        show_recommendation(st.session_state.answers)
        return

    current_phase = phases[st.session_state.current_phase]
    current_question = questions[current_phase][st.session_state.current_question]

    st.subheader(f'Fase {st.session_state.current_phase + 1}: {current_phase}')
    answer = st.radio(current_question, ['Sim', 'Não'], key=f'question_{st.session_state.current_phase}_{st.session_state.current_question}')

    if st.button('Próxima Pergunta', key=f'button_{st.session_state.current_phase}_{st.session_state.current_question}'):
        st.session_state.answers[f'{current_phase}_{st.session_state.current_question}'] = answer

        if st.session_state.current_question < len(questions[current_phase]) - 1:
            st.session_state.current_question += 1
        else:
            st.session_state.current_question = 0
            st.session_state.current_phase += 1

        if st.session_state.current_phase >= len(phases):
            st.session_state.recommendation = show_recommendation(st.session_state.answers)
        else:
            st.rerun()

    total_questions = sum(len(q) for q in questions.values())
    current_question_overall = sum(len(questions[p]) for p in phases[:st.session_state.current_phase]) + st.session_state.current_question
    st.progress(current_question_overall / total_questions)

    st.write(f'Fase atual: {st.session_state.current_phase + 1}/{len(phases)}')
    st.write(f'Pergunta atual: {st.session_state.current_question + 1}/{len(questions[current_phase])}')

    st.subheader("Fluxo de Decisão")
    decision_flow = gv.Digraph(format="png")
    decision_flow.node("Início", "Início")
    for phase_key, question_key in st.session_state.answers.items():
        decision_flow.node(f"{phase_key}", f"{phase_key} - {question_key}")
        decision_flow.edge("Início", f"{phase_key}")
    st.graphviz_chart(decision_flow)

def show_recommendation(answers):
    st.subheader('Recomendação Final:')

    weights = {
        "security": 0.4,
        "scalability": 0.3,
        "energy_efficiency": 0.2,
        "governance": 0.1
    }

    recommendation = get_recommendation(answers, weights)
    st.session_state.recommendation = recommendation
    
    st.write(f"**DLT Recomendada**: {recommendation['dlt']}")
    st.write(f"**Grupo de Consenso**: {recommendation['consensus_group']}")
    st.write(f"**Algoritmo de Consenso Recomendado**: {recommendation['consensus']}")
    
    st.subheader("Matriz de Avaliação")
    evaluation_matrix = recommendation['evaluation_matrix']
    fig = go.Figure(data=[go.Bar(x=list(evaluation_matrix.keys()), y=list(evaluation_matrix.values()))])
    fig.update_layout(title="Pontuação das DLTs", xaxis_title="DLTs", yaxis_title="Pontuação")
    st.plotly_chart(fig)

    st.subheader("Pontuações dos Algoritmos de Consenso")
    consensus_scores = {alg: sum(consensus_algorithms[alg].values()) for alg in recommendation['algorithms']}
    fig = go.Figure(data=[go.Bar(x=list(consensus_scores.keys()), y=list(consensus_scores.values()))])
    fig.update_layout(title="Pontuação dos Algoritmos de Consenso", xaxis_title="Algoritmos", yaxis_title="Pontuação")
    st.plotly_chart(fig)

    with st.expander("Ver Respostas Acumuladas"):
        st.json(answers)

    if st.button("Salvar Recomendação"):
        scenario = "Cenário Geral"
        save_recommendation(st.session_state.username, scenario, recommendation)
        st.success("Recomendação salva com sucesso no seu perfil!")

    st.button("Comparar Algoritmos", on_click=lambda: setattr(st.session_state, 'page', 'Comparação de Recomendações'))

    return recommendation

def restart_decision_tree():
    if st.button("Reiniciar"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def run_decision_tree():
    show_interactive_decision_tree()
    st.markdown("---")
    restart_decision_tree()