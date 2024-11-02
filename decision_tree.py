import streamlit as st
import plotly.graph_objects as go
from dlt_data import academic_references, questions

def create_evaluation_matrices(recommendation):
    if not recommendation or 'evaluation_matrix' not in recommendation:
        return
        
    st.subheader("Matriz de Avaliação Detalhada")
    
    # Create DLT comparison heatmap
    st.subheader("Comparação Detalhada das DLTs")
    metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
    weights = {
        'security': 0.40,
        'scalability': 0.25,
        'energy_efficiency': 0.20,
        'governance': 0.15
    }
    
    # Prepare data for heatmap
    dlts = list(recommendation['evaluation_matrix'].keys())
    metric_values = []
    weighted_scores = []
    
    for metric in metrics:
        row = []
        for dlt in dlts:
            base_score = float(recommendation['evaluation_matrix'][dlt]['metrics'][metric])
            weighted_score = base_score * weights[metric]
            row.append(weighted_score)
        metric_values.append(row)
        weighted_scores.append(sum(row))
    
    # Create enhanced heatmap with academic references
    fig = go.Figure(data=go.Heatmap(
        z=metric_values,
        x=dlts,
        y=['Segurança (40%)', 'Escalabilidade (25%)', 
           'Eficiência Energética (20%)', 'Governança (15%)'],
        colorscale='RdBu',
        hoverongaps=False,
        hovertemplate="<b>DLT:</b> %{x}<br>" +
                     "<b>Métrica:</b> %{y}<br>" +
                     "<b>Score Base:</b> %{customdata[0]:.2f}<br>" +
                     "<b>Score Ponderado:</b> %{z:.2f}<br>" +
                     "<b>Fonte:</b> %{customdata[1]}<br>" +
                     "<extra></extra>",
        customdata=[[score, academic_references.get(dlt, {}).get('source', 'N/A')] 
                   for score, dlt in zip(metric_values, dlts)]
    ))
    
    fig.update_layout(
        title={
            'text': "Matriz de Avaliação de DLTs com Pesos Acadêmicos",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="DLTs",
        yaxis_title="Métricas",
        height=500,
        annotations=[
            dict(
                text="Baseado em pesquisas acadêmicas 2024-2025",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=-0.15,
                font=dict(size=10)
            )
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add academic validation section
    with st.expander("📚 Validação Acadêmica"):
        st.markdown("""
        ### Fontes Acadêmicas
        
        As métricas e pesos utilizados nesta matriz são baseados em pesquisas recentes:
        
        1. **Segurança (40%)**: 
           - Fonte: Liu et al. (2024)
           - Impacto: Alta prioridade para dados de saúde
        
        2. **Escalabilidade (25%)**:
           - Fonte: Mehmood et al. (2025)
           - Impacto: Crucial para crescimento do sistema
        
        3. **Eficiência Energética (20%)**:
           - Fonte: Salim et al. (2024)
           - Impacto: Sustentabilidade do sistema
        
        4. **Governança (15%)**:
           - Fonte: Popoola et al. (2024)
           - Impacto: Flexibilidade operacional
        """)
    
    # Add weighted scores explanation
    st.markdown("### Pontuação Final Ponderada")
    cols = st.columns(len(dlts))
    for idx, (dlt, score) in enumerate(zip(dlts, [sum(row) for row in zip(*metric_values)])):
        with cols[idx]:
            st.metric(
                label=dlt,
                value=f"{score:.2f}",
                delta=f"Ref: {academic_references.get(dlt, {}).get('academic_score', 'N/A')}",
                help=f"Score ponderado baseado em métricas acadêmicas\nFonte: {academic_references.get(dlt, {}).get('source', 'N/A')}"
            )

    # Display visualization legend
    st.markdown("""
    ### 🎨 Legenda da Visualização
    
    - **Cores**: Escala RdBu (Red-Blue)
        - 🔵 Azul escuro: Valores mais altos
        - ⚪ Branco: Valores médios
        - 🔴 Vermelho: Valores mais baixos
        
    - **Tamanho dos Círculos**: Representa o peso relativo da métrica
    - **Tooltips**: Passe o mouse sobre os elementos para ver detalhes e referências acadêmicas
    """)

def create_progress_animation(current_phase, answers, questions):
    """Create an animated progress visualization with improved features."""
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    fig = go.Figure()
    
    # Initialize progress tracking
    phase_progress = {phase: 0 for phase in phases}
    phase_total = {phase: 0 for phase in phases}
    phase_characteristics = {phase: set() for phase in phases}
    
    # Calculate progress for each phase
    for q in questions:
        phase = q['phase']
        phase_total[phase] += 1
        phase_characteristics[phase].add(q['characteristic'])
        if q['id'] in answers:
            phase_progress[phase] += 1
    
    # Create visualization elements
    for i, phase in enumerate(phases):
        # Dynamic styling
        if phase == current_phase:
            color = '#3498db'
            size = 45
        elif phase_progress[phase] > 0:
            color = '#2ecc71'
            size = 40
        else:
            color = '#bdc3c7'
            size = 35
        
        # Create tooltip
        tooltip = f"<b>{phase}</b><br>"
        tooltip += f"Progresso: {phase_progress[phase]}/{phase_total[phase]}<br>"
        tooltip += "<br>Características:<br>"
        tooltip += "<br>".join([f"- {char}" for char in phase_characteristics[phase]])
        
        # Add phase marker
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
        
        # Add connecting lines
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

def run_decision_tree():
    """Main function to run the decision tree interface."""
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")

    st.warning("⚠️ Atenção: Reiniciar o processo irá apagar todas as respostas já fornecidas!")
    if st.button("🔄 Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

    st.markdown("---")
    
    # Define questions with phases and characteristics
    questions_list = [
        {
            "id": "privacy",
            "phase": "Aplicação",
            "characteristic": "Privacidade",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere requisitos de LGPD e HIPAA"
        },
        {
            "id": "integration",
            "phase": "Aplicação",
            "characteristic": "Integração",
            "text": "É necessária integração com outros sistemas de saúde?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere interoperabilidade com sistemas existentes"
        },
        {
            "id": "data_volume",
            "phase": "Infraestrutura",
            "characteristic": "Volume de Dados",
            "text": "O sistema precisa lidar com grandes volumes de registros?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere o volume de transações esperado"
        },
        {
            "id": "energy_efficiency",
            "phase": "Infraestrutura",
            "characteristic": "Eficiência Energética",
            "text": "A eficiência energética é uma preocupação importante?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere o consumo de energia do sistema"
        },
        {
            "id": "network_security",
            "phase": "Consenso",
            "characteristic": "Segurança",
            "text": "É necessário alto nível de segurança na rede?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere requisitos de segurança"
        },
        {
            "id": "scalability",
            "phase": "Consenso",
            "characteristic": "Escalabilidade",
            "text": "A escalabilidade é uma característica chave?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere necessidades futuras de crescimento"
        },
        {
            "id": "governance_flexibility",
            "phase": "Internet",
            "characteristic": "Governança",
            "text": "A governança do sistema precisa ser flexível?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere necessidades de adaptação"
        },
        {
            "id": "interoperability",
            "phase": "Internet",
            "characteristic": "Interoperabilidade",
            "text": "A interoperabilidade com outros sistemas é importante?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere integração com outras redes"
        }
    ]

    # Get current phase and create progress visualization
    current_phase = next((q["phase"] for q in questions_list if q["id"] not in st.session_state.answers), "Completo")
    progress = len(st.session_state.answers) / len(questions_list)
    
    # Show progress animation
    progress_fig = create_progress_animation(current_phase, st.session_state.answers, questions_list)
    st.plotly_chart(progress_fig, use_container_width=True)
    
    st.markdown(f"### Fase Atual: {current_phase}")
    st.progress(progress)

    # Get current question
    current_question = None
    for q in questions_list:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    if current_question:
        st.subheader(f"Característica: {current_question['characteristic']}")
        st.info(f"Dica: {current_question['tooltip']}")
        response = st.radio(
            current_question["text"],
            current_question["options"]
        )

        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question["id"]] = response
            st.experimental_rerun()

    # Show recommendation when all questions are answered
    if len(st.session_state.answers) == len(questions_list):
        from decision_logic import get_recommendation
        
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        st.session_state.recommendation = get_recommendation(st.session_state.answers, weights)
        
        # Display recommendation
        st.header("Recomendação")
        st.write(f"DLT Recomendada: {st.session_state.recommendation['dlt']}")
        st.write(f"Algoritmo de Consenso: {st.session_state.recommendation['consensus']}")
        
        # Add save button for authenticated users
        if st.session_state.get('authenticated', False):
            if st.button("💾 Salvar Recomendação"):
                from database import save_recommendation
                save_recommendation(
                    st.session_state.username,
                    "Healthcare",
                    st.session_state.recommendation
                )
                st.success("Recomendação salva com sucesso!")
        
        # Show evaluation matrices
        create_evaluation_matrices(st.session_state.recommendation)
