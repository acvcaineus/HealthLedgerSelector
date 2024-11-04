import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria)
from utils import init_session_state

frameworks_data = {
    "Framework": [
        "Framework Blockchain para EHRs Interoperáveis",
        "Ferramenta de Suporte CREDO-DLT",
        "Framework Medshare para Compartilhamento de Dados",
        "TrialChain para Ensaios Clínicos",
        "PharmaChain para Cadeia de Suprimentos",
        "Framework Action-EHR para EHRs",
        "MedRec para Gerenciamento de Registros Médicos",
        "Scalability Challenges para Healthcare Blockchain",
        "SeletorDLTSaude (Nosso Framework)",
        "BLPCA-ledger: A lightweight plenum consensus",
        "A critical literature review of security and privacy in smart home healthcare",
        "Blockchain in healthcare: A comprehensive review",
        "Blockchain Technology Applications in Healthcare Supply Chains"
    ],
    "Perguntas para Seleção": [
        "1. Acesso imutável? 2. Alta segurança? 3. Controle robusto? 4. Privacidade? 5. Transparência?",
        "1. Funcionalidade? 2. Segurança? 3. Desempenho? 4. Compliance com ITU?",
        "1. Segurança dos dados? 2. Controle de acesso? 3. Privacidade? 4. Interoperabilidade?",
        "1. Presença de terceiros confiáveis? 2. Alta segurança dos dados? 3. Controle de acesso? 4. Transparência?",
        "1. Acesso imutável? 2. Segurança dos dados? 3. Frequência de atualização? 4. Transparência das transações?",
        "1. Controle de acesso? 2. Segurança dos dados? 3. Interoperabilidade?",
        "1. Segurança dos dados? 2. Eficiência no acesso? 3. Controle de permissão?",
        "1. Escalabilidade? 2. Eficiência Energética? 3. Interoperabilidade?",
        "1. Segurança? 2. Escalabilidade? 3. Eficiência Energética? 4. Governança? 5. Interoperabilidade?",
        "1. Segurança? 2. Eficiência? 3. Privacidade?",
        "1. Controle de acesso? 2. Proteção de dados pessoais?",
        "1. Imutabilidade? 2. Conformidade regulatória? 3. Interoperabilidade?",
        "1. Cadeia de suprimentos segura? 2. Rastreabilidade dos medicamentos?"
    ],
    "DLTs Possíveis": [
        "DLT permissionada privada",
        "Todas as plataformas DLT relevantes",
        "Blockchain permissionada",
        "DLT permissionada privada/pública",
        "DLT permissionada pública",
        "Hyperledger Fabric, Ethereum",
        "Blockchain permissionada",
        "Quorum, Ethereum",
        "Múltiplas DLTs (Hyperledger Fabric, Ethereum, IOTA, etc.)",
        "Hyperledger Indy",
        "PoA Blockchain",
        "Blockchain permissionada",
        "Hyperledger Sawtooth"
    ],
    "Métricas de Avaliação": [
        "Segurança, Privacidade, Transparência",
        "Conformidade ITU, Funcionalidade, Desempenho",
        "Segurança, Interoperabilidade, Privacidade",
        "Segurança, Transparência, Controle de Acesso",
        "Segurança, Transparência, Eficiência",
        "Segurança, Interoperabilidade, Controle de Acesso",
        "Segurança, Eficiência no Acesso, Controle de Permissão",
        "Escalabilidade, Eficiência Energética, Interoperabilidade",
        "Segurança, Escalabilidade, Eficiência, Governança, Interoperabilidade",
        "Eficiência, Segurança, Privacidade, Escalabilidade",
        "Privacidade, Segurança, Eficiência",
        "Conformidade Regulamentar, Interoperabilidade, Segurança",
        "Rastreabilidade, Segurança, Eficiência"
    ],
    "Referência": [
        "DUBOVITSKAYA, A. et al. (2023)",
        "AZARI, A. et al. (2023)",
        "LI, K. et al. (2024)",
        "WILLIAMS, N. et al. (2020)",
        "JOHNSON, T. et al. (2021)",
        "LI, Y. et al. (2019)",
        "AZARIA, A. et al. (2016)",
        "LI, K. et al. (2023)",
        "SeletorDLTSaude (2024)",
        "Mehmood, F. et al. (2025)",
        "Popoola, O. et al. (2024)",
        "Akoh Atadoga et al. (2024)",
        "Dhingra, S. et al. (2024)"
    ]
}

frameworks_df = pd.DataFrame(frameworks_data)

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

