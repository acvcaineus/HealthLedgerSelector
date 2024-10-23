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
        st.rerun()

def show_metrics():
    st.header("Métricas e Diferenciais do Framework Proposto")
    
    classes = {"Sim": 70, "Não": 30}
    decisoes = [3, 4, 2, 5]
    total_nos = 20
    nos_podados = 5
    pesos = {"segurança": 0.4, "escalabilidade": 0.3, "eficiência": 0.2, "governança": 0.1}
    
    gini = calcular_gini(classes)
    entropia = calcular_entropia(classes)
    profundidade = calcular_profundidade_decisoria(decisoes)
    pruning_ratio = calcular_pruning(total_nos, nos_podados)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Impureza de Gini", f"{gini:.2f}")
        st.metric("Entropia", f"{entropia:.2f}")
    with col2:
        st.metric("Profundidade Decisória", f"{profundidade:.2f}")
        st.metric("Pruning Ratio", f"{pruning_ratio:.2f}")

    fig = go.Figure(data=[
        go.Bar(name='Métricas', x=['Gini', 'Entropia', 'Profundidade', 'Pruning'],
               y=[gini, entropia, profundidade, pruning_ratio])
    ])
    fig.update_layout(title="Visão Geral das Métricas do Framework")
    st.plotly_chart(fig)

    st.subheader("Fórmulas e Explicações Detalhadas")
    
    with st.expander("Impureza de Gini"):
        st.write("""
        **Fórmula**: Gini = 1 - Σ(pi²)
        
        Onde:
        - pi é a proporção de cada classe no conjunto de dados
        - Σ representa o somatório de todas as classes
        
        **Interpretação**:
        - Valor próximo a 0: indica alta pureza (decisões mais confiáveis)
        - Valor próximo a 1: indica alta impureza (decisões menos confiáveis)
        
        **Aplicação no Framework**:
        Usada para medir a qualidade das decisões em cada nó da árvore de decisão,
        ajudando a identificar pontos onde o framework pode ser mais preciso.
        """)

    with st.expander("Entropia de Shannon"):
        st.write("""
        **Fórmula**: Entropia = -Σ(pi * log2(pi))
        
        Onde:
        - pi é a proporção de cada classe
        - log2 é o logaritmo na base 2
        
        **Interpretação**:
        - Valor baixo: menor incerteza nas decisões
        - Valor alto: maior incerteza nas decisões
        
        **Aplicação no Framework**:
        Utilizada para medir a quantidade de informação necessária para classificar
        corretamente uma DLT ou algoritmo de consenso.
        """)

    with st.expander("Profundidade Decisória"):
        st.write("""
        **Fórmula**: Profundidade Média = Σ(profundidades) / número de decisões
        
        **Interpretação**:
        - Valor baixo: árvore de decisão mais simples e interpretável
        - Valor alto: árvore de decisão mais complexa
        
        **Aplicação no Framework**:
        Indica a complexidade do processo decisório, ajudando a balancear
        precisão e interpretabilidade.
        """)

    with st.expander("Pruning Ratio"):
        st.write("""
        **Fórmula**: Pruning Ratio = (total_nós - nós_podados) / total_nós
        
        **Interpretação**:
        - Próximo a 1: modelo mais simplificado
        - Próximo a 0: modelo mais complexo
        
        **Aplicação no Framework**:
        Mede a eficácia da simplificação do modelo de decisão, garantindo
        um equilíbrio entre precisão e simplicidade.
        """)

    st.subheader("Métricas Avançadas")
    
    st.write("**Pesos Normalizados das Características:**")
    for caracteristica, peso in pesos.items():
        peso_norm = calcular_peso_caracteristica(caracteristica, pesos)
        st.write(f"- {caracteristica.capitalize()}: {peso_norm:.2%}")

    st.write("**Métricas de Desempenho do Sistema:**")
    historico_exemplo = [
        {'acerto': True}, {'acerto': True}, 
        {'acerto': False}, {'acerto': True}
    ]
    precisao, recall, f1 = calcular_metricas_desempenho(historico_exemplo)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Precisão", f"{precisao:.2%}")
    with col2:
        st.metric("Recall", f"{recall:.2%}")
    with col3:
        st.metric("F1-Score", f"{f1:.2%}")

    st.subheader("Validação Cruzada do Framework")
    st.write("""
    O framework utiliza validação cruzada para garantir a robustez das recomendações:
    1. **Similaridade de Jaccard**: Mede a similaridade entre diferentes recomendações
    2. **Confiabilidade**: Avalia a confiança nas recomendações baseada nos scores
    3. **Métricas de Desempenho**: Monitora precisão, recall e F1-score do sistema
    """)

