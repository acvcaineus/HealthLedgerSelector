import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_peso_caracteristica)
from utils import init_session_state

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
    
    if 'recommendation' in st.session_state and 'answers' in st.session_state:
        rec = st.session_state.recommendation
        answers = st.session_state.answers
        
        if 'evaluation_matrix' in rec:
            classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
            gini = calcular_gini(classes)
            entropy = calcular_entropia(classes)
            depth = calcular_profundidade_decisoria(list(range(len(answers))))
            
            total_nos = len(answers) * 2 + 1
            nos_podados = total_nos - len(answers) - 1
            pruning_metrics = calcular_pruning(total_nos, nos_podados)
            
            # Display metrics in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Métricas de Classificação")
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
                st.subheader("🌳 Métricas da Árvore")
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
            
            # Display metrics radar chart
            fig_radar = create_metrics_radar_chart(
                gini,
                entropy,
                depth / 10,  # Normalize to 0-1 range
                pruning_metrics['pruning_ratio']
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Pruning metrics details
            with st.expander("🔍 Detalhes das Métricas de Poda"):
                st.markdown(f"""
                ### Métricas de Poda Detalhadas
                
                1. **Taxa de Poda:** {pruning_metrics['pruning_ratio']:.2%}
                   - Proporção de nós removidos do modelo
                
                2. **Eficiência da Poda:** {pruning_metrics['eficiencia_poda']:.2%}
                   - Medida de quão eficiente foi o processo de poda
                
                3. **Impacto na Complexidade:** {pruning_metrics['impacto_complexidade']:.3f}
                   - Redução logarítmica na complexidade do modelo
                """)
            
            # Characteristic weights visualization
            st.subheader("⚖️ Pesos das Características")
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
            
            # Explanation of metrics
            with st.expander("ℹ️ Explicação das Métricas"):
                st.markdown("""
                ### Índice de Gini
                Mede a pureza da classificação. Valores próximos a 0 indicam melhor separação entre as classes.
                
                ### Entropia
                Mede a incerteza na decisão. Valores mais baixos indicam maior certeza nas recomendações.
                
                ### Profundidade da Árvore
                Indica a complexidade do processo decisório. Uma profundidade menor sugere um processo mais direto.
                
                ### Taxa de Poda
                Mostra quanto o modelo foi simplificado. Uma taxa maior indica maior otimização do processo.
                """)

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")

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
            'DLT Híbrida', 'DLT com Consenso Delegado', 'DLT com Consenso Delegado',
            'DLT com Consenso Delegado', 'DLT Pública', 'DLT Pública',
            'DLT Pública (Permissionless)'
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
        ]
    }
    df = pd.DataFrame(dlt_data)
    st.table(df)

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
