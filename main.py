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

def create_metrics_radar_chart(gini, entropy, depth, pruning):
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[gini, entropy, depth, pruning],
        theta=['Índice de Gini', 'Entropia', 'Profundidade', 'Taxa de Poda'],
        fill='toself',
        name='Métricas Atuais',
        hovertemplate="<b>%{theta}</b><br>" +
                     "Valor: %{r:.3f}<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        title="Visão Geral das Métricas",
        showlegend=True
    )
    return fig

def create_gini_comparison(classes):
    fig = go.Figure()
    
    values = list(classes.values())
    labels = list(classes.keys())
    
    fig.add_trace(go.Bar(
        x=labels,
        y=values,
        name='Valores por Classe',
        marker_color='#1f77b4',
        hovertemplate="<b>%{x}</b><br>" +
                     "Score: %{y:.3f}<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        title="Distribuição do Índice de Gini por Classe",
        xaxis_title="Classes",
        yaxis_title="Valor",
        showlegend=True
    )
    return fig

def show_metrics():
    st.header("Métricas Técnicas do Processo de Decisão")
    
    # Gini Index Section
    st.subheader("1. Índice de Gini")
    
    with st.expander("Como interpretar o Índice de Gini?"):
        st.markdown("""
        O Índice de Gini mede a impureza de um conjunto de dados. Em nossa árvore de decisão, 
        ele indica quão bem as características distinguem entre diferentes DLTs.
        
        ### Interpretação:
        - **Valores próximos a 0**: Melhor separação entre classes
        - **Valores próximos a 1**: Maior mistura entre classes
        
        ### Fórmula:
        """)
        st.latex(r"Gini = 1 - \sum_{i=1}^{n} p_i^2")
        st.markdown("""
        Onde:
        - $p_i$ é a proporção de cada classe no conjunto
        - $n$ é o número total de classes
        """)
    
    # Example calculation and visualizations
    if 'recommendation' in st.session_state:
        rec = st.session_state.recommendation
        if 'evaluation_matrix' in rec:
            classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
            gini = calcular_gini(classes)
            entropy = calcular_entropia(classes)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Índice de Gini Atual",
                    value=f"{gini:.3f}",
                    help="Quanto menor, melhor a separação entre as classes"
                )
            
            with col2:
                st.metric(
                    label="Entropia Atual",
                    value=f"{entropy:.3f} bits",
                    help="Quanto menor, mais certeza na decisão"
                )
            
            if 'answers' in st.session_state:
                depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
                total_nos = len(st.session_state.answers) * 2 + 1
                nos_podados = total_nos - len(st.session_state.answers) - 1
                pruning_ratio = calcular_pruning(total_nos, nos_podados)
                
                # Add radar chart
                fig_radar = create_metrics_radar_chart(
                    gini,
                    entropy,
                    depth / 10,  # Normalize to 0-1 range
                    pruning_ratio
                )
                st.plotly_chart(fig_radar, use_container_width=True)
                
                with st.expander("Como interpretar o Gráfico Radar?"):
                    st.markdown("""
                    O gráfico radar mostra todas as métricas importantes em um único visual:
                    
                    - **Índice de Gini**: Pureza da classificação
                    - **Entropia**: Certeza nas decisões
                    - **Profundidade**: Complexidade da árvore (normalizada)
                    - **Taxa de Poda**: Eficiência da simplificação
                    
                    Quanto maior a área preenchida, melhor o desempenho geral do modelo.
                    """)
                
                # Add Gini comparison
                fig_gini = create_gini_comparison(classes)
                st.plotly_chart(fig_gini, use_container_width=True)
                
                with st.expander("Como interpretar o Gráfico de Barras?"):
                    st.markdown("""
                    O gráfico de barras mostra a distribuição dos scores entre as diferentes DLTs:
                    
                    - **Altura da barra**: Score da DLT
                    - **Cores**: Azul padrão (#1f77b4) para facilitar a visualização
                    - **Interatividade**: Passe o mouse sobre as barras para ver valores exatos
                    
                    Uma distribuição mais uniforme indica maior incerteza na recomendação.
                    """)

    # Entropy Section
    st.subheader("2. Entropia")
    with st.expander("Como interpretar a Entropia?"):
        st.markdown("""
        A Entropia mede a aleatoriedade ou incerteza em nosso conjunto de decisões.
        Uma menor entropia indica decisões mais consistentes e confiáveis.
        
        ### Interpretação:
        - **Valores baixos**: Alta certeza nas decisões
        - **Valores altos**: Maior incerteza/aleatoriedade
        
        ### Fórmula:
        """)
        st.latex(r"Entropia = -\sum_{i=1}^{n} p_i \log_2(p_i)")
        st.markdown("""
        Onde:
        - $p_i$ é a probabilidade de cada classe
        - Logaritmo na base 2 é usado para medir em bits
        """)
    
    # Decision Tree Metrics
    st.subheader("3. Métricas da Árvore de Decisão")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'answers' in st.session_state:
            depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
            st.metric(
                label="Profundidade da Árvore",
                value=f"{depth:.1f}",
                help="Número médio de decisões necessárias"
            )
    
    with col2:
        if 'recommendation' in st.session_state:
            total_nos = len(st.session_state.answers) * 2 + 1
            nos_podados = total_nos - len(st.session_state.answers) - 1
            pruning_ratio = calcular_pruning(total_nos, nos_podados)
            st.metric(
                label="Taxa de Poda",
                value=f"{pruning_ratio:.2%}",
                help="Porcentagem de nós removidos para simplificação"
            )

def show_reference_table():
    # Updated table structure with data from the provided file
    dlt_data = {
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
        ]
    }
    
    df = pd.DataFrame(dlt_data)
    st.table(df)

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")

    st.markdown("## Referência de DLTs e Algoritmos")
    st.write("Abaixo está uma tabela detalhada com as principais DLTs e suas características para aplicações em saúde:")
    show_reference_table()

    st.markdown("---")
    st.subheader("Iniciar o Processo de Seleção de DLT")
    if st.button("Iniciar Questionário", key="start_questionnaire", help="Clique aqui para começar o processo de seleção de DLT"):
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

if __name__ == "__main__":
    main()
