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
            'Alta Segurança e Controle',
            'Alta Segurança e Descentralização',
            'Alta Segurança e Descentralização',
            'Alta Eficiência Operacional',
            'Alta Eficiência Operacional',
            'Escalabilidade e Governança Flexível',
            'Escalabilidade e Governança Flexível',
            'Alta Escalabilidade em Redes IoT'
        ],
        'Tipo de DLT': [
            'DLT Permissionada Privada',
            'DLT Pública Permissionless',
            'DLT Pública Permissionless',
            'DLT Permissionada Simples',
            'DLT Permissionada Simples',
            'DLT Híbrida',
            'DLT com Consenso Delegado',
            'DLT Pública'
        ],
        'Nome DLT': [
            'Hyperledger Fabric',
            'Bitcoin',
            'Ethereum',
            'Quorum',
            'VeChain',
            'Ethereum 2.0',
            'EOS',
            'IOTA'
        ],
        'Algoritmo de Consenso': [
            'PBFT',
            'PoW',
            'PoS (em transição)',
            'RAFT/PoA',
            'PoA',
            'PoS',
            'DPoS',
            'Tangle'
        ],
        'Características': [
            'Segurança elevada e resiliência contra falhas bizantinas; adequada para ambientes altamente controlados e permissionados.',
            'Oferece segurança máxima e total descentralização, essencial para redes abertas onde a integridade dos dados é crucial.',
            'Com transição para PoS, oferece alta segurança e eficiência energética para aplicações que exigem menos processamento intensivo.',
            'Alta eficiência em redes permissionadas; consenso baseado em autoridade ideal para redes empresariais.',
            'Alta eficiência e controle simplificado para gestão de cadeias de suprimento em redes permissionadas.',
            'Alta escalabilidade e eficiência energética, ideal para redes de saúde regionalizadas.',
            'Governança flexível e performance otimizada com arquitetura semi-descentralizada.',
            'Alta escalabilidade e processamento em tempo real para redes de dispositivos IoT em saúde.'
        ],
        'Casos de Uso': [
            'Prontuários eletrônicos, integração de dados sensíveis entre instituições de saúde',
            'Sistemas de pagamento descentralizados, dados críticos de saúde pública',
            'Dados críticos de saúde pública, governança participativa',
            'Redes locais de hospitais, rastreamento de medicamentos',
            'Rastreamento de medicamentos, gestão de insumos hospitalares',
            'Monitoramento de saúde pública, integração de EHRs',
            'Aplicativos de telemedicina, redes de colaboração em pesquisa',
            'Monitoramento de dispositivos IoT hospitalares, dados em tempo real'
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)

    with st.expander("Ver Detalhes de Implementação e Referências"):
        st.markdown('''
            ### Casos de Implementação Real
            - **MyClinic**: Dados descentralizados em clínicas privadas (Hyperledger Fabric)
            - **MediLedger**: Rastreamento de medicamentos na cadeia farmacêutica (Bitcoin)
            - **Patientory**: Armazenamento seguro de dados de pacientes (Ethereum)
            - **PharmaLedger**: Rede permissionada para suprimentos farmacêuticos (Quorum)
            - **VeChain ToolChain**: Rastreabilidade de produtos médicos
            - **Ethereum-based Health Chain**: Integração de EHRs para hospitais regionais
            - **Telos Blockchain**: Rede colaborativa para dados de saúde em telemedicina
            - **IOTA Healthcare IoT**: Monitoramento IoT de dispositivos médicos

            ### Referências Acadêmicas
            - MEHMOOD et al. (2025) - BLPCA-ledger: A lightweight plenum consensus protocols
            - POPOOLA et al. (2024) - Security and privacy in smart home healthcare schemes
            - AKOH ATADOGA et al. (2024) - Blockchain in healthcare: A comprehensive review
            - DHINGRA et al. (2024) - Blockchain Technology Applications in Healthcare
            - AL-NBHANY et al. (2024) - Blockchain-IoT Healthcare Applications and Trends
        ''')

    if st.button("Iniciar Seleção de DLT", type="primary"):
        st.session_state.page = 'Framework Proposto'
        st.experimental_rerun()

