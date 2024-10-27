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
    """Display metrics with error handling and loading states"""
    st.header("Métricas Técnicas do Processo de Decisão")
    
    try:
        if 'recommendation' in st.session_state:
            with st.spinner('Carregando métricas...'):
                rec = st.session_state.recommendation
                if 'evaluation_matrix' in rec:
                    classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
                    gini = calcular_gini(classes)
                    entropy = calcular_entropia(classes)
                    
                    # Gini Index Section with Explanation
                    with st.expander("1. Índice de Gini - Detalhes e Interpretação"):
                        st.markdown("""
                        ### Fórmula do Índice de Gini
                        $Gini = 1 - \sum_{i=1}^{n} p_i^2$
                        
                        Onde:
                        - $p_i$ é a proporção de cada classe no conjunto
                        - Valores próximos a 0 indicam melhor separação
                        - Valores próximos a 1 indicam maior mistura
                        
                        #### Interpretação:
                        - 0.0 - 0.3: Excelente separação entre classes
                        - 0.3 - 0.6: Separação moderada
                        - 0.6 - 1.0: Alta mistura entre classes
                        """)
                        gini_fig = create_gini_radar(gini)
                        if gini_fig:
                            st.plotly_chart(gini_fig, use_container_width=True)
                    
                    # Entropy Section with Explanation
                    with st.expander("2. Entropia - Detalhes e Interpretação"):
                        st.markdown("""
                        ### Fórmula da Entropia
                        $Entropia = -\sum_{i=1}^{n} p_i \log_2(p_i)$
                        
                        Onde:
                        - $p_i$ é a probabilidade de cada classe
                        - Logaritmo na base 2 é usado para medir em bits
                        - Menor entropia indica maior certeza na decisão
                        
                        #### Interpretação:
                        - 0.0 - 1.0: Alta certeza na decisão
                        - 1.0 - 2.0: Certeza moderada
                        - > 2.0: Alta incerteza na decisão
                        """)
                        entropy_fig = create_entropy_graph(st.session_state.answers)
                        if entropy_fig:
                            st.plotly_chart(entropy_fig, use_container_width=True)
                    
                    # Decision Tree Metrics Dashboard with Explanation
                    with st.expander("3. Métricas da Árvore de Decisão - Detalhes e Interpretação"):
                        st.markdown("""
                        ### Profundidade da Árvore
                        $Profundidade = \frac{\sum_{i=1}^{n} nivel_i}{n}$
                        - Mede a complexidade média do processo decisório
                        - Valores menores indicam processo mais simples
                        
                        ### Taxa de Poda
                        $Taxa_{poda} = \frac{nos_{total} - nos_{podados}}{nos_{total}}$
                        - Indica eficiência na simplificação do modelo
                        - Maior taxa indica modelo mais otimizado
                        
                        ### Índice de Confiança
                        $Confianca = \frac{max_{score} - mean_{score}}{max_{score}}$
                        - Mede a confiabilidade da recomendação
                        - Valores > 0.7 indicam alta confiabilidade
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

def show_home_page():
    """Display home page with reference table"""
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao sistema de seleção de DLT para projetos de saúde.")
    
    st.markdown("## Referência de DLTs e Algoritmos")
    
    # Load and display reference table
    reference_data = {
        'DLT': [
            'Hyperledger Fabric', 'Corda', 'Quorum', 'VeChain', 'IOTA',
            'Ripple (XRP Ledger)', 'Stellar', 'Bitcoin', 'Ethereum (PoW)',
            'Ethereum 2.0 (PoS)'
        ],
        'Tipo de DLT': [
            'DLT Permissionada Privada', 'DLT Permissionada Simples', 'DLT Híbrida',
            'DLT Híbrida', 'DLT com Consenso Delegado', 'DLT com Consenso Delegado',
            'DLT com Consenso Delegado', 'DLT Pública', 'DLT Pública',
            'DLT Pública Permissionless'
        ],
        'Grupo de Algoritmo': [
            'Alta Segurança e Controle dos dados sensíveis',
            'Alta Segurança e Controle dos dados sensíveis',
            'Escalabilidade e Governança Flexível',
            'Alta Eficiência Operacional em redes locais',
            'Alta Escalabilidade em Redes IoT',
            'Alta Eficiência Operacional em redes locais',
            'Alta Eficiência Operacional em redes locais',
            'Alta Segurança e Descentralização de dados críticos',
            'Alta Segurança e Descentralização de dados críticos',
            'Escalabilidade e Governança Flexível'
        ],
        'Algoritmo de Consenso': [
            'RAFT/IBFT', 'RAFT', 'RAFT/IBFT', 'PoA', 'Tangle',
            'Ripple Consensus Algorithm', 'SCP', 'PoW', 'PoW', 'PoS'
        ],
        'Principais Características': [
            'Alta tolerância a falhas, consenso rápido em ambientes permissionados',
            'Consenso baseado em líderes, adequado para redes privadas',
            'Flexibilidade de governança, consenso eficiente para redes híbridas',
            'Alta eficiência, baixa latência, consenso delegado a validadores autorizados',
            'Escalabilidade alta, arquitetura sem blocos, adequada para IoT',
            'Consenso rápido, baixa latência, baseado em validadores confiáveis',
            'Consenso baseado em quórum, alta eficiência, tolerância a falhas',
            'Segurança alta, descentralização, consumo elevado de energia',
            'Segurança alta, descentralização, escalabilidade limitada, alto custo',
            'Eficiência energética, incentivo à participação, redução da centralização'
        ],
        'Estudos de Uso': [
            'Guardtime: Aplicado em sistemas de saúde da Estônia',
            'ProCredEx: Validação de credenciais de profissionais de saúde nos EUA',
            'Chronicled (Mediledger Project): Rastreamento de medicamentos',
            'FarmaTrust: Rastreamento de medicamentos e combate à falsificação',
            'Patientory: Compartilhamento de dados de pacientes via IoT',
            'Change Healthcare: Gestão de ciclo de receita',
            'MedicalChain: Controle de dados e consultas telemédicas',
            'Guardtime: Rastreamento de dados de saúde em redes públicas',
            'Embleema: Desenvolvimento de medicamentos e ensaios clínicos',
            'MTBC: Gestão de registros eletrônicos de saúde (EHR)'
        ]
    }
    
    df = pd.DataFrame(reference_data)
    
    # Display table with individual rows for better readability
    for _, row in df.iterrows():
        with st.expander(f"{row['DLT']} ({row['Tipo de DLT']})"):
            st.markdown(f"""
            **Grupo de Algoritmo:** {row['Grupo de Algoritmo']}  
            **Algoritmo de Consenso:** {row['Algoritmo de Consenso']}  
            **Principais Características:** {row['Principais Características']}  
            **Estudo de Uso:** {row['Estudos de Uso']}
            """)

def show_benchmarks():
    """Display benchmarks comparison page"""
    st.title("Comparação de Benchmarks")
    
    # Performance Metrics Comparison
    st.header("1. Métricas de Desempenho")
    performance_metrics = {
        'DLT': ['Hyperledger Fabric', 'Bitcoin', 'Ethereum', 'Quorum', 'VeChain', 'IOTA'],
        'TPS': [3000, 7, 15, 1000, 2000, 1000],
        'Latência (s)': [1, 600, 15, 2, 10, 60],
        'Consumo Energético': ['Baixo', 'Muito Alto', 'Alto', 'Baixo', 'Baixo', 'Muito Baixo'],
        'Escalabilidade': ['Alta', 'Baixa', 'Média', 'Alta', 'Alta', 'Muito Alta']
    }
    
    df_performance = pd.DataFrame(performance_metrics)
    
    # Create performance visualization
    fig_performance = go.Figure(data=[
        go.Bar(name='TPS', x=df_performance['DLT'], y=df_performance['TPS']),
        go.Bar(name='Latência', x=df_performance['DLT'], y=df_performance['Latência (s)'])
    ])
    
    fig_performance.update_layout(
        title="Comparação de Desempenho",
        barmode='group'
    )
    
    st.plotly_chart(fig_performance)
    
    # Use Cases Comparison
    st.header("2. Comparação de Casos de Uso")
    with st.expander("Registros Médicos Eletrônicos (EMR)"):
        st.markdown("""
        - **Hyperledger Fabric**: Ideal para EMR devido à privacidade e controle de acesso
        - **Ethereum 2.0**: Bom para interoperabilidade entre diferentes sistemas
        - **Quorum**: Excelente para consórcios de hospitais
        """)
    
    with st.expander("Cadeia de Suprimentos Farmacêutica"):
        st.markdown("""
        - **VeChain**: Especializada em rastreamento de medicamentos
        - **Hyperledger Fabric**: Forte em gestão de cadeia de suprimentos
        - **IOTA**: Ótima para integração com IoT
        """)
    
    with st.expander("Compartilhamento de Dados de Pesquisa"):
        st.markdown("""
        - **Ethereum 2.0**: Bom para compartilhamento público de dados
        - **Quorum**: Ideal para consórcios de pesquisa
        - **Stellar**: Eficiente para transações entre instituições
        """)
    
    # Implementation Examples
    st.header("3. Exemplos de Implementação")
    implementation_data = {
        'Projeto': ['Guardtime', 'MedicalChain', 'FarmaTrust', 'Patientory'],
        'DLT': ['Hyperledger Fabric', 'Ethereum', 'VeChain', 'IOTA'],
        'País': ['Estônia', 'Reino Unido', 'Global', 'EUA'],
        'Escala': ['Nacional', 'Regional', 'Global', 'Regional'],
        'Status': ['Produção', 'Piloto', 'Produção', 'Produção']
    }
    
    df_implementation = pd.DataFrame(implementation_data)
    st.dataframe(df_implementation)
    
    # Academic Validation Scores
    st.header("4. Validação Acadêmica")
    academic_scores = {
        'DLT': ['Hyperledger Fabric', 'Ethereum 2.0', 'IOTA', 'VeChain'],
        'Score Acadêmico': [4.5, 4.2, 4.3, 4.0],
        'Citações': [128, 95, 89, 76],
        'Estudos Validados': [15, 12, 10, 8]
    }
    
    df_academic = pd.DataFrame(academic_scores)
    
    fig_academic = go.Figure(data=[
        go.Scatter(
            x=df_academic['DLT'],
            y=df_academic['Score Acadêmico'],
            mode='lines+markers',
            name='Score Acadêmico'
        )
    ])
    
    fig_academic.update_layout(
        title="Scores de Validação Acadêmica",
        yaxis_range=[0, 5]
    )
    
    st.plotly_chart(fig_academic)

def show_fallback_ui():
    """Display fallback UI when main content fails to load"""
    st.error("Ocorreu um erro ao carregar o conteúdo")
    if st.button("Tentar Novamente"):
        st.experimental_rerun()

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
                menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Comparação de Benchs', 'Perfil', 'Logout']
                
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
                elif menu_option == 'Comparação de Benchs':
                    with st.spinner('Carregando comparações...'):
                        show_benchmarks()
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
