import streamlit as st
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm

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

def show_interactive_decision_tree():
    st.header('Árvore de Decisão Interativa para Contextos de Saúde')

    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 0
        st.session_state.current_question = 0
        st.session_state.answers = {}

    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    questions = get_questions()

    current_phase = phases[st.session_state.current_phase]
    current_question = questions[current_phase][st.session_state.current_question]

    st.subheader(f'Fase {st.session_state.current_phase + 1}: {current_phase}')
    answer = st.radio(current_question, ['Sim', 'Não'], key=f'question_{st.session_state.current_phase}_{st.session_state.current_question}')

    if st.button('Próxima Pergunta', key=f'button_{st.session_state.current_phase}_{st.session_state.current_question}'):
        if answer:
            st.session_state.answers[f'{current_phase}_{st.session_state.current_question}'] = answer
            next_question, next_phase = determine_next_question(current_phase, st.session_state.current_question, answer)
            
            if next_phase != current_phase:
                st.session_state.current_phase += 1
                st.session_state.current_question = 0
            else:
                st.session_state.current_question = next_question

            if st.session_state.current_phase >= len(phases):
                show_recommendation(st.session_state.answers)
            else:
                st.rerun()
        else:
            st.warning('Por favor, selecione uma resposta antes de prosseguir.')

    total_questions = sum(len(q) for q in questions.values())
    current_question_overall = sum(len(questions[p]) for p in phases[:st.session_state.current_phase]) + st.session_state.current_question
    st.progress(current_question_overall / total_questions)
    
    st.write(f'Fase atual: {st.session_state.current_phase + 1}/{len(phases)}')
    st.write(f'Pergunta atual: {st.session_state.current_question + 1}/{len(questions[current_phase])}')
    st.write('Debug - Respostas atuais:', st.session_state.answers)

def determine_next_question(current_phase, current_question, answer):
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    questions = get_questions()
    
    if current_question < len(questions[current_phase]) - 1:
        return current_question + 1, current_phase
    else:
        next_phase_index = phases.index(current_phase) + 1
        if next_phase_index < len(phases):
            return 0, phases[next_phase_index]
        else:
            return 0, current_phase  # This will trigger the show_recommendation function

def show_recommendation(answers):
    st.subheader("Recomendação:")
    
    # Simplified logic for demonstration purposes
    if answers.get("Aplicação_0") == "Sim":
        dlt = "DLT Permissionada Privada"
        consensus = "PBFT"
    elif answers.get("Aplicação_1") == "Sim":
        dlt = "DLT Pública ou Híbrida"
        consensus = "PoS"
    elif answers.get("Consenso_0") == "Sim":
        dlt = "DLT Pública ou Permissionada"
        consensus = "PoW"
    else:
        dlt = "DLT Pública ou com Consenso Delegado"
        consensus = "DPoS"

    st.write(f"DLT Recomendada: {dlt}")
    st.write(f"Algoritmo de Consenso Recomendado: {consensus}")
    st.write("Respostas:", answers)

def run_decision_tree():
    if 'current_phase' in st.session_state:
        del st.session_state.current_phase
    if 'current_question' in st.session_state:
        del st.session_state.current_question
    if 'answers' in st.session_state:
        del st.session_state.answers
    show_interactive_decision_tree()
