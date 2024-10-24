import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_peso_caracteristica, calcular_jaccard_similarity,
                    calcular_confiabilidade_recomendacao, calcular_metricas_desempenho)
from utils import init_session_state

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")

    st.subheader("Informações sobre DLTs para Saúde")
    dlt_data = {
        'DLT': ['Hyperledger Fabric', 'VeChain', 'Quorum (Mediledger)', 'IOTA', 'Ripple (XRP Ledger)', 'Stellar', 'Bitcoin', 'Ethereum (PoW)', 'Ethereum 2.0 (PoS)'],
        'Grupo de Algoritmo': ['Alta Segurança e Controle dos dados', 'Alta Eficiência Operacional em redes locais', 'Escalabilidade e Governança Flexível', 'Alta Escalabilidade em Redes IoT', 'Alta Eficiência Operacional em redes locais', 'Alta Eficiência Operacional em redes locais', 'Alta Segurança e Descentralização', 'Alta Segurança e Descentralização', 'Escalabilidade e Governança Flexível'],
        'Algoritmo de Consenso': ['RAFT/IBFT', 'Proof of Authority (PoA)', 'RAFT/IBFT', 'Tangle', 'Ripple Consensus Algorithm', 'Stellar Consensus Protocol (SCP)', 'Proof of Work (PoW)', 'Proof of Work (PoW)', 'Proof of Stake (PoS)'],
        'Caso de Uso': ['Rastreabilidade de medicamentos na cadeia de suprimentos', 'Rastreamento de suprimentos médicos e cadeia farmacêutica', 'Monitoramento e rastreamento de medicamentos', 'Compartilhamento seguro de dados de pacientes via IoT', 'Processamento eficiente de transações e segurança de dados', 'Gerenciamento de transações de pagamentos entre provedores', 'Armazenamento seguro de dados médicos críticos', 'Contratos inteligentes e registros médicos eletrônicos', 'Aceleração de ensaios clínicos e compartilhamento de dados'],
        'Desafios e Limitações': ['Baixa escalabilidade para redes muito grandes', 'Dependência de validadores centralizados', 'Escalabilidade limitada em redes públicas', 'Maturidade tecnológica (não totalmente implementada)', 'Centralização nos validadores principais', 'Governança dependente do quorum', 'Consumo energético elevado, escalabilidade limitada', 'Consumo de energia elevado', 'Governança flexível, mas centralização é possível'],
        'Referência Bibliográfica': ['Mehmood et al. (2025)', 'Popoola et al. (2024)', 'Mehmood et al. (2025)', 'Salim et al. (2024)', 'Makhdoom et al. (2024)', 'Javed et al. (2024)', 'Liu et al. (2024)', 'Makhdoom et al. (2024)', 'Nawaz et al. (2024)']
    }
    df = pd.DataFrame(dlt_data)
    st.table(df)

    st.markdown("---")
    st.subheader("Iniciar o Processo de Seleção de DLT")
    if st.button("Iniciar Questionário", key="start_questionnaire", help="Clique aqui para começar o processo de seleção de DLT"):
        st.success("Questionário iniciado! Redirecionando para o Framework Proposto...")
        st.session_state.page = "Framework Proposto"
        st.rerun()  # Updated to use rerun

def show_framework_info():
    st.header("Sobre o Framework de Seleção de DLT")
    
    st.subheader("Critérios de Avaliação")
    criteria_data = {
        "Critério": ["Segurança", "Escalabilidade", "Eficiência Energética", "Governança"],
        "Peso": ["40%", "30%", "20%", "10%"],
        "Descrição": [
            "Proteção de dados sensíveis e resistência a ataques",
            "Capacidade de lidar com grande volume de transações",
            "Consumo de energia e sustentabilidade",
            "Flexibilidade na gestão e controle da rede"
        ]
    }
    st.table(pd.DataFrame(criteria_data))
    
    st.subheader("Embasamento Acadêmico")
    st.write("""
    O framework é baseado em pesquisas recentes na área de blockchain e DLT aplicadas à saúde:
    
    1. **Segurança e Privacidade**: Popoola et al. (2024) destacam a importância da segurança em sistemas de saúde baseados em IoT.
    
    2. **Escalabilidade**: Salim et al. (2024) apresentam um esquema federado de blockchain para Healthcare 4.0.
    
    3. **Eficiência Energética**: Liu et al. (2024) abordam a integração de blockchain em sistemas de saúde.
    
    4. **Governança**: Nawaz et al. (2024) exploram sistemas de rastreabilidade na cadeia de suprimentos.
    """)

