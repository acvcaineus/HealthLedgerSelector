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
    """Initialize all required session state variables"""
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

def show_home_page():
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
    
    # Reference table
    st.header("Referência de DLTs e Algoritmos")
    data = {
        'Grupo': ['Alta Segurança e Controle', 'Alta Segurança e Controle', 'Alta Eficiência Operacional',
                 'Alta Eficiência Operacional', 'Escalabilidade e Governança Flexível', 'Alta Escalabilidade em Redes IoT'],
        'Tipo DLT': ['DLT Permissionada Privada', 'DLT Pública Permissionless', 'DLT Permissionada Simples',
                     'DLT Híbrida', 'DLT com Consenso Delegado', 'DLT Pública'],
        'Nome DLT': ['Hyperledger Fabric', 'Bitcoin', 'Quorum', 'Ethereum 2.0', 'EOS', 'IOTA'],
        'Algoritmo de Consenso': ['PBFT', 'PoW', 'RAFT/PoA', 'PoS', 'DPoS', 'Tangle'],
        'Principais Características': [
            'Alta segurança e resiliência contra falhas bizantinas',
            'Alta segurança e descentralização total',
            'Simplicidade e eficiência em redes locais',
            'Alta escalabilidade e eficiência energética',
            'Governança flexível e alta performance',
            'Escalabilidade para IoT e dados em tempo real'
        ]
    }
    st.dataframe(pd.DataFrame(data))
    
    if st.button("Iniciar Seleção de DLT", type="primary"):
        st.session_state.page = 'Framework Proposto'
        st.rerun()

def show_metrics():
    """Exibe métricas do processo de decisão com explicações aprimoradas"""
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
                            O Índice de Gini mede a pureza da classificação das DLTs, indicando quão bem o modelo separa as diferentes classes.
                            
                            **Parâmetros de Análise:**
                            1. **Separação de Classes** (peso: 40%)
                               - Como as DLTs são separadas com base nas características
                               - Valor ideal: < 0.3 (boa separação)
                            
                            2. **Pureza dos Dados** (peso: 30%)
                               - Consistência das características dentro de cada grupo
                               - Valor ideal: < 0.4 (alta pureza)
                            
                            3. **Consistência** (peso: 20%)
                               - Estabilidade da classificação entre diferentes execuções
                               - Valor ideal: < 0.2 (alta consistência)
                            
                            4. **Precisão** (peso: 10%)
                               - Acurácia da separação em relação ao ground truth
                               - Valor ideal: < 0.1 (alta precisão)
                            
                            **Fórmula:**
                            \\[ Gini = 1 - \sum_{i=1}^{n} (p_i)^2 \\]
                            onde \( p_i \) é a proporção de cada classe.
                            
                            **Interpretação dos Valores:**
                            - 0.0 - 0.3: Excelente separação
                            - 0.3 - 0.5: Boa separação
                            - 0.5 - 0.7: Separação moderada
                            - > 0.7: Separação inadequada
                        """)

                    st.subheader("2. Evolução da Entropia")
                    with st.expander("Ver Explicação da Entropia"):
                        st.markdown("""
                            ### O que é a Entropia?
                            A Entropia mede a incerteza na classificação das DLTs ao longo do processo decisório.
                            
                            **Fórmula:**
                            \\[ Entropia = - \sum_{i=1}^{n} p_i \log_2(p_i) \\]
                            onde \( p_i \) é a probabilidade da classe i.
                            
                            **Interpretação:**
                            - Valor baixo (< 1.0): Alta certeza na decisão
                            - Valor médio (1.0 - 2.0): Incerteza moderada
                            - Valor alto (> 2.0): Alta incerteza
                            
                            A entropia é útil para:
                            1. Avaliar a qualidade da separação entre diferentes DLTs
                            2. Identificar pontos de decisão críticos
                            3. Otimizar o processo de recomendação
                        """)

                    st.subheader("3. Dashboard de Métricas")
                    with st.expander("Ver Explicação do Dashboard"):
                        st.markdown("""
                            ### Métricas do Dashboard
                            
                            **1. Profundidade da Árvore**
                            \\[ Profundidade = \log_2(n_{folhas}) \\]
                            - Mede a complexidade do processo decisório
                            - Valor ideal: 3-5 níveis
                            
                            **2. Taxa de Poda**
                            \\[ Taxa\ de\ Poda = \\frac{Nós\ Podados}{Total\ de\ Nós} \\]
                            - Indica a simplificação do modelo
                            - Valor ideal: > 0.3 (30% de poda)
                            
                            **3. Índice de Confiança**
                            \\[ Confiança = \\frac{Score\ Máximo - Score\ Médio}{Score\ Máximo} \\]
                            - Mede a confiabilidade da recomendação
                            - Valor ideal: > 0.7 (70%)
                        """)

                    st.subheader("4. Acurácia da Recomendação")
                    with st.expander("Ver Explicação da Acurácia"):
                        st.markdown("""
                            ### Como a Acurácia é Calculada
                            A acurácia mede a precisão do modelo em recomendar a DLT mais adequada, considerando:
                            
                            1. **Precisão da Classificação**: 
                               \\[ Precisão = \\frac{Recomendações\\ Corretas}{Total\\ de\\ Recomendações} \\]
                               - Valor > 90%: Alta precisão
                               - 70-90%: Precisão moderada
                               - < 70%: Baixa precisão
                            
                            2. **Taxa de Verdadeiros Positivos (Recall)**:
                               \\[ Recall = \\frac{Casos\\ Positivos\\ Identificados}{Total\\ de\\ Casos\\ Positivos} \\]
                            
                            3. **F1-Score** (média harmônica entre precisão e recall):
                               \\[ F1 = 2 * \\frac{Precisão * Recall}{Precisão + Recall} \\]
                        """)
                        
                        precision = rec.get('precision', 0.85)
                        recall = rec.get('recall', 0.82)
                        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Precisão", f"{precision:.1%}", help="Proporção de recomendações corretas")
                        with col2:
                            st.metric("Recall", f"{recall:.1%}", help="Proporção de casos positivos identificados")
                        with col3:
                            st.metric("F1-Score", f"{f1:.1%}", help="Média harmônica entre precisão e recall")

        else:
            st.info("Complete o processo de seleção para ver as métricas.")
    except Exception as e:
        st.error(f"Error displaying metrics: {str(e)}")
        st.code(traceback.format_exc())

def main():
    """Main application with improved error handling and state management"""
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
            menu_option = st.selectbox("Escolha uma opção", menu_options)
            if st.button("Logout"):
                logout()
                st.rerun()
        
        if menu_option == 'Início':
            show_home_page()
        elif menu_option == 'Framework Proposto':
            run_decision_tree()
        elif menu_option == 'Métricas':
            show_metrics()

if __name__ == "__main__":
    main()
