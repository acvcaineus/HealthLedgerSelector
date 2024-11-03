import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dlt_data import questions
from decision_logic import get_recommendation
from database import save_recommendation

def create_progress_animation(current_phase, answers, questions):
    """Create an animated progress visualization with enhanced interactivity."""
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    fig = go.Figure()
    
    phase_progress = {phase: 0 for phase in phases}
    phase_total = {phase: 0 for phase in phases}
    phase_characteristics = {phase: set() for phase in phases}
    phase_importance = {
        'Aplicação': 0.4,  # Security and privacy focused
        'Consenso': 0.25,  # Scalability focused
        'Infraestrutura': 0.20,  # Energy efficiency focused
        'Internet': 0.15   # Governance focused
    }
    
    for q in questions:
        phase = q['phase']
        phase_total[phase] += 1
        phase_characteristics[phase].add(q['characteristic'])
        if q['id'] in answers:
            phase_progress[phase] += 1
    
    # Create nodes for each phase with improved styling
    for i, phase in enumerate(phases):
        # Calculate phase completion percentage
        completion = phase_progress[phase] / phase_total[phase] if phase_total[phase] > 0 else 0
        
        if phase == current_phase:
            color = '#3498db'  # Active phase (blue)
            size = 45
            symbol = 'circle'
        elif completion == 1:
            color = '#2ecc71'  # Completed phase (green)
            size = 40
            symbol = 'circle-dot'
        elif completion > 0:
            color = '#f1c40f'  # Partially completed (yellow)
            size = 38
            symbol = 'circle-open'
        else:
            color = '#bdc3c7'  # Pending phase (gray)
            size = 35
            symbol = 'circle-open'
        
        # Enhanced tooltip with more information
        tooltip = f"""
        <b>{phase}</b><br>
        Progresso: {phase_progress[phase]}/{phase_total[phase]} ({completion:.0%})<br>
        Importância: {phase_importance[phase]:.0%}<br>
        <br>Características:<br>
        {('<br>'.join(f'• {char}' for char in phase_characteristics[phase]))}
        """
        
        # Add phase node
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
        
        # Add phase label with completion percentage
        fig.add_annotation(
            x=i, y=-0.2,
            text=f"{phase}<br>({completion:.0%})",
            showarrow=False,
            font=dict(size=12, color='rgba(0,0,0,0.7)')
        )
        
        # Add connecting lines between phases
        if i < len(phases) - 1:
            if completion == 1 and phase_progress[phases[i+1]] > 0:
                line_style = 'solid'
                line_color = '#2ecc71'
            else:
                line_style = 'dot'
                line_color = 'rgba(52, 152, 219, 0.3)'
            
            fig.add_trace(go.Scatter(
                x=[i, i+1],
                y=[0, 0],
                mode='lines',
                line=dict(
                    color=line_color,
                    width=2,
                    dash=line_style
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

def create_dlt_types_matrix():
    """Create matrix showing relationships between DLT types."""
    dlt_types = {
        'DLT Permissionada Privada': {'Segurança': 0.9, 'Escalabilidade': 0.7, 'Eficiência': 0.8, 'Governança': 0.85},
        'DLT Híbrida': {'Segurança': 0.8, 'Escalabilidade': 0.85, 'Eficiência': 0.75, 'Governança': 0.8},
        'DLT Pública': {'Segurança': 0.85, 'Escalabilidade': 0.6, 'Eficiência': 0.5, 'Governança': 0.7},
        'DLT com Consenso Delegado': {'Segurança': 0.75, 'Escalabilidade': 0.9, 'Eficiência': 0.85, 'Governança': 0.75}
    }
    
    df = pd.DataFrame(dlt_types).T
    fig = px.imshow(
        df,
        color_continuous_scale='RdBu',
        aspect='auto',
        title="Matriz de Tipos de DLT"
    )
    return fig

def create_algorithm_groups_matrix():
    """Create matrix comparing different algorithm groups."""
    algorithm_groups = {
        'Alta Segurança': {'Complexidade': 0.8, 'Desempenho': 0.7, 'Descentralização': 0.9},
        'Alta Eficiência': {'Complexidade': 0.6, 'Desempenho': 0.9, 'Descentralização': 0.7},
        'Escalabilidade': {'Complexidade': 0.7, 'Desempenho': 0.8, 'Descentralização': 0.8},
        'Governança': {'Complexidade': 0.75, 'Desempenho': 0.75, 'Descentralização': 0.85}
    }
    
    df = pd.DataFrame(algorithm_groups).T
    fig = px.imshow(
        df,
        color_continuous_scale='RdBu',
        aspect='auto',
        title="Matriz de Grupos de Algoritmos"
    )
    return fig

def create_consensus_algorithms_matrix():
    """Create matrix showing consensus algorithm characteristics."""
    consensus_characteristics = {
        'PBFT': {'Segurança': 0.9, 'Escalabilidade': 0.7, 'Energia': 0.8, 'Governança': 0.85},
        'PoW': {'Segurança': 0.95, 'Escalabilidade': 0.5, 'Energia': 0.3, 'Governança': 0.7},
        'PoS': {'Segurança': 0.85, 'Escalabilidade': 0.8, 'Energia': 0.9, 'Governança': 0.8},
        'PoA': {'Segurança': 0.8, 'Escalabilidade': 0.9, 'Energia': 0.85, 'Governança': 0.75},
        'Tangle': {'Segurança': 0.8, 'Escalabilidade': 0.95, 'Energia': 0.9, 'Governança': 0.7}
    }
    
    df = pd.DataFrame(consensus_characteristics).T
    fig = px.imshow(
        df,
        color_continuous_scale='RdBu',
        aspect='auto',
        title="Matriz de Algoritmos de Consenso"
    )
    return fig

def create_evaluation_matrices(recommendation):
    """Create and display evaluation matrices with hierarchical relationships."""
    if not recommendation or recommendation['dlt'] == "Não disponível":
        st.warning("Recomendação indisponível.")
        return
    
    # Update session state with current recommendation
    st.session_state.current_recommendation = recommendation
    
    st.header("Recomendação de DLT e Análise")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"DLT Recomendada: {recommendation['dlt']}")
        st.write(f"**Tipo:** {recommendation['dlt_type']}")
        st.write(f"**Estrutura de Dados:** {recommendation['data_structure']}")
        st.write(f"**Grupo:** {recommendation['group']}")
        st.write("**Algoritmos:**")
        for algo in recommendation['algorithms']:
            st.write(f"• {algo}")
    
    with col2:
        if 'metrics' in recommendation:
            consistency_index = sum(recommendation['metrics'].values()) / len(recommendation['metrics'])
            st.subheader(f"Índice de Consistência: {consistency_index:.2f}")
            with st.expander("Explicação do Índice de Consistência"):
                st.write("O índice de consistência indica o quão bem a DLT atende aos requisitos de forma balanceada.")
                st.write("Valores mais próximos de 1 indicam maior consistência.")

    # Display matrix sections
    with st.expander("Matriz de Tipos de DLT"):
        st.plotly_chart(create_dlt_types_matrix(), use_container_width=True)
        st.write("""
        Esta matriz mostra as relações entre diferentes tipos de DLT e suas características principais.
        Cores mais escuras indicam maior adequação para cada característica.
        """)

    with st.expander("Matriz de Grupos de Algoritmos"):
        st.plotly_chart(create_algorithm_groups_matrix(), use_container_width=True)
        st.write("""
        Comparação entre diferentes grupos de algoritmos baseada em complexidade,
        desempenho e descentralização.
        """)

    with st.expander("Matriz de Algoritmos de Consenso"):
        st.plotly_chart(create_consensus_algorithms_matrix(), use_container_width=True)
        st.write("""
        Características detalhadas de cada algoritmo de consenso,
        incluindo segurança, escalabilidade, eficiência energética e governança.
        """)

    # Display additional information sections
    with st.expander("Casos de Uso"):
        st.write(recommendation['details']['use_cases'])
        st.subheader("Casos Reais")
        st.write(recommendation['details']['real_cases'])
    
    with st.expander("Desafios e Limitações"):
        st.write(recommendation['details']['challenges'])
    
    with st.expander("Referências"):
        st.write(recommendation['details']['references'])
    
    # Save recommendation functionality
    if st.session_state.authenticated:
        if st.button("Salvar Recomendação", help="Clique para salvar esta recomendação no seu perfil"):
            try:
                # Before saving, ensure recommendation has required fields
                save_data = {
                    'dlt': recommendation.get('dlt', 'N/A'),
                    'consensus': recommendation.get('algorithms', ['N/A'])[0],  # Get first algorithm or N/A
                    'dlt_type': recommendation.get('dlt_type', 'N/A'),
                    'group': recommendation.get('group', 'N/A')
                }
                save_recommendation(st.session_state.username, "Healthcare", save_data)
                st.success("Recomendação salva com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar recomendação: {str(e)}")
    else:
        st.info("Faça login para salvar suas recomendações.")

def run_decision_tree():
    """Main function to run the decision tree interface with improved state management."""
    st.title("Framework de Seleção de DLT")
    
    # Initialize session state for answers if not present
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    if st.button("Reiniciar", help="Clique para recomeçar o processo de seleção"):
        st.session_state.answers = {}
        if 'current_recommendation' in st.session_state:
            del st.session_state.current_recommendation
        st.experimental_rerun()
    
    # Determine current phase
    current_phase = None
    for q in questions:
        if q['id'] not in st.session_state.answers:
            current_phase = q['phase']
            break
    
    if current_phase:
        progress_fig = create_progress_animation(current_phase, st.session_state.answers, questions)
        st.plotly_chart(progress_fig, use_container_width=True)
    
    # Handle current question
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
            # Update recommendation immediately after answer changes
            if len(st.session_state.answers) == len(questions):
                st.session_state.current_recommendation = get_recommendation(st.session_state.answers)
            st.experimental_rerun()
    
    # Display recommendation when all questions are answered
    if len(st.session_state.answers) == len(questions):
        if 'current_recommendation' not in st.session_state:
            st.session_state.current_recommendation = get_recommendation(st.session_state.answers)
        create_evaluation_matrices(st.session_state.current_recommendation)