def show_recommendation_comparison():
    st.header("Comparação de Algoritmos de Consenso")
    
    if 'recommendation' not in st.session_state:
        st.warning("Por favor, complete o questionário primeiro para ver as comparações.")
        return
        
    rec = st.session_state.recommendation
    if 'consensus_group' not in rec:
        st.warning("Grupo de consenso não disponível.")
        return
        
    comparison_data = compare_algorithms(rec['consensus_group'])
    
    metrics = list(comparison_data.keys())
    algorithms = list(comparison_data['Segurança'].keys())
    
    fig = go.Figure()
    for alg in algorithms:
        fig.add_trace(go.Scatterpolar(
            r=[float(comparison_data[metric][alg]) for metric in metrics],
            theta=metrics,
            name=alg,
            fill='toself'
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True,
        title="Comparação de Métricas por Algoritmo"
    )
    st.plotly_chart(fig)
    
    st.subheader("Métricas Detalhadas")
    for metric in metrics:
        st.write(f"**{metric}**")
        metric_data = {
            "Algoritmo": list(comparison_data[metric].keys()),
            "Pontuação": [float(val) for val in comparison_data[metric].values()]
        }
        st.table(pd.DataFrame(metric_data))

def show_metrics():
    st.header("Métricas Adotadas")
    
    st.subheader("Fórmulas e Cálculos")
    
    st.write("### 1. Índice de Gini")
    st.latex(r"Gini = 1 - \sum_{i=1}^{n} p_i^2")
    st.write("Onde:")
    st.write("- p_i é a proporção de cada classe no conjunto")
    st.write("- Valores mais próximos de 0 indicam maior pureza nas decisões")
    
    st.write("### 2. Entropia")
    st.latex(r"Entropia = -\sum_{i=1}^{n} p_i \log_2(p_i)")
    st.write("Onde:")
    st.write("- p_i é a proporção de cada classe")
    st.write("- Menor entropia indica decisões mais consistentes")
    
    st.write("### 3. Pontuação Ponderada")
    st.latex(r"Score = \sum_{i=1}^{n} w_i \times v_i")
    st.write("Onde:")
    st.write("- w_i é o peso de cada critério")
    st.write("- v_i é o valor normalizado do critério")
    
    example_data = {
        "Métrica": ["Segurança", "Escalabilidade", "Eficiência", "Governança"],
        "Valor Base": [4.5, 3.8, 4.2, 3.9],
        "Peso": [0.4, 0.3, 0.2, 0.1],
        "Score Final": [1.8, 1.14, 0.84, 0.39]
    }
    st.table(pd.DataFrame(example_data))
    
    total_score = sum(float(score) for score in example_data["Score Final"])
    st.write(f"Score Total do Exemplo: {total_score:.2f}")

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
        menu_options = ['Início', 'Framework Proposto', 'Comparação de Recomendações', 
                       'Métricas', 'Sobre o Framework', 'Perfil', 'Logout']
        
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
        elif menu_option == 'Comparação de Recomendações':
            show_recommendation_comparison()
        elif menu_option == 'Métricas':
            show_metrics()
        elif menu_option == 'Sobre o Framework':
            show_framework_info()
        elif menu_option == 'Perfil':
            show_user_profile()
        elif menu_option == 'Logout':
            logout()
            st.session_state.page = 'Início'
            st.rerun()  # Updated to use rerun

if __name__ == "__main__":
    main()
