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

# Funções de inicialização e gerenciamento de estado
def init_session_state():
    """Initialize all required session state variables with error handling"""
    try:
        if 'initialized' not in st.session_state:
            st.session_state.update({
                'initialized': True,
                'authenticated': False,
                'username': None,
                'page': 'Início',
                'answers': {},
                'error': None,
                'loading': False,
                'recommendation': None
            })
    except Exception as e:
        st.error(f"Error initializing session state: {str(e)}")
        st.session_state.error = str(e)

def reset_session_state():
    """Reset session state on errors"""
    try:
        st.session_state.update({
            'answers': {},
            'error': None,
            'loading': False,
            'recommendation': None
        })
    except Exception as e:
        st.error(f"Error resetting session state: {str(e)}")

# Funções para criar gráficos específicos
def create_gini_radar(gini_data):
    """Creates a radar chart for the Gini metric using Plotly."""
    labels = list(gini_data.keys())
    values = list(gini_data.values())
    values.append(values[0])  # Close the radar chart loop
    labels.append(labels[0])

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name='Gini Index'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=False,
        title="Gini Index Radar Chart"
    )
    return fig

def create_entropy_graph(answers):
    """Create entropy evolution graph with error handling"""
    try:
        entropy_values = []
        weights = {
            "security": 0.4,
            "scalability": 0.25,
            "energy_efficiency": 0.20,
            "governance": 0.15
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

# Funções de exibição de páginas e métricas
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
            'Alta Segurança e Controle', 'Alta Segurança e Descentralização', 
            'Alta Segurança e Descentralização', 'Alta Eficiência Operacional', 
            'Alta Eficiência Operacional', 'Alta Eficiência Operacional', 
            'Escalabilidade e Governança Flexível', 'Escalabilidade e Governança Flexível', 
            'Alta Escalabilidade em Redes IoT'
        ],
        'Tipo DLT': [
            'DLT Permissionada Privada', 'DLT Pública Permissionless', 
            'DLT Pública Permissionless', 'DLT Permissionada Simples', 
            'DLT Permissionada Simples', 'DLT Permissionada Simples', 
            'DLT Híbrida', 'DLT com Consenso Delegado', 'DLT Pública'
        ],
        'Nome DLT': [
            'Hyperledger Fabric', 'Bitcoin', 'Ethereum', 'Quorum', 
            'Quorum', 'VeChain', 'Ethereum 2.0', 'EOS', 'IOTA'
        ],
        'Algoritmo de Consenso': [
            'PBFT', 'PoW', 'PoS (em transição)', 'RAFT', 
            'PoA', 'PoA', 'PoS', 'DPoS', 'Tangle'
        ],
        'Características': [
            'Segurança elevada e resiliência contra falhas bizantinas; ideal para ambientes permissionados.',
            'Segurança máxima e descentralização, ideal para redes abertas.',
            'Transição para PoS, com alta segurança e eficiência energética.',
            'Consenso rápido e ideal para redes permissionadas pequenas.',
            'Consenso baseado em autoridade para redes empresariais.',
            'Controle simplificado para rastreabilidade de cadeias de suprimento.',
            'Escalabilidade e eficiência energética para redes regionais.',
            'Governança flexível e alta performance em redes semi-descentralizadas.',
            'Escalabilidade e dados em tempo real para redes IoT de saúde.'
        ],
        'Estudo de Uso no Setor de Saúde': [
            'Prontuários eletrônicos e integração de dados sensíveis.',
            'Pagamentos descentralizados e dados críticos de saúde pública.',
            'Armazenamento seguro de dados de pacientes.',
            'Redes locais de hospitais e agendamento de pacientes.',
            'Rastreamento de medicamentos e gestão de insumos hospitalares.',
            'Rastreamento de medicamentos e gestão de insumos hospitalares.',
            'Monitoramento de saúde pública e integração de EHRs.',
            'Telemedicina e redes colaborativas de pesquisa.',
            'Monitoramento IoT de dispositivos médicos.'
        ],
        'Casos Reais': [
            'MyClinic. Disponível em: https://www.myclinic.com',
            'MediLedger. Disponível em: https://www.mediledger.com',
            'Patientory. Disponível em: https://www.patientory.com',
            'PharmaLedger. Disponível em: https://www.pharmaledger.eu',
            'PharmaLedger. Disponível em: https://www.pharmaledger.eu',
            'VeChain ToolChain. Disponível em: https://www.vechain.com',
            'Ethereum-based Health Chain. Disponível em: https://ethereum.org',
            'Telos Blockchain. Disponível em: https://www.telos.net',
            'IOTA Healthcare IoT. Disponível em: https://www.iota.org'
        ],
        'Referência ABNT': [
            'MEHMOOD, F.; KHAN, A. Y.; WANG, H.; et al. BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain based on the hyperledger indy. Computer Standards & Interfaces, 2025. DOI: 10.1016/j.csi.2024.103876',
            'POPOOLA, O.; RODRIGUES, M.; MARCHANG, J.; et al. A critical literature review of security and privacy in smart home healthcare schemes adopting IoT & blockchain: Problems, challenges and solutions. Blockchain: Research and Applications, 2024. DOI: 10.1016/j.bcra.2023.100178',
            'AKOH ATADOGA, et al. Blockchain in healthcare: A comprehensive review of applications and security concerns. International Journal of Science and Research Archive, 2024. DOI: 10.30574/ijsra.2024.11.1.0244',
            'DHINGRA, S.; RAUT, R.; NAIK, K.; et al. Blockchain Technology Applications in Healthcare Supply Chains - A Review. IEEE Access, 2024. DOI: 10.1109/ACCESS.2023.3348813',
            'DHINGRA, S.; RAUT, R.; NAIK, K.; et al. Blockchain Technology Applications in Healthcare Supply Chains - A Review. IEEE Access, 2024. DOI: 10.1109/ACCESS.2023.3348813',
            'AL-NBHANY, W. A. N. A.; ZAHARY, A. T.; AL-SHARGABI, A. A. Blockchain-IoT Healthcare Applications and Trends: A Review. IEEE Access, 2024. DOI: 10.1109/ACCESS.2023.3349187',
            'LI, K.; SAI, A. R.; UROVI, V. Do you need a blockchain in healthcare data sharing? A tertiary review. Exploration of Digital Health Technologies, 2024. DOI: 10.37349/edht.2024.00014',
            'ALGHAMDI, T.; KHALID, R.; JAVAID, N. A Survey of Blockchain based Systems: Scalability Issues and Solutions, Applications and Future Challenges. IEEE Access, 2024. DOI: 10.1109/ACCESS.2024.3408868',
            'AL-NBHANY, W. A. N. A.; ZAHARY, A. T.; AL-SHARGABI, A. A. Blockchain-IoT Healthcare Applications and Trends: A Review. IEEE Access, 2024. DOI: 10.1109/ACCESS.2023.3349187'
        ]
    }

    df = pd.DataFrame(data)
    st.table(df)

    if st.button("Iniciar Seleção de DLT", type="primary"):
        st.session_state.page = 'Framework Proposto'
        st.experimental_rerun()

