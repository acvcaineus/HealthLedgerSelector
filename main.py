import streamlit as st
from user_management import login, register, is_authenticated, logout
from utils import init_session_state
from decision_tree import run_decision_tree
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm
import pandas as pd

def show_home_page():
    st.title("SeletorDLTSaude")
    st.write("Bem-vindo ao SeletorDLTSaude, um sistema de recomendação de tecnologias de ledger distribuído (DLT) para aplicações em saúde.")
    
    if st.button("Iniciar Questionário"):
        st.session_state.page = "Árvore de Decisão"
        st.rerun()

def show_questionnaire():
    st.header("Questionário de Seleção de DLT")
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    scenario = "Registros Médicos Eletrônicos (EMR)"
    if st.session_state.step < len(questions[scenario]):
        current_question = questions[scenario][st.session_state.step]
        st.subheader(current_question['text'])
        st.write(f"Camada: {current_question['shermin_layer']}")
        st.write(f"Característica principal: {current_question['main_characteristic']}")
        answer = st.radio("Escolha uma opção:", current_question['options'])

        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question['id']] = answer
            st.session_state.step += 1
            if st.session_state.step >= len(questions[scenario]):
                st.session_state.page = "Recomendações"
            st.rerun()
    else:
        st.session_state.page = "Recomendações"
        st.rerun()

def show_weights():
    st.header("Definir Pesos das Características")
    st.write("Atribua um peso de 1 a 5 para cada característica, onde 1 é menos importante e 5 é mais importante.")

    weights = {}
    weights["security"] = st.slider("Segurança", 1, 5, 3)
    weights["scalability"] = st.slider("Escalabilidade", 1, 5, 3)
    weights["energy_efficiency"] = st.slider("Eficiência Energética", 1, 5, 3)
    weights["governance"] = st.slider("Governança", 1, 5, 3)
    weights["decentralization"] = st.slider("Descentralização", 1, 5, 3)

    st.session_state.weights = weights
    st.session_state.page = "recommendation"
    st.rerun()

def show_recommendation():
    st.header("Recomendação de DLT e Algoritmo de Consenso")

    if 'weights' not in st.session_state or not st.session_state.weights:
        st.warning('Por favor, defina os pesos das características primeiro.')
        show_weights()
        return

    if 'recommendation' not in st.session_state and 'weights' in st.session_state and st.session_state.weights:
        if st.button('Gerar Recomendação'):
            recommendation = get_recommendation(st.session_state.answers, st.session_state.weights)
            st.session_state.recommendation = recommendation
            st.rerun()
    else:
        recommendation = st.session_state.recommendation

        st.subheader("DLT Recomendada:")
        st.write(recommendation["dlt"])
        st.subheader("Grupo de Algoritmo de Consenso Recomendado:")
        st.write(recommendation["consensus_group"])
        st.subheader("Algoritmos Recomendados:")
        st.write(", ".join(recommendation["algorithms"]))

        st.subheader("Comparação de Algoritmos de Consenso:")
        comparison_data = compare_algorithms(recommendation["consensus_group"])
        df = pd.DataFrame(comparison_data)
        st.table(df)

        st.subheader("Selecione as Prioridades para o Algoritmo Final:")
        priorities = {}
        priorities["Segurança"] = st.slider("Segurança", 1, 5, 3)
        priorities["Escalabilidade"] = st.slider("Escalabilidade", 1, 5, 3)
        priorities["Eficiência Energética"] = st.slider("Eficiência Energética", 1, 5, 3)
        priorities["Governança"] = st.slider("Governança", 1, 5, 3)

        if st.button("Selecionar Algoritmo Final"):
            final_algorithm = select_final_algorithm(recommendation["consensus_group"], priorities)
            st.subheader("Algoritmo de Consenso Final Recomendado:")
            st.write(final_algorithm)

def main():
    init_session_state()
    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")

    if not is_authenticated():
        st.title("SeletorDLTSaude - Login")
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.title("Menu")

        menu_options = ['Árvore de Decisão', 'Início', 'Recomendações', 'Comparação de Frameworks', 'Logout']
        menu_option = st.sidebar.selectbox(
            "Escolha uma opção",
            menu_options,
            index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
        )

        st.session_state.page = menu_option

        if menu_option == 'Árvore de Decisão':
            run_decision_tree()
        elif menu_option == 'Início':
            show_home_page()
        elif menu_option == 'Recomendações':
            show_recommendation()
        elif menu_option == 'Comparação de Frameworks':
            st.write("Página de Comparação de Frameworks em desenvolvimento.")
        elif menu_option == 'Logout':
            logout()

if __name__ == "__main__":
    main()
