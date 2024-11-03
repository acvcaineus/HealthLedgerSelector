import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dlt_data import questions
from decision_logic import get_recommendation, dlt_classification

def create_progress_animation(current_phase, answers, questions):
    """Create an animated progress visualization with enhanced interactivity."""
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    fig = go.Figure()
    
    # Calculate progress for each phase
    phase_progress = {phase: 0 for phase in phases}
    phase_total = {phase: 0 for phase in phases}
    phase_characteristics = {phase: set() for phase in phases}
    
    for q in questions:
        phase = q['phase']
        phase_total[phase] += 1
        phase_characteristics[phase].add(q['characteristic'])
        if q['id'] in answers:
            phase_progress[phase] += 1
    
    # Create nodes for each phase
    for i, phase in enumerate(phases):
        # Determine node styling
        if phase == current_phase:
            color = '#3498db'  # Active phase (blue)
            size = 45
        elif phase_progress[phase] > 0:
            color = '#2ecc71'  # Completed phase (green)
            size = 40
        else:
            color = '#bdc3c7'  # Pending phase (gray)
            size = 35
        
        # Create tooltip with detailed information
        tooltip = f"<b>{phase}</b><br>"
        tooltip += f"Progresso: {phase_progress[phase]}/{phase_total[phase]}<br>"
        tooltip += "<br>Características:<br>"
        tooltip += "<br>".join([f"- {char}" for char in phase_characteristics[phase]])
        
        # Add node
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
        
        # Add phase label
        fig.add_annotation(
            x=i, y=-0.2,
            text=f"{phase}<br>({phase_progress[phase]}/{phase_total[phase]})",
            showarrow=False,
            font=dict(size=12)
        )
        
        # Add connecting lines between phases
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
    
    # Update layout
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

def create_hierarchical_visualization(recommendation):
    """Create a visualization showing the DLT selection path."""
    if not recommendation or recommendation['dlt'] == "Não disponível":
        return None
    
    selected_dlt = recommendation['dlt']
    dlt_info = dlt_classification[selected_dlt]
    
    # Create Sankey diagram data
    nodes = []
    links = []
    
    # Add nodes for each level
    nodes.extend([
        # DLT Types
        dict(label="DLT Types"),
        dict(label=dlt_info['type']),
        # Algorithm Groups
        dict(label="Algorithm Groups"),
        dict(label=dlt_info['group']),
        # Algorithms
        dict(label="Algorithms"),
    ])
    
    # Add nodes for each algorithm
    for algo in dlt_info['algorithms']:
        nodes.append(dict(label=algo))
    
    # Create links
    links.extend([
        # Link from Types to selected type
        dict(source=0, target=1, value=1),
        # Link from selected type to Groups
        dict(source=1, target=2, value=1),
        # Link from Groups to selected group
        dict(source=2, target=3, value=1),
        # Link from selected group to Algorithms
        dict(source=3, target=4, value=1),
    ])
    
    # Add links to algorithms
    for i, _ in enumerate(dlt_info['algorithms']):
        links.append(dict(source=4, target=5+i, value=1))
    
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[node['label'] for node in nodes],
            color=['#3498db' if i < 5 else '#2ecc71' for i in range(len(nodes))]
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links]
        )
    )])
    
    fig.update_layout(
        title_text="DLT Selection Path",
        font_size=12,
        height=400
    )
    
    return fig

def create_evaluation_matrices(recommendation):
    """Create and display evaluation matrices with hierarchical relationships."""
    if not recommendation or recommendation['dlt'] == "Não disponível":
        st.warning("Recomendação indisponível.")
        return
    
    st.header("Recomendação de DLT e Análise")
    
    # Show hierarchical visualization
    st.subheader("🔄 Caminho de Seleção")
    hierarchy_fig = create_hierarchical_visualization(recommendation)
    if hierarchy_fig:
        st.plotly_chart(hierarchy_fig, use_container_width=True)
    
    # Display DLT details
    st.subheader("📊 Detalhes da DLT Recomendada")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**DLT:** {recommendation['dlt']}")
        st.write(f"**Tipo:** {recommendation['dlt_type']}")
        st.write(f"**Grupo:** {recommendation['group']}")
    
    with col2:
        st.write("**Algoritmos Disponíveis:**")
        for algo in recommendation['algorithms']:
            st.write(f"- {algo}")
    
    # Technical details in expandable sections
    with st.expander("📋 Características Técnicas"):
        st.write(recommendation['details']['technical_characteristics'])
        
        # Create metrics visualization
        metrics_df = pd.DataFrame({
            'Métrica': list(recommendation['metrics'].keys()),
            'Valor': list(recommendation['metrics'].values())
        })
        
        fig = go.Figure(data=[
            go.Bar(
                x=metrics_df['Métrica'],
                y=metrics_df['Valor'],
                marker_color='#3498db'
            )
        ])
        
        fig.update_layout(
            title="Métricas Técnicas",
            xaxis_title="Métricas",
            yaxis_title="Pontuação",
            yaxis_range=[0, 1]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("🎯 Casos de Uso"):
        st.write(recommendation['details']['use_cases'])
    
    with st.expander("⚠️ Desafios e Limitações"):
        st.write(recommendation['details']['challenges'])
    
    with st.expander("📚 Referências"):
        st.write(recommendation['details']['references'])
    
    # Create comparison table
    st.subheader("📊 Comparação de DLTs")
    comparison_data = []
    for dlt_name, matrix_info in recommendation['evaluation_matrix'].items():
        comparison_data.append({
            'DLT': dlt_name,
            'Tipo': matrix_info['type'],
            'Grupo': matrix_info['group'],
            'Score': matrix_info['score'],
            **matrix_info['metrics']
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.sort_values('Score', ascending=False)
    
    # Style the dataframe
    def highlight_max(s):
        is_max = s == s.max()
        return ['background-color: #e6f3ff' if v else '' for v in is_max]
    
    styled_df = comparison_df.style\
        .apply(highlight_max)\
        .format({
            'Score': '{:.2f}',
            'security': '{:.2f}',
            'scalability': '{:.2f}',
            'energy_efficiency': '{:.2f}',
            'governance': '{:.2f}'
        })
    
    st.table(styled_df)

def run_decision_tree():
    """Main function to run the decision tree interface."""
    st.title("Framework de Seleção de DLT")
    
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    if st.button("🔄 Reiniciar", help="Clique para recomeçar o processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()
    
    current_phase = None
    for q in questions:
        if q['id'] not in st.session_state.answers:
            current_phase = q['phase']
            break
    
    if current_phase:
        progress_fig = create_progress_animation(current_phase, st.session_state.answers, questions)
        st.plotly_chart(progress_fig, use_container_width=True)
    
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
    
    if len(st.session_state.answers) == len(questions):
        recommendation = get_recommendation(st.session_state.answers)
        create_evaluation_matrices(recommendation)
