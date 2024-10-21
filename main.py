import streamlit as st
from user_management import login, register, is_authenticated, logout
from utils import init_session_state
from decision_tree import run_decision_tree
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm
import pandas as pd
import math

# Funções para cálculo das métricas da árvore de decisão
def calcular_gini(classes):
    """Calcula a impureza de Gini."""
    total = sum(classes.values())
    gini = 1 - sum((count / total) ** 2 for count in classes.values())
    return gini

def calcular_entropia(classes):
    """Calcula a entropia."""
    total = sum(classes.values())
    entropia = -sum((count / total) * math.log2(count / total) for count in classes.values() if count != 0)
    return entropia

def calcular_profundidade_decisoria(decisoes):
    """Calcula a profundidade média da árvore de decisão."""
    if not decisoes:
        return 0
    profundidade_total = sum(decisoes)
    return profundidade_total / len(decisoes)

def calcular_pruning(total_nos, nos_podados):
    """Calcula o pruning ratio (proporção de nós podados)."""
    if total_nos == 0:
        return 0
    pruning_ratio = (total_nos - nos_podados) / total_nos
    return pruning_ratio

# Função para exibir a página inicial
def show_home_page():
    st.title("SeletorDLTSaude")
    st.write("Bem-vindo ao SeletorDLTSaude, um sistema de recomendação de tecnologias de ledger distribuído (DLT) para aplicações em saúde.")

    if st.button("Iniciar Questionário"):
        st.session_state.page = "Árvore de Decisão"
        st.rerun()

# Função para exibir as métricas calculadas
def show_metrics():
    st.header("Métricas da Árvore de Decisão")

    # Exemplo de respostas classificadas para calcular métricas
    classes = {"Sim": 70, "Não": 30}  # Classes de respostas para calcular Gini e Entropia
    decisoes = [3, 4, 2, 5]  # Exemplo de profundidade de decisão
    total_nos = 20
    nos_podados = 5

    gini = calcular_gini(classes)
    entropia = calcular_entropia(classes)
    profundidade = calcular_profundidade_decisoria(decisoes)
    pruning_ratio = calcular_pruning(total_nos, nos_podados)

    st.write(f"**Impureza de Gini**: {gini:.2f}")
    st.write(f"**Entropia**: {entropia:.2f}")
    st.write(f"**Profundidade Decisória**: {profundidade:.2f}")
    st.write(f"**Pruning Ratio**: {pruning_ratio:.2f}")

# Função principal que controla a navegação e o estado da sessão
def main():
    # Inicializa o estado da sessão se necessário
    if 'page' not in st.session_state:
        st.session_state.page = 'Início'

    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")

    if not is_authenticated():  # Verifica se o usuário está autenticado
        st.title("SeletorDLTSaude - Login")

        # Exibe abas para login e registro
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        # Barra lateral com opções de menu
        st.sidebar.title("Menu")
        menu_options = ['Início', 'Árvore de Decisão', 'Métricas', 'Logout']

        # Exibe o seletor de opções de menu e mantém a página corrente no estado de sessão
        menu_option = st.sidebar.selectbox(
            "Escolha uma opção",
            menu_options,
            index=menu_options.index(st.session_state.page) if 'page' in st.session_state and st.session_state.page in menu_options else 0
        )

        # Atualiza a página no estado da sessão com base na escolha
        st.session_state.page = menu_option

        # Controle de navegação entre páginas
        if st.session_state.page == 'Início':
            show_home_page()
        elif st.session_state.page == 'Árvore de Decisão':
            run_decision_tree()  # Executa a árvore de decisão
        elif st.session_state.page == 'Métricas':
            show_metrics()  # Exibe as métricas calculadas
        elif st.session_state.page == 'Logout':
            logout()
            st.session_state.page = 'Início'  # Retorna à página de login após o logout

if __name__ == "__main__":
    main()
