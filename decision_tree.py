import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import math
from decision_logic import get_recommendation, consensus_algorithms, consensus_groups, compare_algorithms
from database import save_recommendation
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_peso_caracteristica, get_metric_explanation)
from dlt_data import questions

def show_phase_progress():
    st.markdown("### Progresso por Fase")
    
    # Create connected circles visualization with custom CSS
    st.markdown('''
        <style>
            .phase-container {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                margin: 20px 0;
            }
            .phase-circle {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                position: relative;
            }
            .phase-name {
                text-align: center;
                margin-top: 8px;
                font-size: 14px;
            }
            .phase-progress {
                text-align: center;
                color: #666;
                font-size: 12px;
            }
            .connection-line {
                flex-grow: 1;
                height: 2px;
                background-color: #CCC;
                position: relative;
                top: -30px;
            }
        </style>
    ''', unsafe_allow_html=True)
    
    # Create a row of connected circles
    st.markdown('<div class="phase-container">', unsafe_allow_html=True)
    
    phases = {
        "Aplicação": "#2ECC71",
        "Consenso": "#3498DB",
        "Infraestrutura": "#9B59B6",
        "Internet": "#E74C3C"
    }
    
    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    
    for idx, (phase_name, color) in enumerate(phases.items()):
        # Get questions for this phase
        phase_questions = [q for q in questions if q["phase"] == phase_name]
        answered = len([q for q in phase_questions if q["id"] in st.session_state.answers])
        total = len(phase_questions)
        
        # Create circle with phase name and progress
        opacity = "1" if phase_name == current_phase else "0.7"
        st.markdown(f'''
            <div style="text-align: center;">
                <div class="phase-circle" style="background-color: {color}; opacity: {opacity};">●</div>
                <div class="phase-name">{phase_name}</div>
                <div class="phase-progress">({answered}/{total})</div>
            </div>
            {('<div class="connection-line"></div>' if idx < len(phases)-1 else '')}
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_dlt_matrix(evaluation_matrix):
    dlt_scores = pd.DataFrame(
        {dlt: data['metrics'] for dlt, data in evaluation_matrix.items()}
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

def run_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
        
    st.title("Framework de Seleção de DLT")
    show_phase_progress()
    
    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break
            
    if current_question:
        st.subheader(f"Fase: {current_question['phase']}")
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
                
    else:
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        
        recommendation = get_recommendation(st.session_state.answers, weights)
        
        if recommendation and recommendation.get('dlt') != "Não disponível":
            st.success("Recomendação Gerada com Sucesso!")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("DLT Recomendada")
                st.write(f"**Tipo de DLT:** {recommendation.get('dlt', 'Não disponível')}")
                st.write(f"**Algoritmo de Consenso:** {recommendation.get('consensus', 'Não disponível')}")
                st.write(f"**Grupo de Consenso:** {recommendation.get('consensus_group', 'Não disponível')}")
                st.write(f"**Descrição:** {recommendation.get('group_description', 'Não disponível')}")
            
            with col2:
                if st.session_state.get('authenticated') and st.session_state.get('username'):
                    if st.button("💾 Salvar Recomendação"):
                        try:
                            save_recommendation(
                                st.session_state.username,
                                "Healthcare DLT Selection",
                                recommendation
                            )
                            st.success("✅ Recomendação salva com sucesso!")
                        except Exception as e:
                            st.error(f"Erro ao salvar recomendação: {str(e)}")
                else:
                    st.info("📝 Faça login para salvar recomendações")
            
            show_dlt_matrix(recommendation.get('evaluation_matrix', {}))
