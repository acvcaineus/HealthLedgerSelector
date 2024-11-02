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
    st.markdown("### Camadas da Pilha de Shermin")
    
    # Create custom CSS for the layer visualization
    st.markdown('''
        <style>
            .layer-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 20px;
                margin: 20px 0;
            }
            .layer {
                width: 200px;
                height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                position: relative;
            }
            .diamond {
                transform: rotate(45deg);
                width: 80px;
                height: 80px;
                margin: -10px;
            }
            .layer-text {
                transform: rotate(-45deg);
                text-align: center;
            }
            .layer-progress {
                position: absolute;
                bottom: -20px;
                text-align: center;
                color: #666;
            }
            .connection-line {
                width: 2px;
                height: 20px;
                background-color: #CCC;
                margin: 0 auto;
            }
        </style>
    ''', unsafe_allow_html=True)
    
    # Define phases and their colors
    phases = {
        "Aplicação": {"color": "#2ECC71", "index": 0},
        "Consenso": {"color": "#3498DB", "index": 1},
        "Infraestrutura": {"color": "#9B59B6", "index": 2},
        "Internet": {"color": "#E74C3C", "index": 3}
    }
    
    # Get current phase
    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    
    # Create the layer visualization
    st.markdown('<div class="layer-container">', unsafe_allow_html=True)
    
    for phase_name, info in phases.items():
        # Get questions for this phase
        phase_questions = [q for q in questions if q["phase"] == phase_name]
        answered = len([q for q in phase_questions if q["id"] in st.session_state.answers])
        total = len(phase_questions)
        
        # Determine if this is the current phase
        is_current = current_phase == phase_name
        opacity = "1" if is_current else "0.7"
        
        # Create the diamond shape for each layer
        st.markdown(f'''
            <div class="layer">
                <div class="diamond" style="background-color: {info['color']}; opacity: {opacity}">
                    <div class="layer-text">{phase_name}</div>
                </div>
                <div class="layer-progress">({answered}/{total})</div>
            </div>
            {('<div class="connection-line"></div>' if info['index'] < len(phases)-1 else '')}
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

def show_algorithm_groups_matrix(consensus_group):
    if consensus_group in consensus_groups:
        group_data = consensus_groups[consensus_group]['characteristics']
        group_df = pd.DataFrame([group_data])
        
        fig = go.Figure(data=go.Heatmap(
            z=group_df.values,
            x=group_df.columns,
            y=[consensus_group],
            colorscale='Viridis',
            hovertemplate="Grupo: %{y}<br>Métrica: %{x}<br>Score: %{z:.2f}<extra></extra>"
        ))
        fig.update_layout(title=f"Características do Grupo {consensus_group}")
        st.plotly_chart(fig, use_container_width=True)

def show_consensus_algorithms_matrix(consensus_group, selected_consensus):
    if consensus_group in consensus_groups:
        algorithms = consensus_groups[consensus_group]['algorithms']
        algo_data = {
            algo: consensus_algorithms.get(algo, {})
            for algo in algorithms
        }
        
        algo_df = pd.DataFrame.from_dict(algo_data, orient='index')
        
        fig = go.Figure(data=go.Heatmap(
            z=algo_df.values,
            x=algo_df.columns,
            y=algo_df.index,
            colorscale='Viridis',
            hovertemplate="Algoritmo: %{y}<br>Métrica: %{x}<br>Score: %{z:.2f}<extra></extra>"
        ))
        fig.update_layout(title=f"Comparação de Algoritmos de Consenso")
        st.plotly_chart(fig, use_container_width=True)

def get_current_phase(questions, answers):
    try:
        return next((q["phase"] for q in questions if q["id"] not in answers), "Completo")
    except (KeyError, StopIteration):
        return "Completo"

def run_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")
    
    # Show phase progress right after the title
    show_phase_progress()
    
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
            
            st.markdown("---")
            st.header("Análise Detalhada da Recomendação")
            
            # 1. DLT Matrix
            with st.expander("Matriz de Avaliação de DLTs", expanded=True):
                st.markdown("### Comparação de DLTs")
                # Show DLT heatmap
                if 'evaluation_matrix' in rec:
                    show_dlt_matrix(rec['evaluation_matrix'])
                    
                st.markdown('''
                ### Como interpretar:
                - Cores mais escuras indicam melhor performance
                - Compare as DLTs em diferentes características
                - Considere o balanço entre características prioritárias
                ''')
            
            # 2. Algorithm Groups Matrix
            with st.expander("Matriz de Grupos de Algoritmos", expanded=True):
                st.markdown("### Comparação de Grupos de Algoritmos")
                show_algorithm_groups_matrix(rec['consensus_group'])
                st.markdown(f'''
                ### Grupo Recomendado: {rec['consensus_group']}
                - **Razão da Escolha**: {rec.get('group_description', '')}
                - **Características Principais**: {', '.join(consensus_groups[rec['consensus_group']]['characteristics'].keys())}
                ''')
            
            # 3. Consensus Algorithms Matrix
            with st.expander("Matriz de Algoritmos de Consenso", expanded=True):
                st.markdown("### Comparação de Algoritmos")
                show_consensus_algorithms_matrix(rec['consensus_group'], rec['consensus'])
                
                # Show weight calculations
                st.markdown("### Ponderação das Características")
                weight_cols = st.columns(4)
                for idx, (char, weight) in enumerate(weights.items()):
                    with weight_cols[idx]:
                        st.metric(
                            f"{char.title()}",
                            f"{float(weight)*100:.1f}%",
                            help=f"Peso atribuído para {char}"
                        )
            
            # 4. Implementation Scenarios
            with st.expander("Cenários de Implementação", expanded=True):
                st.markdown("### Cenários Possíveis")
                
                scenarios = {
                    "EMR": "Prontuário Eletrônico",
                    "Supply Chain": "Cadeia de Suprimentos",
                    "Consent": "Gestão de Consentimento",
                    "IoT": "Dispositivos Médicos"
                }
                
                for scenario, desc in scenarios.items():
                    st.markdown(f"#### {desc}")
                    st.markdown(f"- **DLT Sugerida**: {rec['dlt']}")
                    st.markdown(f"- **Algoritmo**: {rec['consensus']}")
                    st.markdown(f"- **Razão**: Baseado nas características priorizadas para {desc}")
            
            # Create columns for the final recommendation display and save button
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