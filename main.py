import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning)
from utils import init_session_state

def show_user_profile():
    st.header(f"Perfil do Usuário: {st.session_state.username}")
    recommendations = get_user_recommendations(st.session_state.username)
    
    if recommendations:
        st.subheader("Últimas Recomendações")
        
        # Add a save all recommendations button
        if st.button("💾 Salvar Todas as Recomendações", 
                    help="Clique para salvar todas as recomendações novamente"):
            success_count = 0
            for rec in recommendations:
                try:
                    from database import save_recommendation
                    save_recommendation(
                        st.session_state.username,
                        "Healthcare DLT Selection",
                        {
                            'dlt': rec['dlt'],
                            'consensus': rec['consensus'],
                            'timestamp': rec['timestamp']
                        }
                    )
                    success_count += 1
                except Exception as e:
                    st.error(f"Erro ao salvar recomendação: {str(e)}")
            
            if success_count > 0:
                st.success(f"✅ {success_count} recomendações salvas com sucesso!")
        
        # Display individual recommendations
        for rec in recommendations:
            with st.expander(f"Recomendação de {rec['timestamp']}", expanded=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**DLT:** {rec['dlt']}")
                    st.write(f"**Algoritmo de Consenso:** {rec['consensus']}")
                    st.write(f"**Data:** {rec['timestamp']}")
                
                with col2:
                    if st.button("💾 Salvar Recomendação", 
                               key=f"save_rec_{rec['id']}",
                               help="Clique para salvar esta recomendação"):
                        try:
                            from database import save_recommendation
                            save_recommendation(
                                st.session_state.username,
                                "Healthcare DLT Selection",
                                {
                                    'dlt': rec['dlt'],
                                    'consensus': rec['consensus'],
                                    'timestamp': rec['timestamp']
                                }
                            )
                            st.success("✅ Recomendação salva com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao salvar recomendação: {str(e)}")
            st.markdown("---")
    else:
        st.info("Você ainda não tem recomendações salvas. Use o Framework Proposto para gerar recomendações.")

def main():
    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
    init_session_state()

    if not is_authenticated():
        st.title("SeletorDLTSaude - Login")
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.title("Menu")
        menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Perfil', 'Logout']
        
        menu_option = st.sidebar.selectbox(
            "Escolha uma opção",
            menu_options,
            index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
        )
        
        st.session_state.page = menu_option
        
        if menu_option == 'Início':
            st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
            st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")
            
            if st.button("Iniciar Questionário", help="Clique aqui para começar o processo de seleção de DLT"):
                st.session_state.page = "Framework Proposto"
                st.experimental_rerun()
                
        elif menu_option == 'Framework Proposto':
            run_decision_tree()
        elif menu_option == 'Métricas':
            st.title("Métricas e Análises")
            # Add metrics visualization code here
        elif menu_option == 'Perfil':
            show_user_profile()
        elif menu_option == 'Logout':
            logout()
            st.session_state.page = 'Início'
            st.experimental_rerun()

if __name__ == "__main__":
    main()
