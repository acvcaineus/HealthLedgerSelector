import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from dlt_data import questions, dlt_metrics
from decision_logic import get_recommendation, dlt_classification
from database import save_recommendation

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

def create_evaluation_matrices(recommendation):
    """Create and display evaluation matrices with hierarchical relationships."""
    if not recommendation or recommendation['dlt'] == "Não disponível":
        st.warning("Recomendação indisponível.")
        return
    
    st.header("Recomendação de DLT e Análise")
    
    # Display DLT details in organized sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Classificação")
        st.write(f"**DLT:** {recommendation['dlt']}")
        st.write(f"**Tipo:** {recommendation['dlt_type']}")
        st.write(f"**Estrutura de Dados:** {recommendation['data_structure']}")
        st.write(f"**Grupo:** {recommendation['group']}")
    
    with col2:
        st.subheader("Algoritmos")
        for algo in recommendation['algorithms']:
            st.write(f"• {algo}")

    # Calculate and display consistency index
    consistency_index = sum(recommendation['metrics'].values()) / len(recommendation['metrics'])
    st.info(f"Índice de Consistência: {consistency_index:.2f}")
    st.write("*O índice de consistência indica o quão bem a DLT atende aos requisitos de forma balanceada. Valores mais próximos de 1 indicam maior consistência.*")
    
    # Add Save Recommendation button
    if st.session_state.authenticated:
        if st.button("Salvar Recomendação", help="Clique para salvar esta recomendação no seu perfil"):
            try:
                save_recommendation(
                    st.session_state.username,
                    "Healthcare",  # Default scenario
                    {
                        "dlt": recommendation['dlt'],
                        "dlt_type": recommendation['dlt_type'],
                        "consensus": ", ".join(recommendation['algorithms']),
                        "group": recommendation['group']
                    }
                )
                st.success("Recomendação salva com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar recomendação: {str(e)}")
    else:
        st.info("Faça login para salvar suas recomendações.")

    # Additional sections
    with st.expander("Casos de Uso"):
        st.write(recommendation['details']['use_cases'])
        st.subheader("Casos Reais")
        st.write(recommendation['details']['real_cases'])
    
    with st.expander("Desafios e Limitações"):
        st.write(recommendation['details']['challenges'])
    
    with st.expander("Referências"):
        st.write(recommendation['details']['references'])
    
    # Updated comparison table with all DLTs
    st.subheader("Comparação de DLTs")
    comparison_data = []
    for dlt_name, dlt_info in dlt_classification.items():
        metrics = dlt_metrics.get(dlt_name, {}).get('metrics', {})
        comparison_data.append({
            'DLT': dlt_name,
            'Tipo': dlt_info['type'],
            'Estrutura': dlt_info['data_structure'],
            'Grupo': dlt_info['group'],
            'Score': recommendation['evaluation_matrix'].get(dlt_name, {}).get('score', 0.0),
            'Segurança': metrics.get('security', 0.0),
            'Escalabilidade': metrics.get('scalability', 0.0),
            'Eficiência': metrics.get('energy_efficiency', 0.0),
            'Governança': metrics.get('governance', 0.0)
        })

    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.sort_values('Score', ascending=False)
    
    def highlight_selected(df):
        return pd.DataFrame(
            np.where(df.index == recommendation['dlt'],
                    'background-color: #e6f3ff; font-weight: bold',
                    ''),
            index=df.index,
            columns=df.columns
        )
    
    styled_df = comparison_df.style\
        .apply(highlight_selected)\
        .format({
            'Score': '{:.2f}',
            'Segurança': '{:.2f}',
            'Escalabilidade': '{:.2f}',
            'Eficiência': '{:.2f}',
            'Governança': '{:.2f}'
        })
    
    st.table(styled_df)

def run_decision_tree():
    """Main function to run the decision tree interface."""
    st.title("Framework de Seleção de DLT")
    
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    if st.button("Reiniciar", help="Clique para recomeçar o processo de seleção"):
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
