import streamlit as st
import plotly.graph_objects as go
import math
from decision_logic import get_recommendation, consensus_algorithms, consensus_groups, compare_algorithms
from database import save_recommendation
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_peso_caracteristica, get_metric_explanation)
from dlt_data import questions

def run_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")

    st.warning("⚠️ Atenção: Reiniciar o processo irá apagar todas as respostas já fornecidas!")
    if st.button("🔄 Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

    st.markdown("---")
    
    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    progress = len(st.session_state.answers) / len(questions)
    
    st.markdown(f"### Fase Atual: {current_phase}")
    st.progress(progress)

    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    if current_question:
        st.subheader(f"Característica: {current_question['characteristic']}")
        st.info(f"Dica: {current_question['tooltip']}")
        response = st.radio(
            current_question["text"],
            current_question["options"]
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
        if rec and rec['dlt'] != "Não disponível":
            st.success("Recomendação Gerada com Sucesso!")
            
            # Create columns for the recommendation display
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("DLT Recomendada")
                st.write(f"**Tipo de DLT:** {rec['dlt']}")
                st.write(f"**Algoritmo de Consenso:** {rec['consensus']}")
                st.write(f"**Grupo de Consenso:** {rec['consensus_group']}")
                st.write(f"**Descrição:** {rec['group_description']}")
            
            with col2:
                # Add Save Recommendation button only for authenticated users
                if st.session_state.get('authenticated') and st.session_state.get('username'):
                    if st.button("💾 Salvar Recomendação", 
                               help="Clique para salvar esta recomendação no seu perfil"):
                        # Save the recommendation
                        save_recommendation(
                            st.session_state.username,
                            "Healthcare DLT Selection",
                            rec
                        )
                        st.success("✅ Recomendação salva com sucesso!")
                else:
                    st.info("📝 Faça login para salvar recomendações")
            
            # Display confidence metrics
            st.subheader("Métricas de Confiança")
            conf_col1, conf_col2, conf_col3 = st.columns(3)
            
            with conf_col1:
                st.metric(
                    "Confiança Geral",
                    f"{rec['confidence_value']:.2%}",
                    help="Nível geral de confiança na recomendação"
                )
            
            with conf_col2:
                st.metric(
                    "Alinhamento",
                    f"{rec['confidence_components'].get('Alinhamento', 0):.2%}",
                    help="Alinhamento com os requisitos fornecidos"
                )
            
            with conf_col3:
                st.metric(
                    "Consistência",
                    f"{rec['confidence_components'].get('Consistência', 0):.2%}",
                    help="Consistência das respostas fornecidas"
                )