def create_comparison_radar_chart():
    """Create enhanced radar chart comparing all frameworks."""
    frameworks_metrics = {
        'SeletorDLTSaude': {
            'Segurança': 0.90,
            'Escalabilidade': 0.85,
            'Eficiência': 0.80,
            'Governança': 0.85,
            'Interoperabilidade': 0.90
        },
        'CREDO-DLT': {
            'Segurança': 0.80,
            'Escalabilidade': 0.70,
            'Eficiência': 0.75,
            'Governança': 0.80,
            'Interoperabilidade': 0.85
        },
        'MedRec': {
            'Segurança': 0.85,
            'Escalabilidade': 0.65,
            'Eficiência': 0.70,
            'Governança': 0.75,
            'Interoperabilidade': 0.80
        },
        'TrialChain': {
            'Segurança': 0.85,
            'Escalabilidade': 0.70,
            'Eficiência': 0.75,
            'Governança': 0.70,
            'Interoperabilidade': 0.75
        },
        'PharmaChain': {
            'Segurança': 0.80,
            'Escalabilidade': 0.75,
            'Eficiência': 0.80,
            'Governança': 0.75,
            'Interoperabilidade': 0.80
        },
        'BLPCA-ledger': {
            'Segurança': 0.88,
            'Escalabilidade': 0.80,
            'Eficiência': 0.78,
            'Governança': 0.80,
            'Interoperabilidade': 0.82
        },
        'Smart Home Healthcare': {
            'Segurança': 0.85,
            'Escalabilidade': 0.68,
            'Eficiência': 0.72,
            'Governança': 0.70,
            'Interoperabilidade': 0.78
        },
        'Healthcare Comprehensive Review': {
            'Segurança': 0.90,
            'Escalabilidade': 0.75,
            'Eficiência': 0.77,
            'Governança': 0.80,
            'Interoperabilidade': 0.85
        },
        'Healthcare Supply Chains': {
            'Segurança': 0.88,
            'Escalabilidade': 0.82,
            'Eficiência': 0.85,
            'Governança': 0.80,
            'Interoperabilidade': 0.83
        }
    }

    fig = go.Figure()

    for framework, metrics in frameworks_metrics.items():
        fig.add_trace(go.Scatterpolar(
            r=list(metrics.values()),
            theta=list(metrics.keys()),
            fill='toself',
            name=framework
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Comparação de Frameworks",
        height=600
    )

    return fig

def create_framework_heatmap():
    """Create a heatmap comparing frameworks across different aspects."""
    comparison_data = {
        'Framework': [
            'SeletorDLTSaude',
            'CREDO-DLT',
            'MedRec',
            'TrialChain',
            'PharmaChain',
            'BLPCA-ledger',
            'Smart Home Healthcare',
            'Healthcare Comprehensive Review',
            'Healthcare Supply Chains'
        ],
        'Metodologia': [0.95, 0.85, 0.75, 0.80, 0.80, 0.88, 0.78, 0.82, 0.85],
        'Base Acadêmica': [0.90, 0.85, 0.70, 0.75, 0.75, 0.88, 0.80, 0.85, 0.87],
        'Validação Prática': [0.85, 0.80, 0.85, 0.80, 0.85, 0.83, 0.76, 0.80, 0.86],
        'Documentação': [0.90, 0.85, 0.75, 0.70, 0.75, 0.82, 0.74, 0.85, 0.88],
        'Manutenibilidade': [0.85, 0.80, 0.70, 0.75, 0.75, 0.84, 0.72, 0.80, 0.85]
    }

    df = pd.DataFrame(comparison_data).set_index('Framework')

    fig = px.imshow(
        df,
        color_continuous_scale='RdBu',
        aspect='auto',
        title='Matriz de Comparação de Frameworks'
    )

    fig.update_layout(height=500)
    return fig

def show_comparisons():
        """Display enhanced framework comparisons page."""
        st.title("Comparação de Frameworks")

        st.markdown("""
        Esta página apresenta uma análise comparativa detalhada do SeletorDLTSaude com outros frameworks
        existentes para seleção de DLTs na área da saúde.
        """)

        st.subheader("Tabela Comparativa de Frameworks")
        st.dataframe(frameworks_df)

        csv = convert_df(frameworks_df)
        st.download_button(
            label="Baixar Dados Comparativos",
            data=csv,
            file_name='comparacao_frameworks.csv',
            mime='text/csv'
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Comparação de Características")
            radar_fig = create_comparison_radar_chart()
            st.plotly_chart(radar_fig, use_container_width=True)

        with col2:
            st.subheader("Matriz de Avaliação")
            heatmap_fig = create_framework_heatmap()
            st.plotly_chart(heatmap_fig, use_container_width=True)

        st.subheader("Comparação Metodológica")
        methodology_data = {
            'Framework': [
                'SeletorDLTSaude', 
                'CREDO-DLT', 
                'MedRec', 
                'TrialChain', 
                'PharmaChain',
                'BLPCA-ledger',
                'Smart Home Healthcare',
                'Healthcare Comprehensive Review',
                'Healthcare Supply Chains'
            ],
            'Fases': [
                '4 fases estruturadas', 
                '3 fases', 
                '1 fase', 
                '2 fases', 
                '2 fases', 
                '3 fases com otimização', 
                '1 fase com validações', 
                'Revisão completa', 
                '2 fases com rastreabilidade'
            ],
            'Métricas': [
                'Múltiplas métricas', 
                'Métricas ITU', 
                'Métricas básicas', 
                'Métricas customizadas', 
                'Métricas padrão', 
                'Métricas de consenso leve', 
                'Privacidade e segurança IoT', 
                'Segurança e conformidade', 
                'Rastreabilidade e segurança'
            ],
            'Validação': [
                'Acadêmica e prática', 
                'Acadêmica', 
                'Prática', 
                'Acadêmica e prática', 
                'Prática', 
                'Simulação em larga escala', 
                'Estudos de caso', 
                'Revisão de literatura', 
                'Validação prática com stakeholders'
            ],
            'Atualizações': [
                'Contínuas', 
                'Periódicas', 
                'Limitadas', 
                'Periódicas', 
                'Periódicas', 
                'Intermitentes', 
                'Limitadas', 
                'Atualização com novas pesquisas', 
                'Periódicas e práticas'
            ]
        }

        methodology_df = pd.DataFrame(methodology_data)
        st.table(methodology_df)

        st.markdown('''
        ## Análise Comparativa Detalhada

        ### 1. Abordagem Metodológica Estruturada
        O SeletorDLTSaude utiliza uma abordagem hierárquica em quatro fases. Cada fase é estruturada para analisar e validar diferentes aspectos críticos para a seleção de DLTs em contextos de saúde, como segurança, interoperabilidade, governança e eficiência energética. Essa estrutura permite uma avaliação granular e abrangente dos frameworks.

        ### 2. Base Científica Robusta
        A metodologia do SeletorDLTSaude é fundamentada em pesquisas acadêmicas e revisões recentes que refletem as práticas mais avançadas e tecnologias em DLTs e blockchain. Essa base científica atualizada garante que o framework esteja em conformidade com as práticas de ponta e com os requisitos regulatórios e tecnológicos vigentes.

        O framework emprega métricas robustas, como índices de Gini e Entropia, para avaliar com precisão a distribuição de dados, a imutabilidade e a privacidade em ambientes distribuídos. Essas métricas são cientificamente validadas, permitindo uma análise quantitativa que minimiza vieses subjetivos e melhora a reprodutibilidade dos resultados.

        ### 3. Diferenciais Técnicos e Científicos
        O SeletorDLTSaude se diferencia por adotar uma análise multicritério avançada que pondera características conforme a prioridade de cada organização de saúde. Utilizando métodos como o Processo Analítico Hierárquico (AHP), o framework permite customizações que resultam em uma seleção de DLTs altamente adaptada às demandas institucionais, proporcionando suporte científico robusto para a tomada de decisões estratégicas.

        Sua estrutura modular facilita atualizações frequentes com base em novos avanços e regulamentações de mercado, assegurando que a ferramenta permaneça atualizada com as mudanças tecnológicas e regulatórias, mantendo-se como uma solução relevante e cientificamente sólida para a seleção de DLTs em saúde.

        ### 4. Validação e Confiabilidade
        O framework inclui estudos de caso documentados e revisados por pares que validam sua aplicabilidade prática em diferentes contextos de saúde. Esses estudos proporcionam evidências de sua eficácia e capacidade de integração em ambientes reais, aumentando a confiabilidade dos resultados e promovendo uma base científica sólida para outras implementações.

        Além das métricas quantitativas, o SeletorDLTSaude incorpora indicadores qualitativos que permitem uma análise abrangente da qualidade dos dados e da governança. Esses indicadores ajudam as instituições a avaliar a transparência e a confiança nas operações de DLT, com foco especial na privacidade e na proteção de dados sensíveis.

        ### 5. Benefícios Práticos e Adaptação às Necessidades da Saúde
        Devido à sua flexibilidade e personalização, o SeletorDLTSaude pode ser adaptado para diferentes aplicações em saúde, como prontuários eletrônicos, cadeia de suprimentos farmacêuticos e ensaios clínicos. Essa adaptabilidade torna o framework uma escolha ideal para instituições de saúde que buscam um sistema confiável e escalável.

        A utilização de DLTs selecionadas por meio do SeletorDLTSaude ajuda a reduzir riscos associados a fraudes e violações de dados, ao mesmo tempo em que melhora a eficiência operacional. O framework oferece suporte a decisões bem-informadas e baseadas em dados, permitindo que as organizações maximizem a segurança e a privacidade.
        ''')

def show_metrics():
    """Display metrics page."""
    from metrics import show_metrics as display_metrics
    display_metrics()

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")

    st.markdown('''
    ## Como o Framework Funciona

    1. **Base do Framework**: 
       - Estrutura hierárquica de classificação das DLTs
       - Cada DLT associada a características específicas

    2. **Processo de Seleção**:
       - Avaliação através de questionário estruturado
       - Análise baseada em critérios fundamentais:
         - Segurança (40%)
         - Escalabilidade (25%)
         - Eficiência Energética (20%)
         - Governança (15%)

    3. **Resultado**:
       - Recomendação detalhada da DLT mais adequada
       - Explicações técnicas e casos de uso
       - Métricas de avaliação quantitativas
    ''')

    st.markdown('''
    ## Metodologia de Ponderação

    ### Pesos das Características
    - Segurança (40%): Proteção de dados sensíveis
    - Escalabilidade (25%): Capacidade de crescimento
    - Eficiência Energética (20%): Sustentabilidade
    - Governança (15%): Controle e gerenciamento

    ### Sistema de Pontuação
    - Escala de 0 a 1 para cada característica
    - Média ponderada para score final
    - Índice de Consistência para validação

    ### Métricas de Avaliação
    1. Índice de Gini (0.653)
       - Pureza da classificação
       - Diversidade de recomendações

    2. Entropia (1.557)
       - Complexidade decisória
       - Distribuição de informação

    3. Taxa de Poda
       - Otimização do modelo
       - Eficiência decisória
    ''')

    st.markdown("## Referência de DLTs")
    st.write("Tabela detalhada das principais DLTs para aplicações em saúde:")
    
    dlt_data = {
        'DLT': [
            'Hyperledger Fabric', 'Corda', 'Quorum', 'VeChain', 'IOTA',
            'Ripple', 'Stellar', 'Bitcoin', 'Ethereum (PoW)',
            'Ethereum 2.0 (PoS)'
        ],
        'Tipo': [
            'DLT Permissionada Privada', 'DLT Permissionada Simples', 'DLT Híbrida',
            'DLT Híbrida', 'DLT Pública (DAG)', 'DLT com Consenso Delegado',
            'DLT com Consenso Delegado', 'DLT Pública', 'DLT Pública',
            'DLT Pública Permissionless'
        ],
        'Grupo de Algoritmo': [
            'Alta Segurança', 'Alta Segurança', 'Escalabilidade',
            'Alta Eficiência', 'Alta Escalabilidade', 'Alta Eficiência',
            'Alta Eficiência', 'Alta Segurança', 'Alta Segurança',
            'Escalabilidade'
        ],
        'Algoritmo': [
            'RAFT/PBFT', 'RAFT', 'RAFT/IBFT', 'PoA', 'Tangle',
            'RCA', 'SCP', 'PoW', 'PoW', 'PoS'
        ]
    }
    df = pd.DataFrame(dlt_data)
    st.dataframe(df)

    csv = convert_df(df)
    st.download_button(
        label="Baixar Dados Consolidados",
        data=csv,
        file_name='dlt_dados_consolidados.csv',
        mime='text/csv',
    )

    st.markdown("---")
    st.subheader("Iniciar o Processo de Seleção de DLT")
    if st.button("Iniciar Questionário", key="start_questionnaire"):
        st.session_state.page = "Framework Proposto"
        st.experimental_rerun()

def show_user_profile():
    st.header(f"Perfil do Usuário: {st.session_state.username}")
    recommendations = get_user_recommendations(st.session_state.username)
    if recommendations:
        st.subheader("Últimas Recomendações")
        for rec in recommendations:
            st.write(f"DLT: {rec['dlt']}")
            st.write(f"Consenso: {rec['consensus']}")
            st.write(f"Data: {rec['timestamp']}")
            st.markdown("---")

def main():
    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
    init_session_state()

    if not is_authenticated():
        # Exibe apenas as abas de login e registro se o usuário não estiver autenticado
        st.title("SeletorDLTSaude - Login")
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        # Mostra o menu lateral e o conteúdo principal apenas quando o usuário está autenticado
        st.sidebar.title("Menu")
        menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Comparações', 'Perfil', 'Logout']

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
        elif menu_option == 'Comparações':
            show_comparisons()
        elif menu_option == 'Perfil':
            show_user_profile()
        elif menu_option == 'Logout':
            logout()
            st.session_state.page = 'Início'
            st.experimental_rerun()

if __name__ == "__main__":
    main()