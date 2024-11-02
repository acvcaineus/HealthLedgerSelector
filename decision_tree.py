import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import math
from decision_logic import get_recommendation, consensus_algorithms, consensus_groups, compare_algorithms
from database import save_recommendation
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_peso_caracteristica, get_metric_explanation)
from dlt_data import questions

def get_current_phase(questions, answers):
    try:
        return next((q["phase"] for q in questions if q["id"] not in answers), "Completo")
    except (KeyError, StopIteration):
        return "Completo"

def run_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")
    
    # Add phase tracking
    phases = {
        "Aplicação": ["privacy", "integration"],
        "Consenso": ["data_volume", "network_security"],
        "Infraestrutura": ["energy_efficiency", "scalability"],
        "Internet": ["governance_flexibility", "interoperability"]
    }
    
    # Show current phase and progress
    current_phase = get_current_phase(questions, st.session_state.answers)
    total_questions = len(questions)
    answered_questions = len(st.session_state.answers)
    progress = answered_questions / total_questions
    
    # Display progress
    st.markdown(f"### Fase Atual: {current_phase}")
    st.progress(progress, text=f"Progresso: {progress:.0%}")
    
    # Show phase explanation
    phase_explanations = {
        "Aplicação": "Avaliação dos requisitos básicos e características da aplicação",
        "Consenso": "Definição do mecanismo de consenso e validação",
        "Infraestrutura": "Análise dos requisitos de infraestrutura e recursos",
        "Internet": "Avaliação da conectividade e interoperabilidade",
        "Completo": "Todas as fases foram completadas"
    }
    
    st.info(phase_explanations.get(current_phase, ""))

    # Display current phase questions
    st.subheader("Perguntas da Fase Atual")
    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    if current_question:
        with st.expander("Detalhes da Pergunta", expanded=True):
            st.subheader(f"Característica: {current_question.get('characteristic', 'Não especificada')}")
            st.info(f"Dica: {current_question.get('tooltip', 'Não disponível')}")
            response = st.radio(
                current_question.get("text", "Pergunta não disponível"),
                current_question.get("options", ["Sim", "Não"])
            )

            if st.button("Próxima Pergunta"):
                st.session_state.answers[current_question["id"]] = response
                st.experimental_rerun()

    if len(st.session_state.answers) == len(questions):
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        st.session_state.recommendation = get_recommendation(st.session_state.answers, weights)
        
        # Display recommendation
        rec = st.session_state.recommendation
        if rec and rec.get('dlt', "Não disponível") != "Não disponível":
            st.success("Recomendação Gerada com Sucesso!")
            
            # Create columns for the recommendation display
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("DLT Recomendada")
                st.write(f"**Tipo de DLT:** {rec.get('dlt', 'Não disponível')}")
                st.write(f"**Algoritmo de Consenso:** {rec.get('consensus', 'Não disponível')}")
                st.write(f"**Grupo de Consenso:** {rec.get('consensus_group', 'Não disponível')}")
                st.write(f"**Descrição:** {rec.get('group_description', 'Não disponível')}")
            
            with col2:
                # Add Save Recommendation button only for authenticated users
                if st.session_state.get('authenticated') and st.session_state.get('username'):
                    if st.button("💾 Salvar Recomendação", 
                               help="Clique para salvar esta recomendação no seu perfil"):
                        try:
                            save_recommendation(
                                st.session_state.username,
                                "Healthcare DLT Selection",
                                rec
                            )
                            st.success("✅ Recomendação salva com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao salvar recomendação: {str(e)}")
                else:
                    st.info("📝 Faça login para salvar recomendações")
            
            # Display confidence metrics
            st.subheader("Métricas de Confiança")
            conf_col1, conf_col2, conf_col3 = st.columns(3)
            
            with conf_col1:
                st.metric(
                    "Confiança Geral",
                    f"{rec.get('confidence_value', 0):.2%}",
                    help="Nível geral de confiança na recomendação"
                )
            
            with conf_col2:
                st.metric(
                    "Alinhamento",
                    f"{rec.get('confidence_components', {}).get('Alinhamento', 0):.2%}",
                    help="Alinhamento com os requisitos fornecidos"
                )
            
            with conf_col3:
                st.metric(
                    "Consistência",
                    f"{rec.get('confidence_components', {}).get('Consistência', 0):.2%}",
                    help="Consistência das respostas fornecidas"
                )

            # Add evaluation matrices
            st.markdown("---")
            st.subheader("Matrizes de Avaliação")
            
            # DLT Matrix
            with st.expander("Matriz de Avaliação de DLTs", expanded=True):
                if 'evaluation_matrix' in rec:
                    dlt_scores = pd.DataFrame(
                        {dlt: data['metrics'] for dlt, data in rec['evaluation_matrix'].items()}
                    ).T
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=dlt_scores.values,
                        x=dlt_scores.columns,
                        y=dlt_scores.index,
                        colorscale='Viridis',
                        hovertemplate="DLT: %{y}<br>Métrica: %{x}<br>Score: %{z:.2f}<extra></extra>"
                    ))
                    fig.update_layout(title="Matriz de Avaliação das DLTs")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("""
                    ### Como interpretar a Matriz de DLTs:
                    - Cores mais escuras indicam scores mais altos
                    - Cada linha representa uma DLT diferente
                    - Cada coluna representa uma característica avaliada
                    - O mouse sobre as células mostra os valores exatos
                    """)
            
            # Consensus Group Matrix
            with st.expander("Matriz de Grupos de Algoritmos", expanded=True):
                if 'consensus_group' in rec:
                    group_data = consensus_groups[rec['consensus_group']]['characteristics']
                    group_df = pd.DataFrame([group_data])
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=group_df.values,
                        x=group_df.columns,
                        y=[rec['consensus_group']],
                        colorscale='Viridis',
                        hovertemplate="Grupo: %{y}<br>Métrica: %{x}<br>Score: %{z:.2f}<extra></extra>"
                    ))
                    fig.update_layout(title=f"Características do Grupo {rec['consensus_group']}")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown(f"""
                    ### Características do Grupo de Consenso:
                    - **Grupo:** {rec['consensus_group']}
                    - **Descrição:** {consensus_groups[rec['consensus_group']]['description']}
                    - **Algoritmos:** {', '.join(consensus_groups[rec['consensus_group']]['algorithms'])}
                    """)