def show_bench_comparisons():
    st.title("Comparação de Benchmarks de DLT em Saúde")
    
    # 1. Security Radar Chart
    st.header("1. Métricas Técnicas de Validação")
    with st.expander("Segurança (40%)"):
        st.markdown("""
        ### Análise de Segurança
        A segurança é um aspecto crítico para DLTs na área de saúde, representando 40% do peso total na avaliação.
        
        #### Componentes Avaliados:
        - Proteção de dados
        - Privacidade
        - Resistência a ataques
        - Conformidade com regulamentações
        """)
        
        security_data = {
            'MedRec': 4.5,
            'HealthBlock': 4.2,
            'MedChain': 4.0,
            'Framework BR': 4.3,
            'HealthChain': 4.1
        }
        fig_security = create_radar_chart(security_data, "Análise de Segurança dos Benchmarks", "Nível de Segurança")
        st.plotly_chart(fig_security)
        st.markdown("""
        #### Interpretação dos Resultados:
        - **5.0**: Excelente - Máxima segurança e conformidade
        - **4.0-4.9**: Muito Bom - Alta segurança com pequenas melhorias possíveis
        - **3.0-3.9**: Bom - Segurança adequada com áreas para melhoria
        - **< 3.0**: Necessita Atenção - Melhorias significativas necessárias
        """)
    
    # 2. Interoperability Analysis
    with st.expander("Interoperabilidade (20%)"):
        st.markdown("""
        ### Análise de Interoperabilidade
        A capacidade de integração com outros sistemas representa 20% da avaliação total.
        
        #### Aspectos Avaliados:
        - Compatibilidade com APIs
        - Suporte a padrões de interoperabilidade
        - Facilidade de integração
        """)
        
        interop_data = {
            'MedRec': {'APIs': 5, 'Standards': 4, 'Integration': 4},
            'HealthBlock': {'APIs': 4, 'Standards': 4, 'Integration': 3},
            'MedChain': {'APIs': 3, 'Standards': 4, 'Integration': 4},
            'Framework BR': {'APIs': 4, 'Standards': 5, 'Integration': 4},
            'HealthChain': {'APIs': 4, 'Standards': 3, 'Integration': 4}
        }
        fig_interop = create_interop_chart(interop_data)
        st.plotly_chart(fig_interop)
        st.markdown("""
        #### Métricas de Avaliação:
        - **APIs**: Qualidade e disponibilidade de APIs
        - **Standards**: Conformidade com padrões da indústria
        - **Integration**: Facilidade de implementação
        """)
    
    # 3. Scalability Bar Chart
    with st.expander("Escalabilidade (20%)"):
        st.markdown("""
        ### Análise de Escalabilidade
        Capacidade de crescimento e gerenciamento de carga representa 20% da avaliação.
        
        #### Métricas Avaliadas:
        - Transações por segundo (TPS)
        - Latência de rede
        - Capacidade de armazenamento
        """)
        
        scalability_data = {
            'MedRec': 850,
            'HealthBlock': 1200,
            'MedChain': 950,
            'Framework BR': 1100,
            'HealthChain': 900
        }
        fig_scale = create_scalability_chart(scalability_data)
        st.plotly_chart(fig_scale)
        st.markdown("""
        #### Interpretação:
        - **> 1000 TPS**: Excelente escalabilidade
        - **500-1000 TPS**: Boa escalabilidade
        - **< 500 TPS**: Limitada
        """)
    
    # 4. Energy Efficiency
    with st.expander("Eficiência Energética (10%)"):
        st.markdown("""
        ### Análise de Eficiência Energética
        O consumo de energia representa 10% da avaliação total.
        
        #### Aspectos Avaliados:
        - Consumo de energia por transação
        - Sustentabilidade do algoritmo de consenso
        - Impacto ambiental
        """)
        
        energy_data = {
            'PoA': {'tps': 1000, 'energy': 0.1},
            'PBFT': {'tps': 3000, 'energy': 0.3},
            'DPoS': {'tps': 2000, 'energy': 0.2}
        }
        fig_energy = create_energy_chart(energy_data)
        st.plotly_chart(fig_energy)
        st.markdown("""
        #### Classificação de Eficiência:
        - **< 0.1 kWh/tx**: Altamente eficiente
        - **0.1-0.3 kWh/tx**: Eficiente
        - **> 0.3 kWh/tx**: Necessita otimização
        """)
    
    # 5. Governance Score Table
    with st.expander("Governança (10%)"):
        st.markdown("""
        ### Análise de Governança
        A estrutura de governança representa 10% da avaliação total.
        
        #### Critérios Avaliados:
        - Controle de acesso
        - Auditoria
        - Conformidade regulatória
        """)
        
        governance_data = {
            'MedRec': {'Controle': 5, 'Auditoria': 4, 'Compliance': 5},
            'HealthBlock': {'Controle': 4, 'Auditoria': 5, 'Compliance': 4},
            'MedChain': {'Controle': 4, 'Auditoria': 4, 'Compliance': 4},
            'Framework BR': {'Controle': 5, 'Auditoria': 5, 'Compliance': 5},
            'HealthChain': {'Controle': 4, 'Auditoria': 4, 'Compliance': 4}
        }
        st.table(pd.DataFrame(governance_data))
        st.markdown("""
        #### Escala de Avaliação:
        - **5**: Excelente
        - **4**: Muito Bom
        - **3**: Bom
        - **2**: Regular
        - **1**: Necessita Melhorias
        """)
    
    # Final Comparative Analysis
    st.header("Análise Comparativa Final")
    final_scores = {
        'MedRec': {
            'Segurança': 4.5,
            'Interoperabilidade': 4.2,
            'Escalabilidade': 4.0,
            'Eficiência': 4.3,
            'Governança': 4.4
        },
        'HealthBlock': {
            'Segurança': 4.2,
            'Interoperabilidade': 4.0,
            'Escalabilidade': 4.5,
            'Eficiência': 4.1,
            'Governança': 4.2
        },
        'Framework Proposto': {
            'Segurança': 4.8,
            'Interoperabilidade': 4.5,
            'Escalabilidade': 4.3,
            'Eficiência': 4.4,
            'Governança': 4.6
        }
    }
    
    fig_final = create_final_radar(final_scores)
    st.plotly_chart(fig_final)
    
    # Conclusions and Recommendations
    st.header("Conclusões e Recomendações")
    conclusions = calculate_conclusions(final_scores)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Pontos Fortes")
        for strength in conclusions['strengths']:
            st.success(f"✓ {strength}")
    
    with col2:
        st.subheader("Oportunidades de Melhoria")
        for improvement in conclusions['improvements']:
            st.warning(f"⚠ {improvement}")
    
    # Detailed Metrics Explanation
    st.header("Explicação Detalhada das Métricas")
    with st.expander("Ver Fórmulas e Cálculos"):
        st.markdown("""
        ### Cálculo de Métricas Principais
        
        1. **Índice de Segurança Normalizado (ISN)**
        ```python
        ISN = (S_weight * S_score + P_weight * P_score) / (S_weight + P_weight)
        ```
        Onde:
        - S_weight: Peso da segurança (0.4)
        - S_score: Pontuação de segurança
        - P_weight: Peso da privacidade (0.3)
        - P_score: Pontuação de privacidade
        
        2. **Índice de Interoperabilidade (II)**
        ```python
        II = (API_score + STD_score + INT_score) / 3
        ```
        
        3. **Índice de Escalabilidade Ponderada (IEP)**
        ```python
        IEP = (TPS * 0.5) + (Latency * 0.3) + (Storage * 0.2)
        ```
        
        4. **Eficiência Energética Normalizada (EEN)**
        ```python
        EEN = 1 - (Energy_consumption / Max_energy_consumption)
        ```
        """)

def main():
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

if __name__ == "__main__":
    main()