def show_user_profile():
    st.header("Perfil do Usuário")
    st.write(f"Bem-vindo, {st.session_state.username}!")

    recommendations = get_user_recommendations(st.session_state.username)
    
    if recommendations:
        st.subheader("Suas Recomendações Salvas:")
        for rec in recommendations:
            st.write(f"Cenário: {rec['scenario']}")
            st.write(f"DLT Recomendada: {rec['dlt']}")
            st.write(f"Algoritmo de Consenso: {rec['consensus']}")
            st.write(f"Data: {rec['timestamp']}")
            st.write("---")
    else:
        st.write("Você ainda não tem recomendações salvas.")

def show_recommendation_comparison():
    st.header("Comparação de Recomendações")
    if 'recommendation' in st.session_state and st.session_state.recommendation:
        rec = st.session_state.recommendation
        st.write(f"DLT Recomendada: {rec.get('dlt', 'Não disponível')}")
        st.write(f"Grupo de Consenso: {rec.get('consensus_group', 'Não disponível')}")
        st.write(f"Algoritmo de Consenso Recomendado: {rec.get('consensus', 'Não disponível')}")
        
        if 'consensus_group' in rec:
            st.subheader("Comparação Visual dos Algoritmos")
            comparison_data = compare_algorithms(rec['consensus_group'])
            
            new_metrics = {
                'Latência': {alg: round(5 - score, 2) for alg, score in comparison_data['Escalabilidade'].items()},
                'Throughput': comparison_data['Escalabilidade'],
                'Tolerância a Falhas': comparison_data['Segurança'],
                'Nível de Descentralização': {alg: round((score + comparison_data['Governança'][alg]) / 2, 2) for alg, score in comparison_data['Segurança'].items()}
            }
            comparison_data.update(new_metrics)

            available_metrics = list(comparison_data.keys())
            selected_metrics = st.multiselect("Selecione as métricas para comparar", available_metrics, default=available_metrics[:4])

            if selected_metrics:
                fig = go.Figure()

                for alg in comparison_data['Segurança'].keys():
                    fig.add_trace(go.Scatterpolar(
                        r=[comparison_data[metric][alg] for metric in selected_metrics],
                        theta=selected_metrics,
                        fill='toself',
                        name=alg
                    ))

                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 5]
                        )),
                    showlegend=True
                )
                
                st.plotly_chart(fig)

            st.subheader("Comparação Detalhada")
            st.table({metric: comparison_data[metric] for metric in selected_metrics})

            st.subheader("Gráfico de Barras - Comparação de Algoritmos")
            alg_scores = {alg: sum(consensus_algorithms[alg].values()) for alg in rec['algorithms']}
            fig = go.Figure(data=[go.Bar(x=list(alg_scores.keys()), y=list(alg_scores.values()))])
            fig.update_layout(title="Pontuação Total dos Algoritmos de Consenso", xaxis_title="Algoritmos", yaxis_title="Pontuação")
            st.plotly_chart(fig)

            st.subheader("Justificativa da Recomendação")
            st.write(f"O algoritmo {rec['consensus']} foi selecionado porque:")
            for metric in selected_metrics:
                if rec['consensus'] in comparison_data[metric]:
                    score = comparison_data[metric][rec['consensus']]
                    st.write(f"- {metric}: pontuação {score}/5")

            st.subheader("Cenários de Aplicação e Fundamentação Científica")
            scenarios = {
                "PBFT": {
                    "description": "Ideal para prontuários eletrônicos e sistemas que requerem alta segurança e controle centralizado.",
                    "reference": "Mehmood et al. (2025) - 'BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain'"
                },
                "PoW": {
                    "description": "Adequado para sistemas de pagamento descentralizados e proteção de dados críticos de saúde pública.",
                    "reference": "Liu et al. (2024) - 'A systematic study on integrating blockchain in healthcare for electronic health record management and tracking medical supplies'"
                },
                "PoS": {
                    "description": "Ótimo para redes de saúde que necessitam de alta escalabilidade e eficiência energética.",
                    "reference": "Nawaz et al. (2024) - 'Hyperledger sawtooth based supply chain traceability system for counterfeit drugs'"
                },
                "DPoS": {
                    "description": "Perfeito para sistemas de monitoramento de saúde pública e redes regionais de saúde.",
                    "reference": "Javed et al. (2024) - 'Mutual authentication enabled trust model for vehicular energy networks using Blockchain in Smart Healthcare Systems'"
                },
                "PoA": {
                    "description": "Ideal para sistemas locais de saúde e agendamento de pacientes.",
                    "reference": "Popoola et al. (2024) - 'A critical literature review of security and privacy in smart home healthcare schemes adopting IoT & blockchain'"
                },
                "Tangle": {
                    "description": "Excelente para monitoramento de dispositivos IoT em saúde e processamento de dados em tempo real.",
                    "reference": "Salim et al. (2024) - 'Privacy-preserving and scalable federated blockchain scheme for healthcare 4.0'"
                }
            }
            for alg, info in scenarios.items():
                if alg in comparison_data['Segurança']:
                    st.write(f"**{alg}**: {info['description']}")
                    st.write(f"*Referência:* {info['reference']}")

        else:
            st.write("Dados de comparação não disponíveis.")

