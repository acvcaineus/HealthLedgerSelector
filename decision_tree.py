import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def create_progress_animation(current_phase, answers, questions):
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    fig = go.Figure()
    
    # Calculate progress for each phase
    phase_progress = {phase: 0 for phase in phases}
    phase_total = {phase: 0 for phase in phases}
    phase_characteristics = {phase: set() for phase in phases}
    
    # Collect phase information
    for q in questions:
        phase = q['phase']
        phase_total[phase] += 1
        phase_characteristics[phase].add(q['characteristic'])
        if q['id'] in answers:
            phase_progress[phase] += 1
    
    # Add animated nodes with progress indicators
    for i, phase in enumerate(phases):
        # Set color and size based on phase status
        if phase == current_phase:
            color = '#3498db'  # Blue for current
            size = 45  # Larger for current phase
        elif phase_progress[phase] > 0:
            color = '#2ecc71'  # Green for completed
            size = 40
        else:
            color = '#bdc3c7'  # Gray for pending
            size = 35
            
        # Create tooltip text
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

def show_recommendation(answers, weights, questions):
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação Final")
    
    # Main recommendation display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("DLT Recomendada")
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3 style='color: #1f77b4;'>{recommendation['dlt']}</h3>
            <p><strong>Grupo de Consenso:</strong> {recommendation['consensus_group']}</p>
            <p><strong>Algoritmo:</strong> {recommendation['consensus']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add collapsible explanations
        with st.expander("Ver Explicação da DLT Recomendada"):
            st.write(f"### Por que {recommendation['dlt']}?")
            st.write("Esta DLT foi selecionada com base em suas respostas:")
            for question_id, answer in answers.items():
                for q in questions:
                    if q['id'] == question_id:
                        st.write(f"- {q['text']}: **{answer}**")
            st.write("\n### Principais Características:")
            for metric, value in recommendation['evaluation_matrix'][recommendation['dlt']]['metrics'].items():
                if metric != 'academic_validation':
                    st.write(f"- **{metric}**: {float(value):.2f}")
        
        # Add use cases section
        with st.expander("Ver Casos de Uso Recomendados"):
            st.write("### Aplicações Recomendadas")
            use_cases = {
                "DLT Permissionada Privada": [
                    "Prontuários Eletrônicos (EMR)",
                    "Integração de Dados Sensíveis",
                    "Sistemas de Pagamento Descentralizados"
                ],
                "DLT Pública Permissionless": [
                    "Sistemas de Pagamento Descentralizados",
                    "Dados Críticos de Saúde Pública",
                    "Rastreamento de Medicamentos"
                ],
                "DLT Permissionada Simples": [
                    "Sistemas Locais de Saúde",
                    "Agendamento de Pacientes",
                    "Redes Locais de Hospitais"
                ],
                "DLT Híbrida": [
                    "Monitoramento de Saúde Pública",
                    "Redes Regionais de Saúde",
                    "Integração de EHRs"
                ],
                "DLT com Consenso Delegado": [
                    "Monitoramento de Saúde Pública",
                    "Redes Regionais de Saúde",
                    "Integração de EHRs"
                ],
                "DLT Pública": [
                    "Monitoramento IoT em Saúde",
                    "Dados em Tempo Real",
                    "Rastreamento de Dispositivos Médicos"
                ]
            }
            
            recommended_uses = use_cases.get(recommendation['dlt'], [])
            for use_case in recommended_uses:
                st.write(f"- {use_case}")
            
            st.write("\n### Exemplos de Implementação")
            implementation_examples = {
                "DLT Permissionada Privada": "Guardtime: Aplicado em sistemas de saúde da Estônia",
                "DLT Pública Permissionless": "MTBC: Gestão de registros eletrônicos de saúde (EHR)",
                "DLT Permissionada Simples": "ProCredEx: Validação de credenciais de profissionais de saúde",
                "DLT Híbrida": "Chronicled (Mediledger Project): Rastreamento de medicamentos",
                "DLT com Consenso Delegado": "Change Healthcare: Gestão de ciclo de receita",
                "DLT Pública": "Patientory: Compartilhamento de dados via IoT"
            }
            
            if recommendation['dlt'] in implementation_examples:
                st.write(f"**Exemplo Real:** {implementation_examples[recommendation['dlt']]}")
    
        with st.expander("Ver Explicação do Algoritmo de Consenso"):
            st.write(f"### Por que {recommendation['consensus']}?")
            st.write("Este algoritmo de consenso foi selecionado pelos seguintes motivos:")
            if recommendation['consensus'] in consensus_algorithms:
                for metric, value in consensus_algorithms[recommendation['consensus']].items():
                    st.write(f"- **{metric}**: {float(value):.2f}")
    
    with col2:
        st.subheader("Métricas")
        confidence_score = recommendation.get('confidence', False)
        confidence_value = recommendation.get('confidence_value', 0.0)
        st.metric(
            label="Índice de Confiança",
            value=f"{confidence_value:.2%}",
            delta=f"{'Alto' if confidence_score else 'Médio'}",
            help="Baseado na diferença entre o score máximo e a média dos scores"
        )
        
    # Add confidence index explanation
    with st.expander("Ver Explicação do Índice de Confiança"):
        st.write("### Como o Índice de Confiança é Calculado")
        st.write("""O índice de confiança é calculado usando os seguintes parâmetros:
        1. **Diferença entre Scores**: A diferença entre o score mais alto e a média dos scores
        2. **Consistência das Respostas**: Avaliação da coerência entre as respostas fornecidas
        3. **Threshold de Confiança**: 0.7 (70%) - valor mínimo para alta confiança
        
        Fórmula: `Confiabilidade = (max_score - mean_score) / max_score`
        """)
        
        value = recommendation.get('confidence_value', 0.0)
        st.metric(
            "Valor do Índice de Confiança",
            f"{value:.2%}",
            help="Valores acima de 70% indicam alta confiabilidade"
        )
    
    # Enhanced evaluation matrix display
    st.subheader("Matriz de Avaliação Detalhada")
    if 'evaluation_matrix' in recommendation:
        matrix_data = []
        y_labels = []
        
        for dlt, data in recommendation['evaluation_matrix'].items():
            y_labels.append(dlt)
            row = []
            for metric, value in data['metrics'].items():
                if metric != 'academic_validation':  # Skip academic validation
                    try:
                        row.append(float(value))
                    except (ValueError, TypeError):
                        row.append(0.0)
            matrix_data.append(row)
        
        metrics = [m for m in recommendation['evaluation_matrix'][y_labels[0]]['metrics'].keys() 
                  if m != 'academic_validation']
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix_data,
            x=metrics,
            y=y_labels,
            colorscale=[
                [0, "#ff0000"],    # Red for low values
                [0.4, "#ffff00"],  # Yellow for medium values
                [0.7, "#00ff00"]   # Green for high values
            ],
            hoverongaps=False,
            hovertemplate="<b>DLT:</b> %{y}<br>" +
                         "<b>Métrica:</b> %{x}<br>" +
                         "<b>Valor:</b> %{z:.2f}<br>" +
                         "<extra></extra>"
        ))
        
        fig.update_layout(
            title="Comparação Detalhada das DLTs",
            xaxis_title="Métricas",
            yaxis_title="DLTs",
            height=400,
            margin=dict(l=60, r=30, t=100, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Add Algorithm Evaluation Matrix
    with st.expander("Ver Matriz de Avaliação dos Algoritmos"):
        st.write("### Matriz de Avaliação dos Algoritmos de Consenso")
        
        # Create algorithm comparison matrix
        alg_matrix_data = []
        alg_labels = []
        
        for alg in recommendation['algorithms']:
            alg_labels.append(alg)
            row = []
            for metric in ['security', 'scalability', 'energy_efficiency', 'governance']:
                value = consensus_algorithms[alg][metric]
                row.append(float(value))
            alg_matrix_data.append(row)
        
        # Plot algorithm heatmap
        fig_alg = go.Figure(data=go.Heatmap(
            z=alg_matrix_data,
            x=['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
            y=alg_labels,
            colorscale='Viridis',
            hoverongaps=False,
            hovertemplate="<b>Algoritmo:</b> %{y}<br>" +
                         "<b>Métrica:</b> %{x}<br>" +
                         "<b>Valor:</b> %{z:.2f}<br>" +
                         "<extra></extra>"
        ))
        
        fig_alg.update_layout(
            title="Comparação dos Algoritmos de Consenso",
            height=400
        )
        
        st.plotly_chart(fig_alg, use_container_width=True)
    
    # Add Combined DLT-Algorithm Matrix
    with st.expander("Ver Matriz Combinada DLT-Algoritmo"):
        st.write("### Matriz de Compatibilidade DLT-Algoritmo")
        
        # Create combined matrix data
        combined_scores = {}
        for dlt, data in recommendation['evaluation_matrix'].items():
            dlt_scores = {}
            for alg in recommendation['algorithms']:
                # Calculate compatibility score
                score = 0
                for metric in ['security', 'scalability', 'energy_efficiency', 'governance']:
                    dlt_value = float(data['metrics'][metric])
                    alg_value = float(consensus_algorithms[alg][metric])
                    score += (dlt_value * alg_value) / 4
                dlt_scores[alg] = score
            combined_scores[dlt] = dlt_scores
        
        # Convert to matrix format
        combined_matrix = []
        dlt_labels = list(combined_scores.keys())
        alg_labels = recommendation['algorithms']
        
        for dlt in dlt_labels:
            row = []
            for alg in alg_labels:
                row.append(combined_scores[dlt][alg])
            combined_matrix.append(row)
        
        # Plot combined heatmap
        fig_combined = go.Figure(data=go.Heatmap(
            z=combined_matrix,
            x=alg_labels,
            y=dlt_labels,
            colorscale='Viridis',
            hoverongaps=False,
            hovertemplate="<b>DLT:</b> %{y}<br>" +
                         "<b>Algoritmo:</b> %{x}<br>" +
                         "<b>Score:</b> %{z:.2f}<br>" +
                         "<extra></extra>"
        ))
        
        fig_combined.update_layout(
            title="Compatibilidade entre DLTs e Algoritmos",
            height=400
        )
        
        st.plotly_chart(fig_combined, use_container_width=True)
    
    # Save recommendation option
    if st.button("Salvar Recomendação"):
        if st.session_state.get('username'):
            save_recommendation(
                st.session_state.username,
                'Healthcare DLT Selection',
                recommendation
            )
            st.success("Recomendação salva com sucesso!")
        else:
            st.warning("Faça login para salvar a recomendação.")
            
    # Add navigation button to metrics
    st.markdown("---")
    if st.button("Ver Métricas Detalhadas"):
        st.session_state.page = 'Métricas'
        st.experimental_rerun()
    
    return recommendation

def run_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")
    
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
    st.markdown(f"### Fase Atual: {current_phase}")
    st.progress(progress)

    current_question = None
    for q in questions:
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

    if len(st.session_state.answers) == len(questions):
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights, questions)

def restart_decision_tree():
    if st.button("Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()
