import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dlt_data import questions
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
        
        tooltip = f"""
        <b>{phase}</b><br>
        Progresso: {phase_progress[phase]}/{phase_total[phase]}<br>
        <br>Características:<br>
        {('<br>'.join(f'• {char}' for char in phase_characteristics[phase]))}
        """
        
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

    # Show classification path
    st.subheader("Caminho de Classificação")
    
    # Calculate consistency index
    consistency_index = sum(recommendation['metrics'].values()) / len(recommendation['metrics'])
    
    # Display DLT recommendation with consistency index
    st.subheader(f"DLT Recomendada: {recommendation['dlt']} (Índice de Consistência: {consistency_index:.2f})")
    
    with st.expander("Detalhes da Recomendação"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Tipo:** {recommendation['dlt_type']}")
            st.write(f"**Estrutura de Dados:** {recommendation['data_structure']}")
            st.write(f"**Grupo:** {recommendation['group']}")
        
        with col2:
            st.write("**Algoritmos:**")
            for algo in recommendation['algorithms']:
                st.write(f"• {algo}")
    
    # Add Save Recommendation button
    if st.session_state.authenticated:
        if st.button("Salvar Recomendação", help="Clique para salvar esta recomendação no seu perfil"):
            try:
                save_recommendation(
                    st.session_state.username,
                    "Healthcare",
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
    
    with st.expander("Características Técnicas"):
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

    with st.expander("Matrizes de Avaliação"):
        st.subheader("Matriz de Avaliação de DLTs")
        dlt_metrics_df = pd.DataFrame({
            'DLT': ['Hyperledger Fabric', 'Quorum', 'VeChain', 'IOTA', 'Ethereum 2.0'],
            'Segurança': [0.85, 0.78, 0.75, 0.80, 0.85],
            'Escalabilidade': [0.65, 0.70, 0.80, 0.85, 0.75],
            'Eficiência': [0.80, 0.80, 0.85, 0.90, 0.65],
            'Governança': [0.75, 0.78, 0.70, 0.60, 0.80]
        }).set_index('DLT')

        fig_dlt = px.imshow(
            dlt_metrics_df,
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        st.plotly_chart(fig_dlt)

        st.subheader("Matriz de Grupos de Algoritmos")
        algo_groups_df = pd.DataFrame({
            'Grupo': ['Alta Segurança', 'Alta Eficiência', 'Escalabilidade', 'IoT'],
            'Segurança': [0.90, 0.75, 0.80, 0.70],
            'Escalabilidade': [0.60, 0.85, 0.90, 0.95],
            'Eficiência': [0.70, 0.90, 0.85, 0.80],
            'Governança': [0.85, 0.70, 0.75, 0.65]
        }).set_index('Grupo')

        fig_groups = px.imshow(
            algo_groups_df,
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        st.plotly_chart(fig_groups)

    with st.expander("Guia de Interpretação"):
        st.info('''
        Como interpretar as matrizes:
        1. Matriz de DLTs: Mostra o desempenho geral de cada DLT nas principais métricas
        2. Matriz de Grupos: Apresenta as características de cada grupo de algoritmos
        3. Matriz de Algoritmos: Detalha o desempenho específico de cada algoritmo de consenso

        As cores mais escuras indicam valores mais altos (melhor desempenho).
        ''')

    with st.expander("Casos de Uso"):
        st.write(recommendation['details']['use_cases'])
        st.subheader("Casos Reais")
        st.write(recommendation['details']['real_cases'])
    
    with st.expander("Desafios e Limitações"):
        st.write(recommendation['details']['challenges'])
    
    with st.expander("Referências"):
        st.write(recommendation['details']['references'])

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