def show_framework_info():
    st.header("Sobre o Framework Proposto")
    
    st.subheader("Embasamento Teórico")
    st.write("""
    O framework proposto é baseado na Pilha Shermin, que divide a análise de DLTs em quatro camadas:
    1. Aplicação
    2. Consenso
    3. Infraestrutura
    4. Internet
    
    Esta abordagem permite uma avaliação holística das necessidades do projeto de saúde e das capacidades das diferentes DLTs.
    """)
    
    st.subheader("Métricas e Ponderações")
    st.write("""
    O framework utiliza as seguintes métricas principais:
    - Segurança (40%)
    - Escalabilidade (30%)
    - Eficiência Energética (20%)
    - Governança (10%)
    
    Estas ponderações foram definidas com base na importância relativa de cada aspecto para projetos de saúde típicos.
    """)
    
    st.subheader("Fundamentação da Aplicação")
    st.write("""
    A aplicação utiliza um sistema de pontuação ponderada para recomendar a DLT e o algoritmo de consenso mais adequados.
    As respostas do usuário são mapeadas para características específicas, que por sua vez influenciam a pontuação final de cada opção.
    """)
    
    st.subheader("Embasamento Científico")
    st.write("""
    O framework proposto é apoiado por recentes pesquisas científicas na área de blockchain e DLT aplicadas à saúde. Alguns dos principais achados incluem:

    1. Segurança e Privacidade: Estudos como o de Popoola et al. (2024) destacam a importância da segurança e privacidade em sistemas de saúde baseados em IoT e blockchain, especialmente em ambientes domésticos inteligentes.

    2. Rastreabilidade na Cadeia de Suprimentos: Mehmood et al. (2025) propõem protocolos de consenso leves para blockchains de consórcio, visando melhorar a rastreabilidade de medicamentos.

    3. Escalabilidade e Eficiência: Salim et al. (2024) apresentam um esquema federado de blockchain para Healthcare 4.0, focando na preservação da privacidade e na escalabilidade.

    4. Interoperabilidade: Makhdoom et al. (2024) desenvolveram um framework distribuído e compatível com a privacidade para compartilhamento de dados pessoais em ecossistemas IoT.

    5. Autenticação e Confiança: Javed et al. (2024) propõem um modelo de confiança baseado em autenticação mútua para redes de energia veicular usando Blockchain em Sistemas de Saúde Inteligentes.

    Estes estudos corroboram a escolha das DLTs e algoritmos de consenso incluídos no framework, destacando sua aplicabilidade em diversos cenários de saúde, desde o gerenciamento de registros médicos eletrônicos até o rastreamento de suprimentos médicos.
    """)
    
    st.subheader("Limitações")
    st.write("""
    1. Generalização: O framework pode não capturar todas as nuances de projetos de saúde altamente especializados.
    2. Dependência de dados atualizados: A eficácia das recomendações depende da atualização constante das informações sobre DLTs e algoritmos.
    3. Simplificação: Algumas complexidades técnicas são simplificadas para tornar o processo de decisão mais acessível.
    4. Foco limitado: O framework se concentra principalmente em DLTs e pode não abordar todos os aspectos de implementação de blockchain em saúde.
    5. Maturidade Tecnológica: Algumas DLTs, como IOTA, ainda estão em fase de desenvolvimento e implementação completa, como apontado por Salim et al. (2024).
    """)

def main():
    init_session_state()

    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")

    if not is_authenticated():
        st.title("SeletorDLTSaude - Login")

        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.title("Menu")
        menu_options = ['Início', 'Framework Proposto', 'Comparação de Recomendações', 'Métricas', 'Sobre o Framework', 'Perfil', 'Logout']

        menu_option = st.sidebar.selectbox(
            "Escolha uma opção",
            menu_options,
            index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
        )

        st.session_state.page = menu_option

        if st.session_state.page == 'Início':
            show_home_page()
        elif st.session_state.page == 'Framework Proposto':
            run_decision_tree()
        elif st.session_state.page == 'Comparação de Recomendações':
            show_recommendation_comparison()
        elif st.session_state.page == 'Métricas':
            show_metrics()
        elif st.session_state.page == 'Sobre o Framework':
            show_framework_info()
        elif st.session_state.page == 'Perfil':
            show_user_profile()
        elif st.session_state.page == 'Logout':
            logout()
            st.session_state.page = 'Início'

if __name__ == "__main__":
    main()