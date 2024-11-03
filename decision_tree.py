import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
    
    # Create nodes for each phase with improved styling
    for i, phase in enumerate(phases):
        # Determine node styling with better visual hierarchy
        if phase == current_phase:
            color = '#3498db'  # Active phase (blue)
            size = 45
            symbol = 'circle'
        elif phase_progress[phase] > 0:
            color = '#2ecc71'  # Completed phase (green)
            size = 40
            symbol = 'circle-dot'
        else:
            color = '#bdc3c7'  # Pending phase (gray)
            size = 35
            symbol = 'circle-open'
        
        # Enhanced tooltip with more detailed information
        tooltip = f"""
        <b>{phase}</b><br>
        Progresso: {phase_progress[phase]}/{phase_total[phase]}<br>
        <br>Características:<br>
        {('<br>'.join(f'• {char}' for char in phase_characteristics[phase]))}
        """
        
        # Add node with enhanced styling
        fig.add_trace(go.Scatter(
            x=[i], y=[0],
            mode='markers',
            marker=dict(
                size=size,
                color=color,
                line=dict(color='white', width=2),
                symbol=symbol
            ),
            hovertext=tooltip,
            hoverinfo='text',
            showlegend=False
        ))
        
        # Add phase label with progress information
        fig.add_annotation(
            x=i, y=-0.2,
            text=f"{phase}<br>({phase_progress[phase]}/{phase_total[phase]})",
            showarrow=False,
            font=dict(size=12, color='rgba(0,0,0,0.7)')
        )
        
        # Add connecting lines between phases with improved styling
        if i < len(phases) - 1:
            fig.add_trace(go.Scatter(
                x=[i, i+1],
                y=[0, 0],
                mode='lines',
                line=dict(
                    color='rgba(52, 152, 219, 0.3)',
                    width=2,
                    dash='dot'
                ),
                showlegend=False
            ))
    
    # Update layout with improved aesthetics
    fig.update_layout(
        showlegend=False,
        height=200,
        margin=dict(l=20, r=20, t=20, b=40),
        plot_bgcolor='white',
        paper_bgcolor='white',
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

def create_classification_path_visualization(recommendation):
    """Create a visualization showing the complete DLT classification path."""
    if not recommendation or recommendation['dlt'] == "Não disponível":
        return None
    
    # Create Sankey diagram data
    nodes = [
        # Level 1: DLT Type
        dict(label="DLT Types"),
        dict(label=recommendation['dlt_type']),
        # Level 2: Data Structure
        dict(label="Data Structures"),
        dict(label=recommendation['data_structure']),
        # Level 3: Algorithm Group
        dict(label="Algorithm Groups"),
        dict(label=recommendation['group']),
        # Level 4: Specific Algorithms
        dict(label="Algorithms")
    ]
    
    # Add nodes for specific algorithms
    algo_start_idx = len(nodes)
    for algo in recommendation['algorithms']:
        nodes.append(dict(label=algo))
    
    # Create links between nodes
    links = [
        dict(source=0, target=1, value=1),  # Types to selected type
        dict(source=1, target=2, value=1),  # Type to Structures
        dict(source=2, target=3, value=1),  # Structures to selected structure
        dict(source=3, target=4, value=1),  # Structure to Groups
        dict(source=4, target=5, value=1),  # Groups to selected group
        dict(source=5, target=6, value=1),  # Group to Algorithms
    ]
    
    # Add links to specific algorithms
    for i, _ in enumerate(recommendation['algorithms']):
        links.append(dict(source=6, target=algo_start_idx + i, value=1))
    
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[node['label'] for node in nodes],
            color=['#3498db' if i < algo_start_idx else '#2ecc71' 
                   for i in range(len(nodes))]
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links]
        )
    )])
    
    fig.update_layout(
        title_text="Caminho de Classificação Completo",
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
    
    # Show complete classification path
    st.subheader("🔄 Caminho de Classificação")
    path_fig = create_classification_path_visualization(recommendation)
    if path_fig:
        st.plotly_chart(path_fig, use_container_width=True)
    
    # Display DLT details in organized sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Classificação")
        st.write(f"**DLT:** {recommendation['dlt']}")
        st.write(f"**Tipo:** {recommendation['dlt_type']}")
        st.write(f"**Estrutura de Dados:** {recommendation['data_structure']}")
        st.write(f"**Grupo:** {recommendation['group']}")
    
    with col2:
        st.subheader("🔧 Algoritmos")
        for algo in recommendation['algorithms']:
            st.write(f"• {algo}")
    
    # Technical details in expandable sections
    with st.expander("📋 Características Técnicas"):
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

    # Add the new evaluation matrices
    st.subheader("Matriz de Avaliação de DLTs")
    dlt_metrics_df = pd.DataFrame({
        'DLT': ['Hyperledger Fabric', 'Quorum', 'VeChain', 'IOTA', 'Ethereum 2.0'],
        'Segurança': [0.85, 0.78, 0.75, 0.80, 0.85],
        'Escalabilidade': [0.65, 0.70, 0.80, 0.85, 0.75],
        'Eficiência': [0.80, 0.80, 0.85, 0.90, 0.65],
        'Governança': [0.75, 0.78, 0.70, 0.60, 0.80]
    }).set_index('DLT')

    # Create heatmap for DLTs
    fig_dlt = px.imshow(
        dlt_metrics_df,
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    st.plotly_chart(fig_dlt)

    # Algorithm Groups Matrix
    st.subheader("Matriz de Grupos de Algoritmos")
    algo_groups_df = pd.DataFrame({
        'Grupo': ['Alta Segurança', 'Alta Eficiência', 'Escalabilidade', 'IoT'],
        'Segurança': [0.90, 0.75, 0.80, 0.70],
        'Escalabilidade': [0.60, 0.85, 0.90, 0.95],
        'Eficiência': [0.70, 0.90, 0.85, 0.80],
        'Governança': [0.85, 0.70, 0.75, 0.65]
    }).set_index('Grupo')

    # Create heatmap for algorithm groups
    fig_groups = px.imshow(
        algo_groups_df,
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    st.plotly_chart(fig_groups)

    # Consensus Algorithms Matrix
    st.subheader("Matriz de Algoritmos de Consenso")
    algo_df = pd.DataFrame({
        'Algoritmo': ['PBFT', 'PoW', 'PoS', 'PoA', 'Tangle'],
        'Segurança': [0.90, 0.95, 0.85, 0.80, 0.75],
        'Escalabilidade': [0.70, 0.40, 0.85, 0.80, 0.95],
        'Eficiência': [0.80, 0.30, 0.85, 0.90, 0.95],
        'Governança': [0.85, 0.50, 0.80, 0.75, 0.70]
    }).set_index('Algoritmo')

    # Create heatmap for consensus algorithms
    fig_algo = px.imshow(
        algo_df,
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    st.plotly_chart(fig_algo)

    # Add explanatory text
    st.info('''
    ### Como interpretar as matrizes:
    1. **Matriz de DLTs**: Mostra o desempenho geral de cada DLT nas principais métricas
    2. **Matriz de Grupos**: Apresenta as características de cada grupo de algoritmos
    3. **Matriz de Algoritmos**: Detalha o desempenho específico de cada algoritmo de consenso

    As cores mais escuras indicam valores mais altos (melhor desempenho).
    ''')

    # Use cases and examples
    with st.expander("🎯 Casos de Uso"):
        st.write(recommendation['details']['use_cases'])
        st.subheader("Casos Reais")
        st.write(recommendation['details']['real_cases'])
    
    # Challenges and limitations
    with st.expander("⚠️ Desafios e Limitações"):
        st.write(recommendation['details']['challenges'])
    
    # Complete reference information
    with st.expander("📚 Referências"):
        st.write(recommendation['details']['references'])
    
    # Comparison table
    st.subheader("📊 Comparação de DLTs")
    comparison_data = []
    for dlt_name, matrix_info in recommendation['evaluation_matrix'].items():
        comparison_data.append({
            'DLT': dlt_name,
            'Tipo': matrix_info['type'],
            'Estrutura': matrix_info['data_structure'],
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
