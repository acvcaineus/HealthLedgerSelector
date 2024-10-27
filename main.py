import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import get_recommendation, compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)
import traceback
import numpy as np

def create_gini_radar(gini_values):
    """Create an interactive radar chart for Gini index visualization"""
    categories = ['Separação de Classes', 'Pureza dos Dados', 'Consistência', 'Precisão']
    
    fig = go.Figure()
    
    # Add trace for current values
    fig.add_trace(go.Scatterpolar(
        r=[1-gini_values, 1-gini_values/2, (1-gini_values)*0.8, (1-gini_values)*0.9],
        theta=categories,
        fill='toself',
        name='Métricas Atuais'
    ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Análise do Índice de Gini",
        height=400
    )
    
    return fig

def create_entropy_evolution(answers):
    """Create an interactive line chart for entropy evolution"""
    entropy_values = []
    classes = {}
    
    # Calculate entropy for each step
    for i in range(len(answers)):
        partial_answers = dict(list(answers.items())[:i+1])
        weights = {"security": 0.4, "scalability": 0.25, "energy_efficiency": 0.2, "governance": 0.15}
        recommendation = get_recommendation(partial_answers, weights)
        classes = {k: v['score'] for k, v in recommendation['evaluation_matrix'].items()}
        entropy_values.append(calcular_entropia(classes))
    
    fig = go.Figure()
    
    # Add trace for entropy evolution
    fig.add_trace(go.Scatter(
        x=list(range(1, len(entropy_values) + 1)),
        y=entropy_values,
        mode='lines+markers',
        name='Evolução da Entropia',
        hovertemplate='Passo %{x}<br>Entropia: %{y:.2f}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title="Evolução da Entropia no Processo Decisório",
        xaxis_title="Número de Perguntas Respondidas",
        yaxis_title="Entropia (bits)",
        height=400,
        showlegend=True
    )
    
    return fig

def create_metrics_dashboard(depth, pruning_ratio, confidence):
    """Create an interactive dashboard for decision tree metrics"""
    fig = go.Figure()
    
    # Add gauge charts
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=depth,
        title={'text': "Profundidade da Árvore"},
        gauge={'axis': {'range': [0, 10]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 3], 'color': "lightgreen"},
                   {'range': [3, 7], 'color': "yellow"},
                   {'range': [7, 10], 'color': "red"}
               ]},
        domain={'row': 0, 'column': 0}
    ))
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=pruning_ratio * 100,
        title={'text': "Taxa de Poda (%)"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "darkgreen"},
               'steps': [
                   {'range': [0, 30], 'color': "red"},
                   {'range': [30, 70], 'color': "yellow"},
                   {'range': [70, 100], 'color': "lightgreen"}
               ]},
        domain={'row': 0, 'column': 1}
    ))
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        title={'text': "Confiança (%)"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "darkred"},
               'steps': [
                   {'range': [0, 50], 'color': "red"},
                   {'range': [50, 80], 'color': "yellow"},
                   {'range': [80, 100], 'color': "lightgreen"}
               ]},
        domain={'row': 0, 'column': 2}
    ))
    
    # Update layout
    fig.update_layout(
        grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
        title="Dashboard de Métricas da Árvore de Decisão",
        height=400
    )
    
    return fig

