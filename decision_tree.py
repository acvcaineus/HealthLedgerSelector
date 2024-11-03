import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from decision_logic import get_recommendation
from database import save_recommendation
from dlt_data import questions, dlt_metrics

def get_consensus_group_algorithms(consensus_group):
    """Return algorithms for a given consensus group."""
    group_algorithms = {
        "Alta Segurança e Controle": ["PBFT", "PoW"],
        "Alta Eficiência": ["PoA", "RAFT"],
        "Escalabilidade e Governança": ["PoS", "DPoS"],
        "Alta Escalabilidade IoT": ["Tangle", "DAG"]
    }
    return group_algorithms.get(consensus_group, [])

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
    
    # Add tooltips explaining the scoring
    st.info("""
    💡 **Como interpretar os scores:**
    - ✅ Valores ≥ 0.8: Pontos fortes
    - ❌ Valores < 0.8: Áreas que precisam de atenção
    - A pontuação total considera todas as características com pesos iguais (25% cada)
    """)
    
    # DLT Types Matrix
    st.subheader("Matriz de Tipos de DLT")
    dlt_types_df = pd.DataFrame({
        'Tipo': ['DLT Permissionada Privada', 'DLT Permissionada Simples', 'DLT Híbrida', 
                 'DLT com Consenso Delegado', 'DLT Pública', 'DLT Pública Permissionless'],
        'Segurança': [0.85, 0.70, 0.78, 0.80, 0.95, 0.85],
        'Escalabilidade': [0.65, 0.55, 0.75, 0.85, 0.40, 0.75],
        'Eficiência': [0.80, 0.75, 0.80, 0.90, 0.35, 0.65],
        'Governança': [0.75, 0.80, 0.78, 0.60, 0.50, 0.80]
    }).set_index('Tipo')

    # Create heatmap for DLT types
    fig_types = px.imshow(
        dlt_types_df,
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    fig_types.update_layout(
        title="Comparação de Tipos de DLT",
        height=400
    )
    st.plotly_chart(fig_types)
    
    # Consensus Groups Matrix
    st.subheader("Matriz de Grupos de Consenso")
    consensus_groups_df = pd.DataFrame({
        'Grupo': ['Alta Segurança e Controle', 'Alta Eficiência', 'Escalabilidade e Governança', 'Alta Escalabilidade IoT'],
        'Segurança': [0.90, 0.75, 0.80, 0.70],
        'Escalabilidade': [0.60, 0.85, 0.90, 0.95],
        'Eficiência': [0.70, 0.90, 0.85, 0.80],
        'Governança': [0.85, 0.80, 0.95, 0.75]
    }).set_index('Grupo')
    
    fig_consensus = px.imshow(
        consensus_groups_df,
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    fig_consensus.update_layout(
        title="Comparação de Grupos de Consenso",
        height=400
    )
    st.plotly_chart(fig_consensus)
    
    # Algorithms Matrix
    st.subheader("Matriz de Algoritmos do Grupo")
    consensus_group = recommendation.get('consensus_group', 'Alta Segurança e Controle')
    algorithms = get_consensus_group_algorithms(consensus_group)
    
    if algorithms:
        algorithms_df = pd.DataFrame({
            'Algoritmo': algorithms,
            'Segurança': [0.85 if 'PBFT' in alg else 0.75 for alg in algorithms],
            'Escalabilidade': [0.70 if 'PBFT' in alg else 0.85 for alg in algorithms],
            'Eficiência': [0.80 if 'PoS' in alg else 0.70 for alg in algorithms],
            'Governança': [0.90 if 'DPoS' in alg else 0.75 for alg in algorithms]
        }).set_index('Algoritmo')
        
        fig_algorithms = px.imshow(
            algorithms_df,
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        fig_algorithms.update_layout(
            title=f"Comparação de Algoritmos do Grupo: {consensus_group}",
            height=400
        )
        st.plotly_chart(fig_algorithms)
    
    # Create score comparison table with styling
    scores_df = pd.DataFrame({
        'Tipo de DLT': [recommendation['evaluation_matrix'][dlt]['type'] for dlt in recommendation['evaluation_matrix']],
        'DLT': list(recommendation['evaluation_matrix'].keys()),
        'Score Total': [recommendation['weighted_scores'][dlt] for dlt in recommendation['evaluation_matrix']],
        'Segurança': [recommendation['evaluation_matrix'][dlt]['metrics']['security'] for dlt in recommendation['evaluation_matrix']],
        'Escalabilidade': [recommendation['evaluation_matrix'][dlt]['metrics']['scalability'] for dlt in recommendation['evaluation_matrix']],
        'Eficiência': [recommendation['evaluation_matrix'][dlt]['metrics']['energy_efficiency'] for dlt in recommendation['evaluation_matrix']],
        'Governança': [recommendation['evaluation_matrix'][dlt]['metrics']['governance'] for dlt in recommendation['evaluation_matrix']]
    }).sort_values('Score Total', ascending=False)
    
    def highlight_recommended(row):
        return ['background-color: #e6f3ff' if row.name == recommendation['dlt'] else '' for _ in row]
    
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

    # Add explanation section for recommendation
    st.header("Explicação da Recomendação")

    # Add explanation for the chosen DLT
    st.subheader(f"Por que {recommendation['dlt']} foi escolhida:")
    st.write(f"""
    - **Tipo de DLT:** {recommendation['dlt_type']}
    - **Pontuação Total:** {recommendation['weighted_scores'][recommendation['dlt']]:.2f}
    - **Pontos Fortes:**
      - Segurança: {recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['security']:.2f}
      - Escalabilidade: {recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['scalability']:.2f}
      - Eficiência Energética: {recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['energy_efficiency']:.2f}
      - Governança: {recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['governance']:.2f}
    """)

    # Add explanations for why other DLTs were not chosen
    st.subheader("Por que outras DLTs não foram selecionadas:")
    for dlt, score in sorted(recommendation['weighted_scores'].items(), key=lambda x: x[1], reverse=True)[1:]:
        with st.expander(f"{dlt} (Score: {score:.2f})"):
            metrics = recommendation['evaluation_matrix'][dlt]['metrics']
            st.write(f"""
            **Razões:**
            - Segurança: {metrics['security']:.2f} {'✅' if metrics['security'] >= 0.8 else '❌'}
            - Escalabilidade: {metrics['scalability']:.2f} {'✅' if metrics['scalability'] >= 0.8 else '❌'}
            - Eficiência Energética: {metrics['energy_efficiency']:.2f} {'✅' if metrics['energy_efficiency'] >= 0.8 else '❌'}
            - Governança: {metrics['governance']:.2f} {'✅' if metrics['governance'] >= 0.8 else '❌'}
            
            **Diferença para a DLT escolhida:** {(recommendation['weighted_scores'][recommendation['dlt']] - score):.2f} pontos
            """)

def select_consensus_algorithm(dlt_type, answers):
    """Select the best consensus algorithm based on DLT type and characteristics."""
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
        if answers.get('network_security') == 'Sim':
            score += 0.4  # Security weight
        if answers.get('scalability') == 'Sim':
            score += 0.3  # Scalability weight
        if answers.get('energy_efficiency') == 'Sim':
            score += 0.2  # Energy efficiency weight
        if answers.get('governance_flexibility') == 'Sim':
            score += 0.1  # Governance weight
        algorithm_scores[algorithm] = score
    
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
