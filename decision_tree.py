import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dlt_data import questions
from decision_logic import get_recommendation
from database import save_recommendation

def reset_all_states():
    """Reset all session states related to the decision tree and metrics."""
    keys_to_reset = [
        'answers',
        'current_recommendation',
        'metrics_calculated',
        'evaluation_matrices',
        'step',
        'scenario',
        'weights',
        'current_phase'
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    # Return to initial page
    st.session_state.page = 'Início'

def create_progress_animation(current_phase, answers, questions):
    """Create an animated progress visualization with enhanced interactivity."""
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    fig = go.Figure()
    
    # Calculate progress for each phase
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
            # Use different line styles based on completion
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

def run_decision_tree():
    """Main function to run the decision tree interface with improved state management."""
    st.title("Framework de Seleção de DLT")
    
    # Initialize session state for answers if not present
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    if st.button("Reiniciar", help="Clique para recomeçar o processo de seleção"):
        reset_all_states()
        st.experimental_rerun()
    
    # Determine current phase
    current_phase = None
    for q in questions:
        if q['id'] not in st.session_state.answers:
            current_phase = q['phase']
            break
    
    if current_phase:
        st.session_state.current_phase = current_phase
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
            if len(st.session_state.answers) == len(questions):
                st.session_state.current_recommendation = get_recommendation(st.session_state.answers)
            st.experimental_rerun()
    
    # Display recommendation when all questions are answered
    if len(st.session_state.answers) == len(questions):
        if 'current_recommendation' not in st.session_state:
            st.session_state.current_recommendation = get_recommendation(st.session_state.answers)
        st.session_state.current_phase = None  # Clear current phase when finished
        from metrics import show_metrics
        show_metrics()
