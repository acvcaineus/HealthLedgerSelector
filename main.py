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

def create_gini_radar(gini):
    """Create radar chart for Gini index visualization"""
    try:
        categories = ['Separação de Classes', 'Pureza dos Dados', 'Consistência', 'Precisão']
        fig = go.Figure()
        
        # Add trace for Gini index
        fig.add_trace(go.Scatterpolar(
            r=[1-gini, gini, 1-gini, gini],
            theta=categories,
            fill='toself',
            name='Índice de Gini',
            line=dict(color='#1f77b4')
        ))
        
        # Update layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickfont=dict(size=10),
                    tickangle=45
                ),
                angularaxis=dict(
                    tickfont=dict(size=10)
                )
            ),
            showlegend=True,
            title={
                'text': "Análise do Índice de Gini",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            margin=dict(t=100, b=50)
        )
        return fig
    except Exception as e:
        st.error(f"Error creating Gini radar: {str(e)}")
        return None

def create_entropy_graph(answers):
    """Create entropy evolution graph"""
    try:
        entropy_values = []
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        
        for i in range(len(answers)):
            partial_answers = dict(list(answers.items())[:i+1])
            recommendation = get_recommendation(partial_answers, weights)
            classes = {k: v['score'] for k, v in recommendation['evaluation_matrix'].items()}
            entropy_values.append(calcular_entropia(classes))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, len(entropy_values) + 1)),
            y=entropy_values,
            mode='lines+markers',
            name='Evolução da Entropia',
            line=dict(color='#2ecc71', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title={
                'text': "Evolução da Entropia Durante o Processo Decisório",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Número de Perguntas Respondidas",
            yaxis_title="Entropia (bits)",
            margin=dict(t=100, b=50)
        )
        return fig
    except Exception as e:
        st.error(f"Error creating entropy graph: {str(e)}")
        return None

def create_metrics_dashboard(depth, pruning_ratio, confidence):
    """Create metrics dashboard with gauges"""
    try:
        fig = go.Figure()
        
        # Add depth gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=depth,
            title={'text': "Profundidade da Árvore"},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': "#1f77b4"},
                'steps': [
                    {'range': [0, 3], 'color': "#c8e6c9"},
                    {'range': [3, 7], 'color': "#a5d6a7"},
                    {'range': [7, 10], 'color': "#81c784"}
                ]
            },
            domain={'row': 0, 'column': 0}
        ))
        
        # Add pruning ratio gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=pruning_ratio * 100,
            title={'text': "Taxa de Poda (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#2ecc71"},
                'steps': [
                    {'range': [0, 30], 'color': "#ffccbc"},
                    {'range': [30, 70], 'color': "#ffab91"},
                    {'range': [70, 100], 'color': "#ff8a65"}
                ]
            },
            domain={'row': 0, 'column': 1}
        ))
        
        # Add confidence gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=confidence * 100,
            title={'text': "Confiança (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#e74c3c"},
                'steps': [
                    {'range': [0, 30], 'color': "#b3e5fc"},
                    {'range': [30, 70], 'color': "#81d4fa"},
                    {'range': [70, 100], 'color': "#4fc3f7"}
                ]
            },
            domain={'row': 0, 'column': 2}
        ))
        
        fig.update_layout(
            grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
            title={
                'text': "Dashboard de Métricas da Árvore de Decisão",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            margin=dict(t=100, b=50, l=50, r=50)
        )
        return fig
    except Exception as e:
        st.error(f"Error creating metrics dashboard: {str(e)}")
        return None

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
    
    # Load reference data
    dlt_data = [
        ['Hyperledger Fabric', 'DLT Permissionada Privada', 'Alta Segurança e Controle dos dados sensíveis', 'RAFT/IBFT', 
         'Alta tolerância a falhas, consenso rápido em ambientes permissionados', 'Guardtime: Aplicado em sistemas de saúde da Estônia'],
        ['Corda', 'DLT Permissionada Simples', 'Alta Segurança e Controle dos dados sensíveis', 'RAFT',
         'Consenso baseado em líderes, adequado para redes privadas', 'ProCredEx: Validação de credenciais de profissionais de saúde nos EUA'],
        ['Quorum', 'DLT Híbrida', 'Escalabilidade e Governança Flexível', 'RAFT/IBFT',
         'Flexibilidade de governança, consenso eficiente para redes híbridas', 'Chronicled (Mediledger Project): Rastreamento de medicamentos'],
        ['VeChain', 'DLT Híbrida', 'Alta Eficiência Operacional em redes locais', 'PoA',
         'Alta eficiência, baixa latência, consenso delegado a validadores autorizados', 'FarmaTrust: Rastreamento de medicamentos'],
        ['IOTA', 'DLT com Consenso Delegado', 'Alta Escalabilidade em Redes IoT', 'Tangle',
         'Escalabilidade alta, arquitetura sem blocos, adequada para IoT', 'Patientory: Compartilhamento de dados via IoT'],
        ['Ripple', 'DLT com Consenso Delegado', 'Alta Eficiência Operacional em redes locais', 'Ripple Consensus Algorithm',
         'Consenso rápido, baixa latência, baseado em validadores confiáveis', 'Change Healthcare: Gestão de ciclo de receita'],
        ['Stellar', 'DLT com Consenso Delegado', 'Alta Eficiência Operacional em redes locais', 'SCP',
         'Consenso baseado em quórum, alta eficiência, tolerância a falhas', 'MedicalChain: Controle de dados e telemedicina'],
        ['Bitcoin', 'DLT Pública', 'Alta Segurança e Descentralização de dados críticos', 'PoW',
         'Segurança alta, descentralização, consumo elevado de energia', 'Guardtime: Rastreamento de dados de saúde'],
        ['Ethereum 2.0', 'DLT Pública Permissionless', 'Escalabilidade e Governança Flexível', 'PoS',
         'Eficiência energética, incentivo à participação, redução da centralização', 'MTBC: Gestão de registros eletrônicos']
    ]
    
    # Create DataFrame
    df = pd.DataFrame(dlt_data, columns=[
        'DLT', 'Tipo de DLT', 'Grupo de Algoritmo', 
        'Algoritmo de Consenso', 'Principais Características', 
        'Estudos de Uso'
    ])
    
    # Display styled table
    st.markdown("""
        <style>
        .dataframe {
            font-size: 14px !important;
        }
        .dataframe th {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: bold !important;
            text-align: center !important;
        }
        .dataframe td {
            text-align: left !important;
            padding: 8px !important;
        }
        .dataframe tr:nth-child(even) {
            background-color: #f2f2f2 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(df, height=400, use_container_width=True)

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
                    
                    # Add spacing between sections
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # 1. Gini Index with improved layout
                    with st.expander("1. Índice de Gini"):
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.latex(r"Gini = 1 - \sum_{i=1}^{n} p_i^2")
                            st.markdown("""
                                **Interpretação Rápida:**
                                - 🟢 0.0-0.3: Excelente separação
                                - 🟡 0.3-0.6: Separação moderada
                                - 🔴 0.6-1.0: Alta mistura
                            """)
                        with col2:
                            gini_fig = create_gini_radar(gini)
                            if gini_fig:
                                st.plotly_chart(gini_fig, use_container_width=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # 2. Entropy with improved layout
                    with st.expander("2. Entropia"):
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.latex(r"Entropia = -\sum_{i=1}^{n} p_i \log_2(p_i)")
                            st.markdown("""
                                **Interpretação Rápida:**
                                - 🟢 <1.0: Alta certeza
                                - 🟡 1.0-2.0: Certeza moderada
                                - 🔴 >2.0: Alta incerteza
                            """)
                        with col2:
                            entropy_fig = create_entropy_graph(st.session_state.answers)
                            if entropy_fig:
                                st.plotly_chart(entropy_fig, use_container_width=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # 3. Tree Metrics with improved layout
                    with st.expander("3. Métricas da Árvore"):
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.markdown("""
                                **Fórmulas:**
                            """)
                            st.latex(r"Profundidade = \frac{\sum_{i=1}^{n} nivel_i}{n}")
                            st.latex(r"Taxa_{poda} = \frac{nos_{total} - nos_{podados}}{nos_{total}}")
                            st.latex(r"Confianca = \frac{max_{score} - mean_{score}}{max_{score}}")
                            st.markdown("""
                                **Significado:**
                                - Profundidade: Complexidade da árvore
                                - Taxa de Poda: Eficiência da simplificação
                                - Confiança: Certeza da recomendação
                            """)
                        with col2:
                            depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
                            total_nos = len(st.session_state.answers) * 2 + 1
                            nos_podados = total_nos - len(st.session_state.answers) - 1
                            pruning_ratio = calcular_pruning(total_nos, nos_podados)
                            confidence = rec.get('confidence_value', 0.0)
                            
                            metrics_fig = create_metrics_dashboard(depth, pruning_ratio, confidence)
                            if metrics_fig:
                                st.plotly_chart(metrics_fig, use_container_width=True)
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
