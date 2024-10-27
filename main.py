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

def show_reference_table():
    """Display reference table of DLT types and algorithms"""
    st.subheader("Tabela de Referência de DLTs e Algoritmos")
    
    data = {
        'Grupo': [
            'Alta Segurança e Controle',
            'Alta Segurança e Controle',
            'Alta Eficiência Operacional',
            'Escalabilidade e Governança Flexível',
            'Alta Escalabilidade em Redes IoT',
            'Alta Segurança e Descentralização'
        ],
        'Tipo DLT': [
            'DLT Permissionada Privada',
            'DLT Pública Permissionless',
            'DLT Permissionada Simples',
            'DLT Híbrida',
            'DLT com Consenso Delegado',
            'DLT Pública'
        ],
        'Exemplo': [
            'Hyperledger Fabric',
            'Bitcoin',
            'Quorum',
            'Ethereum 2.0',
            'IOTA',
            'Ethereum'
        ],
        'Algoritmo de Consenso': [
            'PBFT',
            'PoW',
            'RAFT/PoA',
            'PoS',
            'Tangle',
            'PoW/PoS'
        ],
        'Caso de Uso em Saúde': [
            'Prontuários Eletrônicos',
            'Dados Críticos de Saúde',
            'Sistemas Locais',
            'Redes Regionais',
            'IoT Médico',
            'Ensaios Clínicos'
        ]
    }
    
    df = pd.DataFrame(data)
    st.table(df)

def create_gini_radar(gini):
    """Create Gini index radar visualization with error handling"""
    try:
        categories = ['Separação de Classes', 'Pureza dos Dados', 'Consistência', 'Precisão']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[1-gini, gini, 1-gini, gini],
            theta=categories,
            fill='toself',
            name='Índice de Gini'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title="Análise do Índice de Gini"
        )
        return fig
    except Exception as e:
        st.error(f"Error creating Gini radar: {str(e)}")
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
                        st.title("SeletorDLTSaude")
                        st.write("Bem-vindo ao sistema de seleção de DLT para saúde.")
                        show_reference_table()
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
