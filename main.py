import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from user_management import login, register, is_authenticated, logout
from database import get_user_recommendations, save_recommendation, save_feedback
from decision_logic import get_recommendation, get_comparison_data, get_sunburst_data
from dlt_data import scenarios, questions, dlt_options, consensus_options, metrics
from utils import init_session_state

def show_recommendation():
    if 'recommendation' not in st.session_state:
        st.error("Por favor, complete o questionário primeiro para receber uma recomendação.")
        return

    recommendation = st.session_state.recommendation
    st.header("Recomendação")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Framework DLT")
        st.info(recommendation['dlt'])
    with col2:
        st.subheader("Algoritmo de Consenso")
        st.info(recommendation['consensus'])

    with st.expander("Explicação Detalhada"):
        st.markdown(f'''
        **DLT Recomendada:** {recommendation['dlt']}
        {recommendation['dlt_explanation']}

        **Algoritmo de Consenso Recomendado:** {recommendation['consensus']}
        {recommendation['consensus_explanation']}
        ''')

    st.header("Feedback")
    st.write("Por favor, forneça seu feedback sobre a recomendação:")

    col1, col2 = st.columns(2)
    with col1:
        rating = st.slider("Avalie a qualidade da recomendação:", 1, 5, 3)
    with col2:
        usefulness = st.selectbox("Quão útil foi esta recomendação?", 
                                  ["Muito útil", "Útil", "Neutro", "Pouco útil", "Nada útil"])

    feedback_text = st.text_area("Seus comentários:", max_chars=500, 
                                 help="Por favor, forneça detalhes sobre o que você achou da recomendação.")
    
    specific_feedback = st.multiselect("Selecione os aspectos que você gostaria de comentar:",
                                       ["Clareza da explicação", "Relevância para o cenário", 
                                        "Comparação com outras soluções", "Facilidade de implementação"])

    if st.button("Enviar Feedback"):
        if feedback_text.strip() == "":
            st.warning("Por favor, escreva um comentário antes de enviar o feedback.")
        else:
            feedback_data = {
                "rating": rating,
                "usefulness": usefulness,
                "comment": feedback_text,
                "specific_aspects": specific_feedback
            }
            save_feedback(st.session_state.username, st.session_state.scenario, recommendation, feedback_data)
            st.success("Obrigado pelo seu feedback! Sua opinião é muito importante para nós.")
            st.balloons()

    if st.button("Voltar para a Página Inicial"):
        st.session_state.page = "home"
        st.rerun()

def show_questionnaire():
    st.header("Questionário")
    if st.session_state.scenario not in questions:
        st.error(f"Cenário '{st.session_state.scenario}' não encontrado.")
        return

    scenario_questions = questions[st.session_state.scenario]
    if st.session_state.step > len(scenario_questions):
        st.session_state.page = "recommendation"
        recommendation = get_recommendation(st.session_state.answers, st.session_state.weights)
        st.session_state.recommendation = recommendation
        st.rerun()
        return

    question = scenario_questions[st.session_state.step - 1]
    st.subheader(f"Pergunta {st.session_state.step}")
    st.write(question['text'])

    answer = st.radio("Selecione uma opção:", question['options'])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Voltar") and st.session_state.step > 1:
            st.session_state.step -= 1
            st.rerun()
    with col2:
        if st.button("Próximo"):
            st.session_state.answers[question['id']] = answer
            if st.session_state.step < len(scenario_questions):
                st.session_state.step += 1
            else:
                st.session_state.page = "recommendation"
                recommendation = get_recommendation(st.session_state.answers, st.session_state.weights)
                st.session_state.recommendation = recommendation
            st.rerun()

def show_scenario_selection():
    st.header("Escolha um Cenário de Saúde")
    scenario = st.selectbox("Selecione um cenário", list(scenarios.keys()))

    st.write(f"**Descrição do cenário:** {scenarios[scenario]}")

    if st.button("Iniciar"):
        st.session_state.scenario = scenario
        st.session_state.step = 1
        st.session_state.answers = {}
        st.session_state.page = "questionnaire"
        st.rerun()

def show_home_page():
    st.header("Bem-vindo ao SeletorDLTSaude")
    st.write("""
    O SeletorDLTSaude é uma ferramenta interativa projetada para ajudar profissionais e pesquisadores 
    da área de saúde a escolher a melhor solução de Tecnologia de Ledger Distribuído (DLT) e o algoritmo 
    de consenso mais adequado para seus projetos.
    """)

    if st.button("Iniciar Questionário"):
        st.session_state.page = "scenario_selection"
        st.rerun()

def main():
    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
    init_session_state()

    st.title("SeletorDLTSaude")
    st.sidebar.image("assets/logo.svg", use_column_width=True)

    if not is_authenticated():
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.success(f"Logado como {st.session_state.username}")
        st.sidebar.button("Sair", on_click=logout)

        if 'page' not in st.session_state:
            st.session_state.page = "home"

        if st.session_state.page == "home":
            show_home_page()
        elif st.session_state.page == "scenario_selection":
            show_scenario_selection()
        elif st.session_state.page == "questionnaire":
            show_questionnaire()
        elif st.session_state.page == "recommendation":
            show_recommendation()

        st.sidebar.header("Recomendações Anteriores")
        user_recommendations = get_user_recommendations(st.session_state.username)
        for rec in user_recommendations:
            with st.sidebar.expander(f"{rec['scenario']} - {rec['timestamp']}"):
                st.write(f"DLT: {rec['dlt']}")
                st.write(f"Consenso: {rec['consensus']}")

if __name__ == "__main__":
    main()
