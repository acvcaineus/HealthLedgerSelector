import streamlit as st
from user_management import login, register, logout, is_authenticated
from decision_tree import run_decision_tree
from database import get_user_recommendations
from utils import init_session_state
from metrics import calcular_gini, calcular_entropia, calcular_profundidade_decisoria, calcular_pruning

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

# Função para exibir o perfil do usuário
def show_user_profile():
    st.header("Perfil do Usuário")
    st.write(f"Bem-vindo, {st.session_state.username}!")

    recommendations = get_user_recommendations(st.session_state.username)
    
    if recommendations:
        st.subheader("Suas Recomendações Salvas:")
        for rec in recommendations:
            st.write(f"Cenário: {rec['scenario']}")
            st.write(f"DLT Recomendada: {rec['dlt']}")
            st.write(f"Algoritmo de Consenso: {rec['consensus']}")
            st.write(f"Data: {rec['timestamp']}")
            st.write("---")
    else:
        st.write("Você ainda não tem recomendações salvas.")

# Função principal que controla a navegação e o estado da sessão
def main():
    # Inicializa o estado da sessão se necessário
    init_session_state()

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
        menu_options = ['Início', 'Árvore de Decisão', 'Métricas', 'Perfil', 'Logout']

        # Exibe o seletor de opções de menu e mantém a página corrente no estado de sessão
        menu_option = st.sidebar.selectbox(
            "Escolha uma opção",
            menu_options,
            index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
        )

        # Atualiza a página no estado da sessão com base na escolha
        st.session_state.page = menu_option

        # Controle de navegação entre páginas
        if st.session_state.page == 'Início':
            show_home_page()
        elif st.session_state.page == 'Árvore de Decisão':
            run_decision_tree()
        elif st.session_state.page == 'Métricas':
            show_metrics()
        elif st.session_state.page == 'Perfil':
            show_user_profile()
        elif st.session_state.page == 'Logout':
            logout()
            st.session_state.page = 'Início'  # Retorna à página de login após o logout

if __name__ == "__main__":
    main()
