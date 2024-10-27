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

def reset_session_state():
    """Reset session state on errors"""
    try:
        st.session_state.answers = {}
        st.session_state.error = None
        st.session_state.loading = False
        st.session_state.recommendation = None
    except Exception as e:
        st.error(f"Error resetting session state: {str(e)}")

def show_home_page():
    """Display home page with framework explanation and reference table"""
    st.title("SeletorDLTSaude")
    st.write("Bem-vindo ao sistema de seleção de DLT para saúde.")

    st.header("Objetivo do Framework")
    st.markdown('''
        O SeletorDLTSaude é uma aplicação interativa desenvolvida para ajudar profissionais 
        e pesquisadores a escolherem a melhor solução de Distributed Ledger Technology (DLT) 
        e o algoritmo de consenso mais adequado para projetos de saúde. 
        
        A aplicação guia o usuário através de um processo estruturado em quatro fases:
        - **Fase de Aplicação**: Avalia requisitos de privacidade e integração
        - **Fase de Consenso**: Analisa necessidades de segurança e eficiência
        - **Fase de Infraestrutura**: Considera escalabilidade e performance
        - **Fase de Internet**: Avalia governança e interoperabilidade
    ''')

    st.subheader("Tabela de Referência de DLTs e Algoritmos")
    data = {
        'Grupo': [
            'Alta Segurança e Controle',
            'Alta Segurança e Controle',
            'Alta Eficiência Operacional',
            'Alta Eficiência Operacional',
            'Escalabilidade e Governança Flexível',
            'Alta Escalabilidade em Redes IoT'
        ],
        'Tipo DLT': [
            'DLT Permissionada Privada',
            'DLT Pública Permissionless',
            'DLT Permissionada Simples',
            'DLT Híbrida',
            'DLT com Consenso Delegado',
            'DLT Pública'
        ],
        'Nome DLT': [
            'Hyperledger Fabric',
            'Bitcoin',
            'Quorum',
            'Ethereum 2.0',
            'EOS',
            'IOTA'
        ],
        'Algoritmo de Consenso': [
            'PBFT',
            'PoW',
            'RAFT/PoA',
            'PoS',
            'DPoS',
            'Tangle'
        ],
        'Principais Características': [
            'Alta segurança e resiliência contra falhas bizantinas',
            'Alta segurança e descentralização total',
            'Simplicidade e eficiência em redes locais',
            'Alta escalabilidade e eficiência energética',
            'Governança flexível e alta performance',
            'Escalabilidade para IoT e dados em tempo real'
        ]
    }
    
    df = pd.DataFrame(data)
    st.table(df)

    if st.button("Iniciar Seleção de DLT", type="primary"):
        st.session_state.page = 'Framework Proposto'
        st.experimental_rerun()

def show_fallback_ui():
    """Display fallback UI when main content fails to load"""
    st.error("Ocorreu um erro ao carregar o conteúdo")
    if st.button("Tentar Novamente"):
        st.experimental_rerun()

def create_entropy_graph(answers):
    """Create entropy evolution graph with error handling"""
    try:
        with st.spinner('Calculando evolução da entropia...'):
            entropy_values = []
            weights = {
                "security": float(0.4),
                "scalability": float(0.25),
                "energy_efficiency": float(0.20),
                "governance": float(0.15)
            }
            for i in range(len(answers)):
                partial_answers = dict(list(answers.items())[:i+1])
                classes = {k: v['score'] for k, v in get_recommendation(partial_answers, weights)['evaluation_matrix'].items()}
                entropy_values.append(calcular_entropia(classes))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(1, len(entropy_values) + 1)),
                y=entropy_values,
                mode='lines+markers',
                name='Evolução da Entropia'
            ))
            fig.update_layout(
                title="Evolução da Entropia Durante o Processo Decisório",
                xaxis_title="Número de Perguntas Respondidas",
                yaxis_title="Entropia (bits)"
            )
            return fig
    except Exception as e:
        st.error(f"Error creating entropy graph: {str(e)}")
        return None

def create_metrics_dashboard(depth, pruning_ratio, confidence):
    """Create metrics dashboard with error handling"""
    try:
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=depth,
            title={'text': "Profundidade da Árvore"},
            gauge={'axis': {'range': [0, 10]},
                   'bar': {'color': "darkblue"}},
            domain={'row': 0, 'column': 0}
        ))
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=pruning_ratio * 100,
            title={'text': "Taxa de Poda (%)"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "darkgreen"}},
            domain={'row': 0, 'column': 1}
        ))
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=confidence * 100,
            title={'text': "Confiança (%)"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "darkred"}},
            domain={'row': 0, 'column': 2}
        ))
        fig.update_layout(
            grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
            title="Dashboard de Métricas da Árvore de Decisão"
        )
        return fig
    except Exception as e:
        st.error(f"Error creating metrics dashboard: {str(e)}")
        return None

