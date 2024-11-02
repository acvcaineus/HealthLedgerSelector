import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from decision_logic import get_recommendation
from database import save_recommendation
from dlt_data import questions, dlt_metrics

def create_progress_animation(current_phase, answers):
    """Create an animated progress visualization."""
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    fig = go.Figure()
    
    phase_progress = {phase: 0 for phase in phases}
    phase_total = {phase: 0 for phase in phases}
    phase_characteristics = {phase: set() for phase in phases}
    
    for q in questions:
        phase = q['phase']
        phase_total[phase] += 1
        phase_characteristics[phase].add(q['characteristic'])
        if q['id'] in answers:
            phase_progress[phase] += 1
    
    for i, phase in enumerate(phases):
        if phase == current_phase:
            color = '#3498db'
            size = 45
        elif phase_progress[phase] > 0:
            color = '#2ecc71'
            size = 40
        else:
            color = '#bdc3c7'
            size = 35
            
        tooltip = f"<b>{phase}</b><br>"
        tooltip += f"Progresso: {phase_progress[phase]}/{phase_total[phase]}<br>"
        tooltip += "<br>Características:<br>"
        tooltip += "<br>".join([f"- {char}" for char in phase_characteristics[phase]])
        
        fig.add_trace(go.Scatter(
            x=[i], y=[0],
            mode='markers',
            marker=dict(
                size=size,
                color=color,
                line=dict(color='white', width=2),
                symbol='circle'
            ),
            hovertext=tooltip,
            hoverinfo='text',
            showlegend=False
        ))
        
        fig.add_annotation(
            x=i, y=-0.2,
            text=f"{phase}<br>({phase_progress[phase]}/{phase_total[phase]})",
            showarrow=False,
            font=dict(size=12)
        )
        
        if i < len(phases) - 1:
            fig.add_trace(go.Scatter(
                x=[i, i+1],
                y=[0, 0],
                mode='lines',
                line=dict(
                    color='gray',
                    width=2,
                    dash='dot'
                ),
                showlegend=False
            ))
    
    fig.update_layout(
        showlegend=False,
        height=200,
        margin=dict(l=20, r=20, t=20, b=40),
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.5, len(phases)-0.5]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.5, 0.5]
        )
    )
    
    return fig

def create_evaluation_matrices(recommendation):
    """Create and display evaluation matrices."""
    if not recommendation or 'evaluation_matrix' not in recommendation:
        return
        
    st.subheader("Matriz de Avaliação Detalhada")
    
    # Add CSS for highlighting
    st.markdown('''
    <style>
        .recommended {
            background-color: #e6f3ff;
            font-weight: bold;
        }
        .metric-high {
            color: #2ecc71;
            font-weight: bold;
        }
        .metric-low {
            color: #e74c3c;
        }
    </style>
    ''', unsafe_allow_html=True)
    
    # DLT Matrix Section
    with st.expander("ℹ️ Entenda a Matriz de DLTs"):
        st.markdown("""
        ### Matriz de Avaliação de DLTs
        
        Esta matriz mostra a comparação detalhada entre diferentes DLTs baseada em quatro métricas principais:
        
        - **Segurança**: Capacidade de proteger dados e transações
        - **Escalabilidade**: Capacidade de crescer mantendo o desempenho
        - **Eficiência Energética**: Consumo de energia por transação
        - **Governança**: Flexibilidade e controle do sistema
        
        Os valores são normalizados de 0 a 1, onde 1 representa o melhor desempenho.
        """)
    
    # Group DLTs by type
    dlt_by_type = {}
    for dlt, info in recommendation['evaluation_matrix'].items():
        dlt_type = info['type']
        if dlt_type not in dlt_by_type:
            dlt_by_type[dlt_type] = []
        dlt_by_type[dlt_type].append(dlt)
    
    # Create DLT comparison heatmap for weighted scores
    st.subheader("Comparação de Métricas por Tipo de DLT")
    metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
    metrics_pt = ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança']
    
    # Prepare data for weighted metrics heatmap
    weighted_values = []
    dlt_types = []
    dlt_names = []
    
    for dlt_type in sorted(dlt_by_type.keys()):
        for dlt in dlt_by_type[dlt_type]:
            row = []
            for metric in metrics:
                weighted_score = recommendation['evaluation_matrix'][dlt]['weighted_metrics'][metric]
                row.append(weighted_score)
            weighted_values.append(row)
            dlt_types.append(dlt_type)
            dlt_names.append(dlt)
    
    # Create weighted metrics heatmap
    fig_weighted = go.Figure(data=go.Heatmap(
        z=weighted_values,
        y=dlt_names,
        x=metrics_pt,
        colorscale='RdBu',
        hoverongaps=False,
        hovertemplate="<b>DLT:</b> %{y}<br>" +
                     "<b>Tipo:</b> %{customdata}<br>" +
                     "<b>Métrica:</b> %{x}<br>" +
                     "<b>Score Ponderado:</b> %{z:.2f}<br>" +
                     "<extra></extra>",
        customdata=dlt_types
    ))
    
    fig_weighted.update_layout(
        title="Scores Ponderados por Tipo de DLT",
        yaxis_title="DLTs",
        xaxis_title="Métricas",
        height=600
    )
    
    st.plotly_chart(fig_weighted, use_container_width=True)
    st.caption("As DLTs estão agrupadas por tipo para melhor comparação. Cores mais escuras indicam scores mais altos.")
    
    # Create score comparison table with styling
    scores_df = pd.DataFrame({
        'Tipo de DLT': [recommendation['evaluation_matrix'][dlt]['type'] for dlt in dlt_names],
        'DLT': dlt_names,
        'Score Total': [recommendation['weighted_scores'][dlt] for dlt in dlt_names],
        'Segurança': [recommendation['evaluation_matrix'][dlt]['raw_metrics']['security'] for dlt in dlt_names],
        'Escalabilidade': [recommendation['evaluation_matrix'][dlt]['raw_metrics']['scalability'] for dlt in dlt_names],
        'Eficiência': [recommendation['evaluation_matrix'][dlt]['raw_metrics']['energy_efficiency'] for dlt in dlt_names],
        'Governança': [recommendation['evaluation_matrix'][dlt]['raw_metrics']['governance'] for dlt in dlt_names]
    }).sort_values('Score Total', ascending=False)
    
    # Style the DataFrame
    def highlight_recommended(row):
        if row.name == recommendation['dlt']:
            return ['background-color: #e6f3ff'] * len(row)
        return [''] * len(row)
    
    def highlight_metrics(val):
        if isinstance(val, float):
            if val >= 0.8:
                return 'color: #2ecc71; font-weight: bold'
            elif val <= 0.4:
                return 'color: #e74c3c'
        return ''
    
    scores_styled = scores_df.style\
        .apply(highlight_recommended, axis=1)\
        .applymap(highlight_metrics, subset=['Segurança', 'Escalabilidade', 'Eficiência', 'Governança'])
    
    st.subheader("Tabela Comparativa de DLTs")
    st.table(scores_styled)
    st.caption("💡 A linha destacada em azul indica a DLT recomendada. Métricas em verde são pontos fortes (≥0.8) e em vermelho são pontos de atenção (≤0.4).")

