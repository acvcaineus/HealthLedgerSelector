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
    
    phases = {
        "Aplicação": "#2ECC71",
        "Consenso": "#3498DB",
        "Infraestrutura": "#9B59B6",
        "Internet": "#E74C3C"
    }
    
    st.markdown('<div class="phase-container">', unsafe_allow_html=True)
    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    
    for idx, (phase_name, color) in enumerate(phases.items()):
        phase_questions = [q for q in questions if q["phase"] == phase_name]
        answered = len([q for q in phase_questions if q["id"] in st.session_state.answers])
        total = len(phase_questions)
        
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
    
    # Add warning about restarting
    st.warning("⚠️ Atenção: Reiniciar o processo irá apagar todas as respostas já fornecidas!")
    if st.button("🔄 Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

    st.markdown("---")
    
    # Show DLT Selection Table
    st.subheader("Tabela de Seleção de DLT")
    dlt_df = pd.DataFrame({
        'Grupo': ['Alta Segurança e Controle', 'Alta Eficiência Operacional', 'Escalabilidade e Governança', 'Alta Escalabilidade IoT'],
        'DLTs': ['Hyperledger Fabric, Bitcoin', 'Quorum, VeChain', 'Ethereum 2.0, EOS', 'IOTA'],
        'Algoritmos': ['PBFT, PoW', 'RAFT, PoA', 'PoS, DPoS', 'Tangle'],
        'Características': ['Segurança máxima, Privacidade', 'Eficiência, Baixa latência', 'Escalabilidade, Flexibilidade', 'IoT, Tempo real']
    })
    st.table(dlt_df)
    
    st.markdown("---")
    
    # Create the dynamic decision tree visualization
    st.subheader("Árvore de Decisão")
    
    # Get current phase and progress
    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    total_questions = len(questions)
    answered_questions = len(st.session_state.answers)
    
    # Show phase progress
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### Fase Atual: {current_phase}")
        progress = answered_questions / total_questions
        st.progress(progress, text=f"Progresso: {int(progress * 100)}%")
    
    with col2:
        st.metric(
            "Questões Respondidas",
            f"{answered_questions}/{total_questions}",
            help="Número de questões respondidas vs. total"
        )
    
    # Show current phase explanation
    phase_explanations = {
        "Aplicação": "Avaliação dos requisitos básicos e características da aplicação",
        "Consenso": "Definição do mecanismo de consenso e validação",
        "Infraestrutura": "Análise dos requisitos de infraestrutura e recursos",
        "Internet": "Avaliação da conectividade e interoperabilidade",
        "Completo": "Todas as fases foram completadas"
    }
    st.info(phase_explanations.get(current_phase, ""))
    
    # Show phase progress visualization
    show_phase_progress()
    
    # Display current question or recommendation
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
            
            # Calculate metrics
            if 'evaluation_matrix' in recommendation:
                classes = {k: v['score'] for k, v in recommendation['evaluation_matrix'].items()}
                gini = calcular_gini(classes)
                entropy = calcular_entropia(classes)
                depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
                total_nos = len(st.session_state.answers) * 2 + 1
                nos_podados = total_nos - len(st.session_state.answers) - 1
                pruning_metrics = calcular_pruning(total_nos, nos_podados)
            
            # Display recommendation with metrics
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader("DLT Recomendada")
                st.write(f"**Tipo de DLT:** {recommendation.get('dlt', 'Não disponível')}")
                st.write(f"**Algoritmo de Consenso:** {recommendation.get('consensus', 'Não disponível')}")
                st.write(f"**Grupo de Consenso:** {recommendation.get('consensus_group', 'Não disponível')}")
                st.write(f"**Descrição:** {recommendation.get('group_description', 'Não disponível')}")
                
                # Display metrics
                st.subheader("Métricas de Decisão")
                metrics_col1, metrics_col2 = st.columns(2)
                with metrics_col1:
                    st.metric("Índice de Gini", f"{gini:.3f}")
                    st.metric("Profundidade da Árvore", f"{depth:.1f}")
                with metrics_col2:
                    st.metric("Entropia", f"{entropy:.3f}")
                    st.metric("Taxa de Poda", f"{pruning_metrics['pruning_ratio']:.2%}")
            
            with col2:
                if st.session_state.get('authenticated') and st.session_state.get('username'):
                    if st.button("💾 Salvar Recomendação", help="Clique para salvar esta recomendação"):
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
            
            # Show evaluation matrix
            show_dlt_matrix(recommendation.get('evaluation_matrix', {}))
