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

# Framework comparison data
frameworks_data = {
    "Framework": [
        "Framework Blockchain para EHRs Interoperáveis",
        "Ferramenta de Suporte CREDO-DLT",
        "Framework Medshare para Compartilhamento de Dados",
        "TrialChain para Ensaios Clínicos",
        "PharmaChain para Cadeia de Suprimentos",
        "Framework Action-EHR para EHRs",
        "MedRec para Gerenciamento de Registros Médicos",
        "SeletorDLTSaude (Nosso Framework)"
    ],
    "Perguntas para Seleção": [
        "1. Acesso imutável? 2. Alta segurança? 3. Controle robusto? 4. Privacidade? 5. Transparência?",
        "1. Funcionalidade? 2. Segurança? 3. Desempenho? 4. Compliance com ITU?",
        "1. Segurança dos dados? 2. Controle de acesso? 3. Privacidade? 4. Interoperabilidade?",
        "1. Presença de terceiros confiáveis? 2. Alta segurança dos dados? 3. Controle de acesso? 4. Transparência?",
        "1. Acesso imutável? 2. Segurança dos dados? 3. Frequência de atualização? 4. Transparência das transações?",
        "1. Controle de acesso? 2. Segurança dos dados? 3. Interoperabilidade?",
        "1. Segurança dos dados? 2. Eficiência no acesso? 3. Controle de permissão?",
        "1. Segurança? 2. Escalabilidade? 3. Eficiência Energética? 4. Governança? 5. Interoperabilidade?"
    ],
    "DLTs Possíveis": [
        "DLT permissionada privada",
        "Todas as plataformas DLT relevantes",
        "Blockchain permissionada",
        "DLT permissionada privada/pública",
        "DLT permissionada pública",
        "Hyperledger Fabric, Ethereum",
        "Blockchain permissionada",
        "Múltiplas DLTs (Hyperledger Fabric, Ethereum, IOTA, etc.)"
    ]
}

frameworks_df = pd.DataFrame(frameworks_data)

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

def create_comparison_radar_chart():
    """Create radar chart comparing frameworks."""
    frameworks_metrics = {
        'SeletorDLTSaude': {
            'Segurança': 0.9,
            'Escalabilidade': 0.85,
            'Eficiência': 0.8,
            'Governança': 0.85,
            'Interoperabilidade': 0.9
        },
        'CREDO-DLT': {
            'Segurança': 0.8,
            'Escalabilidade': 0.7,
            'Eficiência': 0.75,
            'Governança': 0.8,
            'Interoperabilidade': 0.85
        },
        'MedRec': {
            'Segurança': 0.85,
            'Escalabilidade': 0.65,
            'Eficiência': 0.7,
            'Governança': 0.75,
            'Interoperabilidade': 0.8
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
        title="Comparação de Frameworks"
    )
    
    return fig

def show_comparisons():
    """Display framework comparisons page."""
    st.title("Comparação de Frameworks")
    
    st.markdown("""
    Esta página apresenta uma análise comparativa do SeletorDLTSaude com outros frameworks
    existentes para seleção de DLTs na área da saúde.
    """)
    
    # Framework comparison table
    st.subheader("Tabela Comparativa de Frameworks")
    st.dataframe(frameworks_df)
    
    # Download button for comparison data
    csv = convert_df(frameworks_df)
    st.download_button(
        label="Baixar Dados Comparativos",
        data=csv,
        file_name='comparacao_frameworks.csv',
        mime='text/csv'
    )
    
    # Radar chart comparison
    st.subheader("Comparação Visual de Características")
    fig = create_comparison_radar_chart()
    st.plotly_chart(fig, use_container_width=True)
    
    # Side-by-side metrics comparison
    st.subheader("Comparação de Métricas")
    metrics_comparison = pd.DataFrame({
        'Métrica': ['Segurança', 'Escalabilidade', 'Eficiência', 'Governança', 'Interoperabilidade'],
        'SeletorDLTSaude': [0.9, 0.85, 0.8, 0.85, 0.9],
        'CREDO-DLT': [0.8, 0.7, 0.75, 0.8, 0.85],
        'MedRec': [0.85, 0.65, 0.7, 0.75, 0.8]
    })
    
    fig_metrics = px.bar(
        metrics_comparison,
        x='Métrica',
        y=['SeletorDLTSaude', 'CREDO-DLT', 'MedRec'],
        barmode='group',
        title='Comparação de Métricas entre Frameworks'
    )
    st.plotly_chart(fig_metrics)
    
    # Methodology comparison
    st.subheader("Comparação Metodológica")
    methodology_data = {
        'Framework': ['SeletorDLTSaude', 'CREDO-DLT', 'MedRec'],
        'Fases': ['4 fases', '3 fases', '1 fase'],
        'Métricas': ['Múltiplas métricas', 'Métricas ITU', 'Métricas básicas'],
        'Validação': ['Acadêmica e prática', 'Acadêmica', 'Prática']
    }
    
    methodology_df = pd.DataFrame(methodology_data)
    st.table(methodology_df)
    
    # Add conclusion section
    st.markdown('''
    ## Conclusão da Análise Comparativa

    O SeletorDLTSaude se destaca dos demais frameworks pelos seguintes diferenciais:

    1. **Abordagem Hierárquica**: 
       - Único framework que considera a estrutura hierárquica completa (DLT → Tipo → Grupo → Algoritmo)
       - Permite recomendações mais precisas e contextualizadas

    2. **Base Científica Atualizada**: 
       - Referencias acadêmicas recentes (2024-2025)
       - Validação por estudos de caso reais em saúde

    3. **Métricas Quantitativas**:
       - Sistema de pontuação baseado em evidências
       - Índice de consistência para validar recomendações

    4. **Flexibilidade e Adaptabilidade**:
       - Suporte a múltiplos cenários de saúde
       - Atualização contínua da base de conhecimento

    5. **Transparência na Decisão**:
       - Explicações detalhadas em cada etapa
       - Visualizações interativas das métricas
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

    # New section for scoring methodology
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
    
    # Reference table data
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
        st.title("SeletorDLTSaude - Login")
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
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