def select_consensus_algorithm(dlt_type, answers):
    """Select the best consensus algorithm based on DLT type and characteristics."""
    # Define algorithm groups and their algorithms
    algorithm_groups = {
        "Alta Segurança e Controle": {
            "algorithms": ["PBFT", "PoW"],
            "dlt_types": ["DLT Permissionada Privada", "DLT Pública"]
        },
        "Alta Eficiência": {
            "algorithms": ["PoA", "RAFT"],
            "dlt_types": ["DLT Permissionada Simples"]
        },
        "Escalabilidade e Governança": {
            "algorithms": ["PoS", "DPoS"],
            "dlt_types": ["DLT Híbrida", "DLT Pública Permissionless"]
        },
        "Alta Escalabilidade IoT": {
            "algorithms": ["Tangle", "DAG"],
            "dlt_types": ["DLT com Consenso Delegado"]
        }
    }
    
    # Find matching group for DLT type
    matching_group = None
    for group, info in algorithm_groups.items():
        if dlt_type in info["dlt_types"]:
            matching_group = group
            break
    
    if not matching_group:
        return "Não disponível"
    
    # Score algorithms within the matching group
    algorithm_scores = {}
    for algorithm in algorithm_groups[matching_group]["algorithms"]:
        score = 0
        if "security" in answers and answers["security"] == "Sim":
            score += 0.4  # Security weight
        if "scalability" in answers and answers["scalability"] == "Sim":
            score += 0.3  # Scalability weight
        if "energy_efficiency" in answers and answers["energy_efficiency"] == "Sim":
            score += 0.2  # Energy efficiency weight
        if "governance_flexibility" in answers and answers["governance_flexibility"] == "Sim":
            score += 0.1  # Governance weight
        algorithm_scores[algorithm] = score
    
    # Return the highest scoring algorithm
    return max(algorithm_scores.items(), key=lambda x: x[1])[0] if algorithm_scores else "Não disponível"

def run_decision_tree():
    """Main function to run the decision tree interface."""
    st.title("Framework de Seleção de DLT")
    
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    # Add reset button
    if st.button("🔄 Reiniciar", help="Clique para recomeçar o processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()
    
    # Get current phase
    current_phase = None
    for q in questions:
        if q['id'] not in st.session_state.answers:
            current_phase = q['phase']
            break
    
    # Display progress animation
    if current_phase:
        progress_fig = create_progress_animation(current_phase, st.session_state.answers)
        st.plotly_chart(progress_fig, use_container_width=True)
    
    # Display current question
    current_question = None
    for q in questions:
        if q['id'] not in st.session_state.answers:
            current_question = q
            break
    
    if current_question:
        st.subheader(f"Fase: {current_question['phase']}")
        st.info(f"Característica: {current_question['characteristic']}")
        
        response = st.radio(
            current_question['text'],
            current_question['options']
        )
        
        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question['id']] = response
            st.experimental_rerun()
    
    # Show recommendation when all questions are answered
    if len(st.session_state.answers) == len(questions):
        recommendation = get_recommendation(st.session_state.answers)
        
        st.header("Recomendação")
        st.write(f"DLT Recomendada: {recommendation['dlt']}")
        st.write(f"Tipo de DLT: {recommendation['dlt_type']}")
        st.write(f"Algoritmo de Consenso: {recommendation['consensus']}")
        
        # Display evaluation matrices
        create_evaluation_matrices(recommendation)
        
        # Add save button for authenticated users
        if st.session_state.get('authenticated', False):
            if st.button("💾 Salvar Recomendação"):
                save_recommendation(
                    st.session_state.username,
                    "Healthcare",
                    recommendation
                )
                st.success("Recomendação salva com sucesso!")
