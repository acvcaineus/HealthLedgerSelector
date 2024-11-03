import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_peso_caracteristica)
from utils import init_session_state

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

def create_metrics_radar_chart(gini, entropy, depth, pruning):
    """Create a radar chart for technical metrics visualization."""
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

def create_characteristic_weights_chart(characteristic_weights):
    """Create a radar chart for characteristic weights visualization."""
    fig = go.Figure()
    
    chars = list(characteristic_weights.keys())
    values = [characteristic_weights[char]['peso_ajustado'] for char in chars]
    values.append(values[0])  # Close the polygon
    chars.append(chars[0])  # Close the polygon
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=chars,
        fill='toself',
        name='Pesos Ajustados'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Distribuição dos Pesos das Características"
    )
    return fig

def show_metrics():
    """Display technical metrics and analysis."""
    st.header("Métricas Técnicas do Processo de Decisão")
    
    if 'answers' in st.session_state and len(st.session_state.answers) > 0:
        answers = st.session_state.answers
        
        # Calculate basic metrics
        total_nos = len(answers) * 2 + 1
        nos_podados = total_nos - len(answers) - 1
        pruning_metrics = calcular_pruning(total_nos, nos_podados)
        
        # Create dummy classes for Gini and Entropy calculation
        classes = {'class_a': len(answers), 'class_b': nos_podados}
        gini = calcular_gini(classes)
        entropy = calcular_entropia(classes)
        depth = calcular_profundidade_decisoria(list(range(len(answers))))
        
        # Display metrics in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Métricas de Classificação")
            st.metric(
                label="Índice de Gini",
                value=f"{gini:.3f}",
                help="Medida de pureza da classificação"
            )
            st.metric(
                label="Entropia",
                value=f"{entropy:.3f} bits",
                help="Medida de incerteza na decisão"
            )
        
        with col2:
            st.subheader("Métricas da Árvore")
            st.metric(
                label="Profundidade da Árvore",
                value=f"{depth:.1f}",
                help="Número médio de decisões necessárias"
            )
            st.metric(
                label="Taxa de Poda",
                value=f"{pruning_metrics['pruning_ratio']:.2%}",
                help="Proporção de nós removidos"
            )

        with st.expander("Explicação do Índice de Gini"):
            st.write("O Índice de Gini mede a pureza da classificação...")
            st.write("Valores próximos a 0 indicam boa separação entre as classes")
            st.write("Valores próximos a 1 indicam maior mistura entre as classes")

        with st.expander("Explicação da Entropia"):
            st.write("A Entropia mede a incerteza na decisão...")
            st.write("Valores baixos indicam maior certeza na decisão")
            st.write("Valores altos indicam maior incerteza na decisão")

        with st.expander("Explicação da Profundidade"):
            st.write("A profundidade mede o número médio de decisões necessárias...")
            st.write("Valores menores indicam um processo decisório mais direto")
            st.write("Valores maiores indicam um processo decisório mais complexo")

        with st.expander("Explicação da Taxa de Poda"):
            st.write("A taxa de poda indica a simplificação do modelo...")
            st.write("Valores altos indicam maior simplificação do modelo")
            st.write("Valores baixos indicam menor simplificação do modelo")
        
        # Display metrics radar chart
        fig_radar = create_metrics_radar_chart(
            gini,
            entropy,
            depth / 10,  # Normalize to 0-1 range
            pruning_metrics['pruning_ratio']
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Characteristic weights visualization
        st.subheader("Pesos das Características")
        weights = {
            "security": 0.4,
            "scalability": 0.25,
            "energy_efficiency": 0.20,
            "governance": 0.15
        }
        
        characteristic_weights = {}
        for char in weights.keys():
            weight_metrics = calcular_peso_caracteristica(char, weights, answers)
            characteristic_weights[char] = weight_metrics
        
        fig_weights = create_characteristic_weights_chart(characteristic_weights)
        st.plotly_chart(fig_weights)
    else:
        st.info("Complete o questionário para visualizar as métricas detalhadas.")

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")

    st.markdown('''
    ## Como o Framework Funciona

    1. **Base do Framework**: 
       - A tabela abaixo apresenta a estrutura hierárquica de classificação das DLTs
       - Cada DLT está associada a um tipo, grupo de algoritmo e algoritmos específicos

    2. **Processo de Seleção**:
       - O framework avalia suas necessidades através de um questionário
       - As respostas são analisadas considerando segurança, escalabilidade, eficiência e governança
       - A recomendação é baseada na tabela de classificação e suas prioridades

    3. **Resultado**:
       - Você receberá uma recomendação detalhada da DLT mais adequada
       - Incluindo explicações técnicas e casos de uso relacionados
       - Métricas de avaliação para validar a recomendação
    ''')

    st.markdown("## Referência de DLTs e Algoritmos")
    st.write("Abaixo está uma tabela detalhada com as principais DLTs e suas características para aplicações em saúde:")
    
    # Reference table data
    dlt_data = {
        'DLT': [
            'Hyperledger Fabric', 'Corda', 'Quorum', 'VeChain', 'IOTA',
            'Ripple (XRP Ledger)', 'Stellar', 'Bitcoin', 'Ethereum (PoW)',
            'Ethereum 2.0 (PoS)'
        ],
        'Tipo de DLT': [
            'DLT Permissionada Privada', 'DLT Permissionada Simples', 'DLT Híbrida',
            'DLT Híbrida', 'DLT Pública (DAG)', 'DLT com Consenso Delegado',
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
        'Algoritmos de Consenso': [
            'RAFT, PBFT',
            'RAFT',
            'RAFT, IBFT',
            'PoA',
            'Tangle',
            'Ripple Consensus Protocol',
            'Stellar Consensus Protocol',
            'PoW',
            'PoW',
            'PoS'
        ]
    }
    df = pd.DataFrame(dlt_data)
    st.dataframe(df)

    # Add download button for consolidated data
    csv = convert_df(df)
    st.download_button(
        label="Baixar Dados Consolidados",
        data=csv,
        file_name='dlt_dados_consolidados.csv',
        mime='text/csv',
    )

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
