import streamlit as st
import graphviz
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm

def get_questions():
    return [
        {
            "text": "A aplicação exige alta segurança e controle dos dados sensíveis?",
            "options": ["Sim", "Não"]
        },
        {
            "text": "A aplicação precisa de alta eficiência operacional em redes locais?",
            "options": ["Sim", "Não"]
        },
        {
            "text": "A rede exige escalabilidade e governança flexível?",
            "options": ["Sim", "Não"]
        },
        {
            "text": "A infraestrutura precisa lidar com alta escalabilidade em redes IoT?",
            "options": ["Sim", "Não"]
        },
        {
            "text": "A rede precisa de alta segurança e descentralização de dados críticos?",
            "options": ["Sim", "Não"]
        }
    ]

def show_interactive_decision_tree():
    st.header("Árvore de Decisão Interativa para Contextos de Saúde")

    questions = get_questions()
    
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    
    if 'answers' not in st.session_state:
        st.session_state.answers = []

    if st.session_state.current_question < len(questions):
        question = questions[st.session_state.current_question]
        answer = st.radio(question["text"], question["options"])
        
        if st.button("Próxima Pergunta" if st.session_state.current_question < len(questions) - 1 else "Finalizar"):
            st.session_state.answers.append(answer)
            st.session_state.current_question += 1
            st.experimental_rerun()
    
    else:
        show_recommendation(st.session_state.answers)

def show_recommendation(answers):
    st.subheader("Recomendação:")
    
    if answers[0] == "Sim":
        st.write("DLT Recomendada: DLT Permissionada Privada")
        st.write("Algoritmos de Consenso: PBFT")
        st.write("DLTs Aplicáveis: Hyperledger Fabric, Corda")
        st.write("Agrupamento: Alta Segurança e Controle")
    elif answers[2] == "Sim":
        st.write("DLT Recomendada: DLT Pública ou Híbrida")
        st.write("Algoritmos de Consenso: PoS, DPoS")
        st.write("DLTs Aplicáveis: Ethereum, Algorand")
        st.write("Agrupamento: Escalabilidade e Governança Flexível")
    # Add more conditions based on the answers

    st.write("Respostas:", answers)

def run_decision_tree():
    if 'current_question' in st.session_state:
        del st.session_state.current_question
    if 'answers' in st.session_state:
        del st.session_state.answers
    show_interactive_decision_tree()

# Keep other functions (calculate_metrics, generate_decision_tree) as they were