def show_metrics_explanation():
    """Display enhanced metrics explanations with interactive visualizations"""
    st.header("Métricas Técnicas do Framework")
    
    # Get necessary values from session state
    answers = st.session_state.get('answers', {})
    if not answers:
        st.warning("Complete o processo de seleção para ver as métricas detalhadas.")
        return
        
    weights = {"security": 0.4, "scalability": 0.25, "energy_efficiency": 0.2, "governance": 0.15}
    recommendation = get_recommendation(answers, weights)
    classes = {k: v['score'] for k, v in recommendation['evaluation_matrix'].items()}
    
    gini_values = calcular_gini(classes)
    depth = calcular_profundidade_decisoria(list(range(len(answers))))
    total_nos = len(answers) * 2 + 1
    nos_podados = total_nos - len(answers) - 1
    pruning_ratio = calcular_pruning(total_nos, nos_podados)
    confidence = recommendation.get('confidence_value', 0.0)
    
    # Gini Index Section
    with st.expander("Índice de Gini - Pureza da Classificação"):
        st.write("### Análise do Índice de Gini")
        gini_fig = create_gini_radar(gini_values)
        st.plotly_chart(gini_fig)
        st.markdown('''
            O Índice de Gini mede a pureza da classificação:
            - **0-0.3**: Alta pureza - Decisão muito confiável
            - **0.3-0.6**: Pureza moderada - Decisão aceitável
            - **>0.6**: Baixa pureza - Decisão precisa ser revisada
        ''')
    
    # Entropy Evolution
    with st.expander("Evolução da Entropia - Processo Decisório"):
        st.write("### Evolução da Entropia nas Decisões")
        entropy_fig = create_entropy_evolution(answers)
        st.plotly_chart(entropy_fig)
        st.markdown('''
            A entropia mostra a incerteza no processo decisório:
            - **Descendente**: Aumento da certeza nas decisões
            - **Estável**: Consistência nas decisões
            - **Ascendente**: Aumento da incerteza
        ''')
    
    # Decision Tree Metrics
    with st.expander("Métricas da Árvore de Decisão"):
        st.write("### Dashboard de Métricas")
        metrics_fig = create_metrics_dashboard(depth, pruning_ratio, confidence)
        st.plotly_chart(metrics_fig)
        st.markdown('''
            Análise das métricas principais:
            - **Profundidade**: Complexidade do processo decisório
            - **Taxa de Poda**: Eficiência da simplificação
            - **Confiança**: Confiabilidade da recomendação
        ''')
    
    # Framework Justification
    with st.expander("Justificativa do Framework"):
        st.write("### Fundamentação do Framework")
        st.markdown('''
            O framework foi desenvolvido considerando:
            1. **Segurança (40%)**: 
               - Proteção de dados sensíveis de saúde
               - Conformidade com LGPD e HIPAA
            2. **Escalabilidade (25%)**:
               - Capacidade de crescimento da rede
               - Suporte a múltiplos nós e transações
            3. **Eficiência Energética (20%)**:
               - Sustentabilidade da solução
               - Custo operacional otimizado
            4. **Governança (15%)**:
               - Flexibilidade administrativa
               - Controle de acesso e permissões
        ''')

def init_session_state():
    """Initialize all required session state variables with error handling"""
    try:
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.page = 'Início'
            st.session_state.answers = {}
            st.session_state.error = None
            st.session_state.loading = False
            st.session_state.recommendation = None
    except Exception as e:
        st.error(f"Error initializing session state: {str(e)}")
        st.session_state.error = str(e)

def main():
    """Main application with improved error handling and state management"""
    try:
        st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
        init_session_state()

        if st.session_state.error:
            st.error("Ocorreu um erro ao carregar o conteúdo")
            if st.button("Tentar Novamente"):
                st.experimental_rerun()
            return

        if not is_authenticated():
            st.title("SeletorDLTSaude - Login")
            tab1, tab2 = st.tabs(["Login", "Registrar"])
            with tab1:
                login()
            with tab2:
                register()
        else:
            with st.sidebar:
                st.title("Menu")
                menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Perfil', 'Logout']
                
                try:
                    menu_option = st.selectbox(
                        "Escolha uma opção",
                        menu_options,
                        index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
                    )
                    st.session_state.page = menu_option
                except Exception as e:
                    st.error(f"Error in navigation: {str(e)}")
                    menu_option = 'Início'

            try:
                if menu_option == 'Início':
                    st.title("SeletorDLTSaude")
                    st.write("Bem-vindo ao sistema de seleção de DLT para saúde.")
                elif menu_option == 'Framework Proposto':
                    run_decision_tree()
                elif menu_option == 'Métricas':
                    show_metrics_explanation()
                elif menu_option == 'Perfil':
                    st.header(f"Perfil do Usuário: {st.session_state.username}")
                    recommendations = get_user_recommendations(st.session_state.username)
                    if recommendations:
                        st.subheader("Últimas Recomendações")
                        for rec in recommendations:
                            st.write(f"DLT: {rec['dlt']}")
                            st.write(f"Consenso: {rec['consensus']}")
                            st.write(f"Data: {rec['timestamp']}")
                            st.markdown("---")
                elif menu_option == 'Logout':
                    logout()
                    st.session_state.page = 'Início'
                    st.experimental_rerun()

            except Exception as e:
                st.error(f"Error loading content: {str(e)}")
                if st.button("Tentar Novamente"):
                    st.experimental_rerun()

    except Exception as e:
        st.error(f"Critical error: {str(e)}")
        st.code(traceback.format_exc())
        st.session_state.error = str(e)
        if st.button("Reiniciar Aplicação"):
            st.session_state.clear()
            st.experimental_rerun()

if __name__ == "__main__":
    main()
