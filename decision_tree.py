import streamlit as st
import graphviz
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm

def get_questions():
    return [
        {
            "phase": "Fase 1: Aplicação",
            "questions": [
                {
                    "text": "A aplicação exige alta privacidade e controle centralizado?",
                    "options": ["Sim", "Não"]
                },
                {
                    "text": "A aplicação precisa de alta escalabilidade e eficiência energética?",
                    "options": ["Sim", "Não"]
                }
            ]
        },
        {
            "phase": "Fase 2: Consenso",
            "questions": [
                {
                    "text": "A rede exige alta resiliência contra ataques e falhas bizantinas?",
                    "options": ["Sim", "Não"]
                },
                {
                    "text": "A eficiência energética é um fator crucial para a rede?",
                    "options": ["Sim", "Não"]
                }
            ]
        },
        {
            "phase": "Fase 3: Infraestrutura",
            "questions": [
                {
                    "text": "A rede precisa integrar-se a sistemas legados de saúde (ex: EHRs, bancos de dados hospitalares)?",
                    "options": ["Sim", "Não"]
                },
                {
                    "text": "A infraestrutura precisa lidar com grandes volumes de dados ou dispositivos IoT?",
                    "options": ["Sim", "Não"]
                }
            ]
        },
        {
            "phase": "Fase 4: Governança",
            "questions": [
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
    ]

def show_interactive_decision_tree():
    st.header("Árvore de Decisão Interativa para Contextos de Saúde")

    questions = get_questions()
    
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 0
    
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    total_questions = sum(len(phase['questions']) for phase in questions)
    current_question_overall = sum(len(questions[i]['questions']) for i in range(st.session_state.current_phase)) + st.session_state.current_question
    st.progress(current_question_overall / total_questions)

    current_phase = questions[st.session_state.current_phase]
    current_question = current_phase["questions"][st.session_state.current_question]

    st.subheader(current_phase["phase"])
    answer = st.radio(current_question["text"], current_question["options"], key=f"question_{st.session_state.current_phase}_{st.session_state.current_question}")
    
    is_last_question = (st.session_state.current_phase == len(questions) - 1) and (st.session_state.current_question == len(current_phase["questions"]) - 1)
    button_text = "Finalizar" if is_last_question else "Próxima Pergunta"
    
    if st.button(button_text, key=f"button_{st.session_state.current_phase}_{st.session_state.current_question}"):
        try:
            st.session_state.answers[f"{current_phase['phase']}_{st.session_state.current_question}"] = answer
            
            if st.session_state.current_question < len(current_phase["questions"]) - 1:
                st.session_state.current_question += 1
            elif st.session_state.current_phase < len(questions) - 1:
                st.session_state.current_phase += 1
                st.session_state.current_question = 0
            else:
                show_recommendation(st.session_state.answers)
            
            st.rerun()
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar a resposta: {str(e)}")
            st.write("Por favor, tente novamente ou entre em contato com o suporte.")

    st.write(f"Fase atual: {st.session_state.current_phase + 1}/{len(questions)}")
    st.write(f"Pergunta atual: {st.session_state.current_question + 1}/{len(current_phase['questions'])}")
    st.write("Debug - Respostas atuais:", st.session_state.answers)

def show_recommendation(answers):
    st.subheader("Recomendação:")
    
    # Logic for DLT recommendation based on answers
    if answers.get("Fase 1: Aplicação_0") == "Sim":
        dlt = "DLT Permissionada Privada"
        consensus = "PBFT"
        applicable_dlts = ["Hyperledger Fabric", "Corda"]
        grouping = "Alta Segurança e Controle"
    elif answers.get("Fase 1: Aplicação_1") == "Sim":
        dlt = "DLT Pública ou Híbrida"
        consensus = "PoS, Tangle (IOTA)"
        applicable_dlts = ["Ethereum 2.0", "IOTA"]
        grouping = "Alta Escalabilidade em Redes IoT"
    elif answers.get("Fase 2: Consenso_0") == "Sim":
        dlt = "DLT Pública ou Permissionada"
        consensus = "PBFT, PoW, HoneyBadger BFT"
        applicable_dlts = ["Hyperledger Fabric", "Bitcoin", "Ethereum"]
        grouping = "Alta Segurança e Controle"
    else:
        dlt = "DLT Pública ou com Consenso Delegado"
        consensus = "DPoS"
        applicable_dlts = ["EOS", "Tron"]
        grouping = "Escalabilidade e Governança Flexível"

    st.write(f"DLT Recomendada: {dlt}")
    st.write(f"Algoritmos de Consenso: {consensus}")
    st.write(f"DLTs Aplicáveis: {', '.join(applicable_dlts)}")
    st.write(f"Agrupamento: {grouping}")

    st.write("Respostas:", answers)

def run_decision_tree():
    if 'current_phase' in st.session_state:
        del st.session_state.current_phase
    if 'current_question' in st.session_state:
        del st.session_state.current_question
    if 'answers' in st.session_state:
        del st.session_state.answers
    show_interactive_decision_tree()

# Keep other functions (calculate_metrics, generate_decision_tree) as they were
