import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)
from utils import init_session_state

def show_metrics():
    st.title("Métricas do Processo de Decisão")
    
    if 'recommendation' not in st.session_state:
        st.warning("Complete o processo de recomendação primeiro para ver as métricas.")
        if st.button("Ir para o Framework"):
            st.session_state.page = "Framework Proposto"
            st.experimental_rerun()
        return
        
    try:
        rec = st.session_state.recommendation
        
        # Accuracy metrics
        with st.expander("Precisão (Accuracy)", expanded=True):
            st.write("### Métricas de Precisão")
            col1, col2 = st.columns(2)
            
            with col1:
                if 'evaluation_matrix' in rec:
                    scores = [float(data['score']) for data in rec['evaluation_matrix'].values()]
                    correct_decisions = sum(1 for score in scores if score > 0.7)
                    total_decisions = len(scores)
                    
                    fig = go.Figure(data=[
                        go.Bar(name='Decisões Corretas', x=['Precisão'], y=[correct_decisions]),
                        go.Bar(name='Total', x=['Precisão'], y=[total_decisions])
                    ])
                    fig.update_layout(title="Precisão das Recomendações")
                    st.plotly_chart(fig)
                    
                    accuracy = correct_decisions / total_decisions if total_decisions > 0 else 0
                    st.metric("Precisão", f"{accuracy:.2%}")
                else:
                    st.warning("Dados de avaliação não disponíveis")
                
            with col2:
                st.write('''
                A precisão mede a proporção de decisões corretas em relação ao total.
                
                **Interpretação:**
                - Valores altos: Sistema confiável
                - Valores baixos: Necessita ajustes
                ''')
        
        # Sensitivity and Specificity
        with st.expander("Sensibilidade e Especificidade"):
            st.write("### Análise de Sensibilidade")
            
            if 'evaluation_matrix' in rec:
                col1, col2 = st.columns(2)
                
                true_positives = sum(1 for data in rec['evaluation_matrix'].values() 
                                   if float(data['score']) > 0.7)
                false_positives = sum(1 for data in rec['evaluation_matrix'].values() 
                                    if float(data['score']) <= 0.7)
                total = len(rec['evaluation_matrix'])
                
                sensitivity = true_positives / total if total > 0 else 0
                specificity = (total - false_positives) / total if total > 0 else 0
                
                with col1:
                    st.metric("Sensibilidade", f"{sensitivity:.2%}")
                with col2:
                    st.metric("Especificidade", f"{specificity:.2%}")
                
                # Create ROC-like visualization
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[0, specificity, 1],
                    y=[0, sensitivity, 1],
                    mode='lines+markers',
                    name='Curva ROC'
                ))
                fig.update_layout(
                    title="Visualização de Sensibilidade vs. Especificidade",
                    xaxis_title="1 - Especificidade",
                    yaxis_title="Sensibilidade"
                )
                st.plotly_chart(fig)
            else:
                st.warning("Dados insuficientes para calcular sensibilidade e especificidade")
        
        # Tree Depth
        with st.expander("Profundidade da Árvore"):
            st.write("### Análise de Profundidade")
            if 'answers' in st.session_state:
                depth = len(st.session_state.answers)
                total_nodes = depth * 2 + 1
                pruned_nodes = total_nodes - depth - 1
                pruning_ratio = calcular_pruning(total_nodes, pruned_nodes)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Profundidade Atual", depth)
                    st.progress(depth / 8)  # Assuming 8 is max depth
                with col2:
                    st.metric("Taxa de Poda", f"{pruning_ratio:.1%}")
                
                # Create tree depth visualization
                fig = go.Figure(go.Sunburst(
                    ids=['root'] + [f'level_{i}' for i in range(depth)],
                    labels=['Raiz'] + [f'Nível {i+1}' for i in range(depth)],
                    parents=[''] + ['root'] * depth,
                    values=[1] * (depth + 1)
                ))
                fig.update_layout(title="Visualização da Profundidade da Árvore")
                st.plotly_chart(fig)
            else:
                st.warning("Dados da árvore não disponíveis")
        
        # Add return button
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Retornar ao Framework"):
                st.session_state.page = "Framework Proposto"
                st.experimental_rerun()
        with col2:
            if st.button("Voltar ao Início"):
                st.session_state.page = "Início"
                st.experimental_rerun()
                
    except Exception as e:
        st.error(f"Erro ao processar métricas: {str(e)}")
        st.info("Por favor, tente reiniciar o processo de recomendação")

def show_home_page():
    # [Previous home page code remains unchanged]
    pass

def show_user_profile():
    # [Previous user profile code remains unchanged]
    pass

def main():
    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
    init_session_state()

    try:
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
                show_home_page()
            elif menu_option == 'Framework Proposto':
                run_decision_tree()
            elif menu_option == 'Métricas':
                show_metrics()
            elif menu_option == 'Perfil':
                show_user_profile()
            elif menu_option == 'Logout':
                logout()
                st.session_state.page = 'Início'
                st.experimental_rerun()
    except Exception as e:
        st.error(f"Erro na aplicação: {str(e)}")
        st.info("Por favor, recarregue a página ou faça login novamente.")

if __name__ == "__main__":
    main()