def show_metrics():
    """Display metrics with enhanced explanations"""
    st.header("Métricas Técnicas do Processo de Decisão")
    
    try:
        if 'recommendation' in st.session_state:
            with st.spinner('Carregando métricas...'):
                rec = st.session_state.recommendation
                if 'evaluation_matrix' in rec:
                    classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
                    gini = calcular_gini(classes)
                    entropy = calcular_entropia(classes)
                    
                    # Show Gini Index Visualization with explanation
                    st.subheader("1. Índice de Gini")
                    with st.expander("Ver Explicação do Índice de Gini"):
                        st.markdown("""
                        ### O que é o Índice de Gini?
                        O Índice de Gini mede a pureza da classificação das DLTs. É calculado usando a fórmula:
                        
                        $Gini = 1 - \sum_{i=1}^{n} p_i^2$
                        
                        Onde:
                        - $p_i$ é a proporção de cada classe no conjunto
                        
                        ### Interpretação dos Eixos:
                        - **Separação de Classes**: Indica quão bem as DLTs são distinguidas
                        - **Pureza dos Dados**: Medida da homogeneidade dos grupos
                        - **Consistência**: Estabilidade da classificação
                        - **Precisão**: Acurácia geral do modelo
                        
                        ### Interpretação dos Valores:
                        - Valores próximos a 0: Melhor separação entre DLTs
                        - Valores próximos a 1: Maior mistura entre categorias
                        """)
                    gini_fig = create_gini_radar(gini)
                    if gini_fig:
                        st.plotly_chart(gini_fig, use_container_width=True)
                    
                    # Show Entropy Evolution with explanation
                    st.subheader("2. Evolução da Entropia")
                    with st.expander("Ver Explicação da Evolução da Entropia"):
                        st.markdown("""
                        ### O que é a Entropia?
                        A Entropia mede a incerteza na classificação das DLTs ao longo do processo decisório.
                        
                        $Entropia = -\sum_{i=1}^{n} p_i \log_2(p_i)$
                        
                        ### Interpretação do Gráfico:
                        - **Eixo X**: Número de perguntas respondidas
                        - **Eixo Y**: Valor da entropia em bits
                        
                        ### Tendências:
                        - **Diminuição**: Indica maior certeza na decisão
                        - **Aumento**: Indica maior incerteza ou complexidade
                        - **Estabilização**: Indica convergência do processo decisório
                        """)
                    entropy_fig = create_entropy_graph(st.session_state.answers)
                    if entropy_fig:
                        st.plotly_chart(entropy_fig, use_container_width=True)
                    
                    # Show Decision Tree Metrics Dashboard with explanation
                    st.subheader("3. Dashboard de Métricas")
                    with st.expander("Ver Explicação do Dashboard de Métricas"):
                        st.markdown("""
                        ### Métricas do Dashboard:
                        
                        1. **Profundidade da Árvore**
                        - O que é: Número médio de decisões necessárias
                        - Cálculo: $Profundidade = \sum(níveis) / total\_decisões$
                        - Interpretação: Valores menores indicam processo mais direto
                        
                        2. **Taxa de Poda**
                        - O que é: Proporção de simplificação da árvore
                        - Cálculo: $Taxa = (total\_nós - nós\_podados) / total\_nós$
                        - Interpretação: Maior taxa indica melhor otimização
                        
                        3. **Índice de Confiança**
                        - O que é: Medida da confiabilidade da recomendação
                        - Cálculo: $Confiança = (max\_score - mean\_score) / max\_score$
                        - Interpretação: Valores acima de 70% indicam alta confiabilidade
                        """)
                    
                    depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
                    total_nos = len(st.session_state.answers) * 2 + 1
                    nos_podados = total_nos - len(st.session_state.answers) - 1
                    pruning_ratio = calcular_pruning(total_nos, nos_podados)
                    confidence = rec.get('confidence_value', 0.0)
                    
                    metrics_fig = create_metrics_dashboard(depth, pruning_ratio, confidence)
                    if metrics_fig:
                        st.plotly_chart(metrics_fig, use_container_width=True)
        else:
            st.info("Complete o processo de seleção para ver as métricas.")
    except Exception as e:
        st.error(f"Error displaying metrics: {str(e)}")
        st.code(traceback.format_exc())

def main():
    """Main application with improved error handling and state management"""
    try:
        st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
        init_session_state()

        if st.session_state.error:
            show_fallback_ui()
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
                    with st.spinner('Carregando página inicial...'):
                        show_home_page()
                elif menu_option == 'Framework Proposto':
                    with st.spinner('Carregando framework...'):
                        run_decision_tree()
                elif menu_option == 'Métricas':
                    with st.spinner('Carregando métricas...'):
                        show_metrics()
                elif menu_option == 'Perfil':
                    with st.spinner('Carregando perfil...'):
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
                show_fallback_ui()

    except Exception as e:
        st.error(f"Critical error: {str(e)}")
        st.code(traceback.format_exc())
        reset_session_state()

if __name__ == "__main__":
    main()
