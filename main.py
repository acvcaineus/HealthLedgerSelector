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

    data = {
        'Grupo': ['Alta Segurança e Controle', 'Alta Segurança e Descentralização', 
                 'Alta Segurança e Descentralização', 'Alta Eficiência Operacional', 
                 'Alta Eficiência Operacional', 'Alta Eficiência Operacional', 
                 'Escalabilidade e Governança Flexível', 'Escalabilidade e Governança Flexível', 
                 'Alta Escalabilidade em Redes IoT'],
        'Tipo DLT': ['DLT Permissionada Privada', 'DLT Pública Permissionless', 
                     'DLT Pública Permissionless', 'DLT Permissionada Simples', 
                     'DLT Permissionada Simples', 'DLT Permissionada Simples', 
                     'DLT Híbrida', 'DLT com Consenso Delegado', 'DLT Pública'],
        'Nome DLT': ['Hyperledger Fabric', 'Bitcoin', 'Ethereum', 'Quorum', 
                     'Quorum', 'VeChain', 'Ethereum 2.0', 'EOS', 'IOTA'],
        'Algoritmo de Consenso': ['PBFT', 'PoW', 'PoS (em transição)', 'RAFT', 
                                 'PoA', 'PoA', 'PoS', 'DPoS', 'Tangle']
    }

    df = pd.DataFrame(data)
    st.table(df)

    if st.button("Iniciar Seleção de DLT", type="primary"):
        st.session_state.page = 'Framework Proposto'
        st.rerun()

def show_metrics():
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
                        st.latex(r'''Gini = 1 - \sum_{i=1}^{n} p_i^2''')
                        st.markdown("""
                            O Índice de Gini mede a dispersão das recomendações entre as diferentes DLTs.
                            - Valor próximo a 0: Uma DLT claramente se destaca
                            - Valor próximo a 1: Várias DLTs têm pontuações similares
                        """)

                    st.subheader("2. Entropia da Decisão")
                    with st.expander("Ver Explicação da Entropia"):
                        st.latex(r'''Entropia = -\sum_{i=1}^{n} p_i \log_2(p_i)''')
                        st.markdown("""
                            A Entropia mede a incerteza na classificação das DLTs.
                            - Valor baixo: Alta certeza na recomendação
                            - Valor alto: Maior incerteza na escolha
                        """)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Índice de Gini", f"{gini:.2f}")
                    with col2:
                        st.metric("Entropia", f"{entropy:.2f}")

                    st.subheader("3. Matriz de Avaliação")
                    matrix_data = []
                    for dlt, data in rec['evaluation_matrix'].items():
                        row = [dlt]
                        for metric in ['security', 'scalability', 'energy_efficiency', 'governance']:
                            row.append(float(data['metrics'][metric]))
                        matrix_data.append(row)

                    df = pd.DataFrame(matrix_data, 
                                    columns=['DLT', 'Segurança', 'Escalabilidade', 
                                            'Eficiência Energética', 'Governança'])
                    st.table(df)

                    st.subheader("4. Visualização das Métricas")
                    fig = go.Figure()
                    for dlt in df['DLT']:
                        values = df[df['DLT'] == dlt].iloc[0, 1:].values.tolist()
                        values.append(values[0])  # Close the polygon
                        fig.add_trace(go.Scatterpolar(
                            r=values,
                            theta=['Segurança', 'Escalabilidade', 'Eficiência Energética', 
                                  'Governança', 'Segurança'],
                            name=dlt,
                            fill='toself'
                        ))

                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                        showlegend=True,
                        title="Comparação de Métricas entre DLTs"
                    )
                    st.plotly_chart(fig)

        else:
            st.info("Complete o processo de seleção para ver as métricas.")

    except Exception as e:
        st.error(f"Erro ao exibir métricas: {str(e)}")
        st.code(traceback.format_exc())

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
        with st.sidebar:
            st.title("Menu")
            menu_options = ['Início', 'Framework Proposto', 'Métricas']
            menu_option = st.selectbox(
                "Escolha uma opção",
                menu_options,
                index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
            )
            st.session_state.page = menu_option

            if st.button("Logout"):
                logout()

        if menu_option == 'Início':
            show_home_page()
        elif menu_option == 'Framework Proposto':
            run_decision_tree()
        elif menu_option == 'Métricas':
            show_metrics()

if __name__ == "__main__":
    main()
