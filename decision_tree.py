import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def create_progress_animation(current_phase, answers, questions):
    """Creates an animated progress visualization for the questionnaire phases"""
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
    
    # Add animated nodes with progress indicators
    for i, phase in enumerate(phases):
        color = '#3498db' if phase == current_phase else '#2ecc71' if phase_progress[phase] > 0 else '#bdc3c7'
        size = 45 if phase == current_phase else 40 if phase_progress[phase] > 0 else 35
        
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
        
        # Add phase label with progress
        fig.add_annotation(
            x=i, y=-0.2,
            text=f"{phase}<br>({phase_progress[phase]}/{phase_total[phase]})",
            showarrow=False,
            font=dict(size=12)
        )
        
        if i < len(phases) - 1:
            fig.add_trace(go.Scatter(
                x=[i, i+1], y=[0, 0],
                mode='lines',
                line=dict(color='gray', width=2, dash='dot'),
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

def show_recommendation(answers, weights, questions):
    """Enhanced recommendation display with detailed metrics and explanations"""
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação Final")
    
    # Main recommendation display with enhanced visuals
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3 style='color: #1f77b4;'>{recommendation['dlt']}</h3>
            <p><strong>Grupo:</strong> {recommendation['consensus_group']}</p>
            <p><strong>Algoritmo:</strong> {recommendation['consensus']}</p>
            <p><strong>Validação Acadêmica:</strong> {recommendation['academic_validation'].get('score', 'N/A')}/5.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed explanations in expandable sections
        with st.expander("🔍 Ver Explicação Detalhada da DLT"):
            st.markdown(f"""
            ### Por que {recommendation['dlt']}?
            
            {recommendation['characteristics']}
            
            #### Casos de Uso Recomendados:
            {recommendation['use_cases']}
            
            #### Validação Acadêmica:
            - **Score:** {recommendation['academic_validation'].get('score', 'N/A')}/5.0
            - **Citações:** {recommendation['academic_validation'].get('citations', 'N/A')}
            - **Referência:** {recommendation['academic_validation'].get('reference', 'N/A')}
            - **Validação:** {recommendation['academic_validation'].get('validation', 'N/A')}
            """)
        
        with st.expander("⚙️ Ver Detalhes do Algoritmo de Consenso"):
            st.markdown(f"""
            ### Por que {recommendation['consensus']}?
            
            Este algoritmo foi selecionado com base nos seguintes critérios:
            """)
            
            # Create metrics visualization for consensus algorithm
            metrics = consensus_algorithms[recommendation['consensus']]
            metrics_df = pd.DataFrame({
                'Métrica': ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
                'Valor': [metrics['security'], metrics['scalability'], 
                         metrics['energy_efficiency'], metrics['governance']]
            })
            
            fig = go.Figure(data=[
                go.Bar(x=metrics_df['Métrica'], y=metrics_df['Valor'],
                      marker_color=['#ff9999', '#99ff99', '#99ccff', '#ffcc99'])
            ])
            
            fig.update_layout(
                title="Métricas do Algoritmo de Consenso",
                yaxis_title="Pontuação",
                yaxis=dict(range=[0, 5])
            )
            
            st.plotly_chart(fig)
    
    with col2:
        st.subheader("📊 Métricas de Confiança")
        confidence_score = recommendation.get('confidence', False)
        confidence_value = recommendation.get('confidence_value', 0.0)
        
        # Enhanced confidence metrics display
        st.markdown(f"""
        <div style='background-color: {'#d4edda' if confidence_score else '#fff3cd'}; 
                    padding: 15px; border-radius: 5px;'>
            <h4 style='margin: 0;'>Índice de Confiança</h4>
            <h2 style='margin: 10px 0;'>{confidence_value:.1%}</h2>
            <p style='margin: 0;'>{'Alta Confiança' if confidence_score else 'Confiança Moderada'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("ℹ️ Como é calculado?"):
            st.markdown("""
            O índice de confiança é calculado considerando:
            1. **Diferença de Scores**: Entre o maior score e a média
            2. **Consistência**: Das respostas fornecidas
            3. **Validação Acadêmica**: Pontuação baseada em estudos
            
            Um valor acima de 70% indica alta confiabilidade na recomendação.
            """)
    
    # Enhanced evaluation matrix visualization
    st.subheader("🎯 Matriz de Avaliação Detalhada")
    if 'evaluation_matrix' in recommendation:
        matrix_data = []
        metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
        
        for dlt, data in recommendation['evaluation_matrix'].items():
            row = [dlt] + [float(data['metrics'][m]) for m in metrics]
            matrix_data.append(row)
        
        df = pd.DataFrame(matrix_data, 
                         columns=['DLT', 'Segurança', 'Escalabilidade', 
                                 'Eficiência Energética', 'Governança'])
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=df.iloc[:, 1:].values,
            x=df.columns[1:],
            y=df['DLT'],
            colorscale='Viridis',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Comparação de Métricas entre DLTs",
            height=400
        )
        
        st.plotly_chart(fig)
        
        with st.expander("📋 Ver Tabela Completa"):
            st.table(df)
    
    return recommendation

def run_decision_tree():
    """Run the decision tree with enhanced UI and explanations"""
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")
    
    # Questions data structure
    questions = [
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

    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    progress = len(st.session_state.answers) / len(questions)
    
    # Show progress animation
    progress_fig = create_progress_animation(current_phase, st.session_state.answers, questions)
    st.plotly_chart(progress_fig, use_container_width=True)
    
    # Show current phase details
    st.markdown(f"""
    ### Fase Atual: {current_phase}
    <div style='margin-bottom: 20px;'>
        <div style='height: 20px; background-color: #f0f2f6; border-radius: 10px;'>
            <div style='width: {progress*100}%; height: 100%; background-color: #1f77b4; 
                      border-radius: 10px; transition: width 0.5s ease-in-out;'></div>
        </div>
        <p style='text-align: right; margin-top: 5px;'>{int(progress*100)}% Completo</p>
    </div>
    """, unsafe_allow_html=True)

    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    if current_question:
        st.subheader(f"Característica: {current_question['characteristic']}")
        
        # Enhanced question display with tooltip
        with st.container():
            st.info(f"ℹ️ {current_question['tooltip']}")
            response = st.radio(
                current_question["text"],
                current_question["options"],
                key=f"question_{current_question['id']}"
            )
        
        if st.button("Próxima Pergunta", key="next_question"):
            st.session_state.answers[current_question["id"]] = response
            st.rerun()

    if len(st.session_state.answers) == len(questions):
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights, questions)

def restart_decision_tree():
    """Reset the decision tree state"""
    if st.button("Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.rerun()