def show_metrics():
    """Exibe métricas do processo de decisão com explicações"""
    st.header("Métricas Técnicas do Processo de Decisão")
    try:
        if 'recommendation' in st.session_state:
            with st.spinner('Carregando métricas...'):
                rec = st.session_state.recommendation
                if 'evaluation_matrix' in rec:
                    classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
                    gini = calcular_gini(classes)
                    entropy = calcular_entropia(classes)

                    st.subheader("1. Índice de Gini")
                    with st.expander("Ver Explicação do Índice de Gini"):
                        st.markdown("""
                            ### O que é o Índice de Gini?
                            O Índice de Gini mede a pureza da classificação das DLTs, representando a variabilidade 
                            entre classes. É calculado como:

                            \\[ Gini = 1 - \sum (p_i)^2 \\]

                            onde \( p_i \) é a proporção de cada classe.
                        """)

                    # Verificação de gini e conversão em dicionário, caso necessário
                    gini_data = gini if isinstance(gini, dict) else {"Gini": gini}
                    gini_fig = create_gini_radar(gini_data)
                    if gini_fig:
                        st.plotly_chart(gini_fig, use_container_width=True)

                    st.subheader("2. Evolução da Entropia")
                    with st.expander("Ver Explicação da Evolução da Entropia"):
                        st.markdown("""
                            ### O que é a Entropia?
                            A Entropia mede a incerteza na classificação das DLTs ao longo do processo decisório. 
                            Calculada como:

                            \\[ Entropia = - \sum p_i \log_2(p_i) \\]

                            onde \( p_i \) é a probabilidade da classe i.
                        """)
                    entropy_fig = create_entropy_graph(st.session_state.answers)
                    if entropy_fig:
                        st.plotly_chart(entropy_fig, use_container_width=True)

                    st.subheader("3. Dashboard de Métricas")
                    with st.expander("Ver Explicação do Dashboard de Métricas"):
                        st.markdown("""
                            ### Métricas do Dashboard:
                            - **Profundidade da Árvore**: Representa a quantidade de níveis do processo de decisão.
                            - **Taxa de Poda**: Calculada como a proporção de nós podados na árvore para simplificar 
                              o modelo, usando:

                              \\[ Taxa\ de\ Poda = \\frac{No\ Podados}{Total\ de\ Nos} \\]

                            - **Índice de Confiança**: Medida de confiança do modelo na recomendação gerada, em %.
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

def show_fallback_ui():
    """Display fallback UI when main content fails to load"""
    st.error("Ocorreu um erro ao carregar o conteúdo")
    if st.button("Tentar Novamente"):
        st.experimental_rerun()

# Funções de exibição para outras páginas de análise e comparação
def show_technical_metrics():
    """Exibe as métricas técnicas de validação do framework proposto com gráficos comparativos"""
    st.header("Métricas Técnicas de Validação do Framework Proposto")
    # Gráficos e tabelas de exemplo para segurança, escalabilidade, etc.

def show_comparative_characteristics():
    """Exibe a comparação das características técnicas e operacionais"""
    st.header("Comparação das Características Técnicas e Operacionais")
    # Exemplo de tabelas e organogramas para características

def show_comparative_scoring():
    """Exibe a pontuação comparativa e validação entre benchmarks"""
    st.header("Pontuação Comparativa e Validação")
    # Gráficos de radar multi-métrico para cada benchmark

def show_discussion_conclusion():
    """Exibe discussão e conclusão da análise de validação científica"""
    st.header("Discussão e Conclusão sobre a Validação Científica")
    # Gráficos de pizza e tabelas de resumo

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
                menu_options = [
                    'Início', 'Framework Proposto', 'Métricas', 'Comparações Benchs',
                    'Métricas Técnicas', 'Comparação de Características', 
                    'Pontuação Comparativa', 'Discussão e Conclusão', 'Perfil', 'Logout'
                ]

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
                elif menu_option == 'Comparações Benchs':
                    with st.spinner('Carregando comparações de benchmarks...'):
                        show_bench_comparisons()
                elif menu_option == 'Métricas Técnicas':
                    with st.spinner('Carregando métricas técnicas...'):
                        show_technical_metrics()
                elif menu_option == 'Comparação de Características':
                    with st.spinner('Carregando comparação de características...'):
                        show_comparative_characteristics()
                elif menu_option == 'Pontuação Comparativa':
                    with st.spinner('Carregando pontuação comparativa...'):
                        show_comparative_scoring()
                elif menu_option == 'Discussão e Conclusão':
                    with st.spinner('Carregando discussão e conclusão...'):
                        show_discussion_conclusion()
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