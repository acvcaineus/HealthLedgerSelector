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

def show_home_page():
    """Display home page with reference table and start button"""
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao sistema de seleção de DLT para projetos de saúde.")
    
    # Add "Iniciar Questionário" button with prominent styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <style>
            div.stButton > button {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 15px 30px;
                border-radius: 10px;
                border: none;
                width: 100%;
            }
            div.stButton > button:hover {
                background-color: #45a049;
            }
            </style>
        """, unsafe_allow_html=True)
        if st.button("🚀 Iniciar Questionário", help="Clique para começar o processo de seleção de DLT"):
            st.session_state.page = 'Framework Proposto'
            st.experimental_rerun()
    
    st.markdown("## Tabela de Referência DLT")
    
    # Updated DLT reference data with new consensus algorithms
    dlt_data = [
        ['Hyperledger Fabric', 'DLT Permissionada Privada', 'Alta Segurança e Controle dos dados sensíveis', 'PBFT/RAFT/IBFT', 
         'Alta tolerância a falhas, finalidade imediata, adequado para redes permissionadas', 'Sistemas de saúde da Estônia: Proteção da integridade e privacidade dos registros médicos. Redes de provedores de saúde com necessidade de forte consistência'],
        ['Hyperledger Sawtooth', 'DLT Permissionada Privada', 'Alta Eficiência e Controle', 'PoET', 
         'Eficiente em recursos, eleição justa de líderes, adequado para redes permissionadas', 'Gestão da cadeia de suprimentos médicos, rastreamento de medicamentos e equipamentos'],
        ['EOS', 'DLT Pública', 'Alta Escalabilidade', 'DPoS', 
         'Alto throughput, eficiência energética, validação delegada', 'Sistemas de gestão de dados de saúde em larga escala, registros médicos distribuídos'],
        ['TRON', 'DLT Pública', 'Alta Escalabilidade', 'DPoS', 
         'Alto throughput, eficiência energética, validação delegada', 'Gestão de dados de saúde em larga escala, interoperabilidade entre sistemas'],
        ['Corda', 'DLT Permissionada Simples', 'Alta Segurança e Controle dos dados sensíveis', 'RAFT',
         'Consenso baseado em líderes, adequado para redes privadas', 'ProCredEx: Validação de credenciais de profissionais de saúde nos EUA'],
        ['Quorum', 'DLT Híbrida', 'Escalabilidade e Governança Flexível', 'RAFT/IBFT',
         'Flexibilidade de governança, consenso eficiente para redes híbridas', 'Chronicled (Mediledger Project): Rastreamento de medicamentos na cadeia farmacêutica'],
        ['VeChain', 'DLT Híbrida', 'Alta Eficiência Operacional em redes locais', 'PoA',
         'Alta eficiência, baixa latência, consenso delegado a validadores autorizados', 'FarmaTrust: Rastreamento de medicamentos e combate à falsificação'],
        ['IOTA', 'DLT com Consenso Delegado', 'Alta Escalabilidade em Redes IoT', 'Tangle',
         'Escalabilidade alta, arquitetura sem blocos, adequada para IoT', 'Patientory: Compartilhamento seguro de dados de pacientes via IoT'],
        ['Ripple (XRP Ledger)', 'DLT com Consenso Delegado', 'Alta Eficiência Operacional em redes locais', 'Ripple Consensus Algorithm',
         'Consenso rápido, baixa latência, baseado em validadores confiáveis', 'Change Healthcare: Gestão de ciclo de receita e processamento de transações'],
        ['Stellar', 'DLT com Consenso Delegado', 'Alta Eficiência Operacional em redes locais', 'SCP',
         'Consenso baseado em quórum, alta eficiência, tolerância a falhas', 'MedicalChain: Controle de dados de pacientes e telemedicina'],
        ['Bitcoin', 'DLT Pública', 'Alta Segurança e Descentralização de dados críticos', 'PoW',
         'Segurança alta, descentralização, consumo elevado de energia', 'Guardtime: Rastreamento de dados de saúde em redes públicas'],
        ['Ethereum (PoW)', 'DLT Pública', 'Alta Segurança e Descentralização de dados críticos', 'PoW',
         'Segurança alta, descentralização, escalabilidade limitada, alto custo', 'Embleema: Desenvolvimento de medicamentos e ensaios clínicos'],
        ['Ethereum 2.0 (PoS)', 'DLT Pública Permissionless', 'Escalabilidade e Governança Flexível', 'PoS',
         'Eficiência energética, incentivo à participação, redução da centralização', 'MTBC: Gestão de registros eletrônicos de saúde (EHR)']
    ]
    
    # Create DataFrame
    df = pd.DataFrame(dlt_data, columns=[
        'DLT', 'Tipo de DLT', 'Grupo de Algoritmo', 
        'Algoritmo de Consenso', 'Principais Características', 
        'Estudos de Uso'
    ])
    
    # Enhanced table styling
    st.markdown("""
        <style>
        .dataframe {
            font-size: 14px !important;
            width: 100% !important;
        }
        .dataframe th {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: bold !important;
            text-align: center !important;
            padding: 12px 8px !important;
            white-space: normal !important;
        }
        .dataframe td {
            text-align: left !important;
            padding: 10px 8px !important;
            white-space: normal !important;
            vertical-align: top !important;
        }
        .dataframe tr:nth-child(even) {
            background-color: #f2f2f2 !important;
        }
        .dataframe tr:hover {
            background-color: #ddd !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display the table with improved height and width settings
    st.dataframe(
        df.style.set_properties(**{
            'white-space': 'normal',
            'height': 'auto',
            'text-align': 'left',
            'vertical-align': 'top'
        }),
        height=600,
        use_container_width=True
    )

def show_metrics():
    """Display metrics with improved layout and concise explanations"""
    st.header("Métricas Técnicas do Processo de Decisão")
    
    try:
        if 'recommendation' in st.session_state:
            with st.spinner('Carregando métricas...'):
                rec = st.session_state.recommendation
                if 'evaluation_matrix' in rec:
                    classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
                    gini = calcular_gini(classes)
                    entropy = calcular_entropia(classes)
                    
                    # Metrics Sections with enhanced explanations
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # 1. Gini Index with improved visualization
                    with st.expander("1. Índice de Gini"):
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.latex(r"Gini = 1 - \sum_{i=1}^{n} p_i^2")
                            st.markdown("""
                                **Interpretação Rápida:**
                                - 🟢 0.0-0.3: Excelente separação
                                - 🟡 0.3-0.6: Separação moderada
                                - 🔴 0.6-1.0: Alta mistura
                                
                                **Significado:**
                                O índice de Gini mede a pureza da classificação. 
                                Quanto menor o valor, melhor a separação entre as classes.
                            """)
                        with col2:
                            st.metric(
                                "Valor do Índice de Gini",
                                f"{gini:.3f}",
                                delta=("Boa separação" if gini < 0.3 else 
                                      "Separação moderada" if gini < 0.6 else 
                                      "Alta mistura")
                            )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # 2. Entropy with enhanced explanation
                    with st.expander("2. Entropia"):
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.latex(r"Entropia = -\sum_{i=1}^{n} p_i \log_2(p_i)")
                            st.markdown("""
                                **Interpretação Rápida:**
                                - 🟢 <1.0: Alta certeza
                                - 🟡 1.0-2.0: Certeza moderada
                                - 🔴 >2.0: Alta incerteza
                                
                                **Significado:**
                                A entropia mede a incerteza na decisão.
                                Valores menores indicam maior confiança na recomendação.
                            """)
                        with col2:
                            st.metric(
                                "Valor da Entropia",
                                f"{entropy:.3f}",
                                delta=("Alta certeza" if entropy < 1.0 else 
                                      "Certeza moderada" if entropy < 2.0 else 
                                      "Alta incerteza")
                            )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # 3. Tree Metrics with enhanced visualization
                    with st.expander("3. Métricas da Árvore"):
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.markdown("""
                                **Métricas Principais:**
                                1. **Profundidade da Árvore**
                                - Mede a complexidade do processo decisório
                                - Valores menores indicam processo mais simples
                                
                                2. **Taxa de Poda**
                                - Indica a eficiência da simplificação
                                - Valores maiores indicam melhor otimização
                                
                                3. **Índice de Confiança**
                                - Mede a confiabilidade da recomendação
                                - Valores > 0.7 indicam alta confiabilidade
                            """)
                        with col2:
                            depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
                            total_nos = len(st.session_state.answers) * 2 + 1
                            nos_podados = total_nos - len(st.session_state.answers) - 1
                            pruning_ratio = calcular_pruning(total_nos, nos_podados)
                            confidence = rec.get('confidence_value', 0.0)
                            
                            # Display metrics with improved formatting
                            st.metric("Profundidade", f"{depth:.2f}", 
                                    delta="Baixa" if depth < 3 else "Média" if depth < 5 else "Alta")
                            st.metric("Taxa de Poda", f"{pruning_ratio:.2%}", 
                                    delta="Boa" if pruning_ratio > 0.5 else "Regular")
                            st.metric("Confiança", f"{confidence:.2%}", 
                                    delta="Alta" if confidence > 0.7 else "Média")
        else:
            st.info("Complete o processo de seleção para ver as métricas.")
    except Exception as e:
        st.error(f"Error displaying metrics: {str(e)}")
        st.code(traceback.format_exc())

def main():
    """Main application function"""
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
            menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Perfil', 'Logout']
            
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

if __name__ == "__main__":
    main()
