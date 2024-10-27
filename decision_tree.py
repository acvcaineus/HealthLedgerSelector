import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, compare_algorithms, calculate_compatibility_scores
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def create_progress_animation(current_phase, answers, questions):
    """Create an animated progress visualization for the decision process"""
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
    
    # Update layout with responsive height
    fig.update_layout(
        showlegend=False,
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
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

def get_confidence_level(value):
    """Get confidence level and description based on value"""
    if value >= 0.7:
        return "Alto", "Forte indicação de que esta é a melhor escolha"
    elif value >= 0.4:
        return "Médio", "Recomendação adequada, mas existem alternativas próximas"
    else:
        return "Baixo", "Recomendação com reservas, considere analisar alternativas"

def create_gini_visualization(value):
    """Create a visualization for Gini index"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 0.3], 'color': "lightgreen"},
                {'range': [0.3, 0.6], 'color': "yellow"},
                {'range': [0.6, 1], 'color': "red"}
            ],
        }
    ))
    fig.update_layout(height=300)
    return fig

def show_metrics_explanation():
    """Display enhanced metrics explanations with interactive visualizations"""
    st.header("Análise das Métricas do Processo Decisório")
    
    answers = st.session_state.get('answers', {})
    if not answers:
        st.warning("Complete o processo de seleção para ver as métricas detalhadas.")
        return
        
    weights = {"security": 0.4, "scalability": 0.25, "energy_efficiency": 0.2, "governance": 0.15}
    recommendation = get_recommendation(answers, weights)
    classes = {k: v['score'] for k, v in recommendation['evaluation_matrix'].items()}
    
    gini_value = calcular_gini(classes)
    entropy_value = calcular_entropia(classes)
    depth = calcular_profundidade_decisoria(list(range(len(answers))))
    
    # Gini Index Analysis
    with st.expander("Análise do Índice de Gini"):
        st.write("### Índice de Gini da Classificação")
        gini_fig = create_gini_visualization(gini_value)
        st.plotly_chart(gini_fig)
        st.write(f"\n**Análise**: O índice de Gini de {gini_value:.3f} indica " +
                ("uma boa separação entre as classes." if gini_value < 0.3 else
                 "uma separação moderada entre as classes." if gini_value < 0.6 else
                 "uma alta mistura entre as classes."))
    
    # Entropy Analysis
    with st.expander("Análise da Entropia"):
        st.write("### Entropia da Classificação")
        st.write("""
        A entropia mede a incerteza ou aleatoriedade na distribuição das classes. 
        Quanto menor a entropia, mais certeza temos na classificação.
        """)
        st.metric("Entropia", f"{entropy_value:.3f}")
        st.write(f"\n**Análise**: O valor de entropia {entropy_value:.3f} indica " +
                ("baixa incerteza na classificação." if entropy_value < 1 else
                 "incerteza moderada na classificação." if entropy_value < 2 else
                 "alta incerteza na classificação."))
    
    # Decision Tree Depth Analysis
    with st.expander("Análise da Profundidade Decisória"):
        st.write("### Profundidade da Árvore de Decisão")
        st.write("""
        A profundidade da árvore indica a complexidade do processo decisório.
        Uma menor profundidade geralmente indica um processo mais direto e interpretável.
        """)
        st.metric("Profundidade Média", f"{depth:.2f}")
        st.write(f"\n**Análise**: A profundidade média de {depth:.2f} indica " +
                ("um processo decisório simples." if depth < 3 else
                 "um processo decisório de complexidade moderada." if depth < 5 else
                 "um processo decisório complexo."))

def show_recommendation(answers, weights, questions):
    """Display the final recommendation with enhanced visualizations"""
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
        
        # Metrics translation dictionary
        metrics_pt = {
            "security": "Segurança",
            "scalability": "Escalabilidade",
            "energy_efficiency": "Eficiência Energética",
            "governance": "Governança"
        }
        
        # Detailed Justification
        with st.expander("Ver Justificativa da Recomendação"):
            st.write("### Por que esta DLT foi recomendada?")
            st.write(f"A {recommendation['dlt']} foi selecionada pelos seguintes motivos:")
            for metric, value in recommendation['evaluation_matrix'][recommendation['dlt']]['metrics'].items():
                st.write(f"- **{metrics_pt[metric]}**: {float(value):.2f}")
            
            st.write("\n### Por que outras DLTs não foram selecionadas:")
            for dlt, data in recommendation['evaluation_matrix'].items():
                if dlt != recommendation['dlt']:
                    st.write(f"\n**{dlt}**:")
                    differences = []
                    for metric, value in data['metrics'].items():
                        ref_value = recommendation['evaluation_matrix'][recommendation['dlt']]['metrics'][metric]
                        if float(value) < float(ref_value):
                            differences.append(f"{metrics_pt[metric]} ({float(value):.2f} vs {float(ref_value):.2f})")
                    st.write("Pontuação inferior em: " + ", ".join(differences))
        
        # Application Scenarios
        with st.expander("Ver Cenários de Aplicação"):
            st.write("### Cenários Recomendados de Uso")
            scenarios = {
                "DLT Permissionada Privada": [
                    "Prontuários Eletrônicos (EMR)",
                    "Integração de Dados Sensíveis",
                    "Sistemas de Pagamento Descentralizados"
                ],
                "DLT Pública Permissionless": [
                    "Dados Públicos de Saúde",
                    "Registro de Pesquisas Clínicas",
                    "Rastreamento de Medicamentos"
                ],
                "DLT Permissionada Simples": [
                    "Sistemas Locais de Saúde",
                    "Agendamento de Pacientes",
                    "Redes Locais de Hospitais"
                ],
                "DLT Híbrida": [
                    "Integração de Sistemas de Saúde",
                    "Compartilhamento Controlado de Dados",
                    "Redes Regionais de Saúde"
                ],
                "DLT com Consenso Delegado": [
                    "Gestão de Credenciais Médicas",
                    "Autorização de Procedimentos",
                    "Validação de Documentos"
                ],
                "DLT Pública": [
                    "Monitoramento IoT em Saúde",
                    "Dados em Tempo Real",
                    "Pesquisa Colaborativa"
                ]
            }
            
            if recommendation['dlt'] in scenarios:
                for scenario in scenarios[recommendation['dlt']]:
                    st.write(f"- {scenario}")
        
        # Evaluation Matrix
        with st.expander("Ver Matriz de Avaliação das DLTs"):
            st.write("Esta matriz mostra a comparação das diferentes DLTs baseada nas métricas principais.")
            
            matrix_data = []
            y_labels = []
            
            for dlt, data in recommendation['evaluation_matrix'].items():
                y_labels.append(dlt)
                row = []
                for metric, value in data['metrics'].items():
                    if metric in metrics_pt:
                        try:
                            row.append(float(value))
                        except (ValueError, TypeError):
                            row.append(0.0)
                matrix_data.append(row)
            
            metrics = [metrics_pt[m] for m in metrics_pt.keys()]
            
            fig = go.Figure(data=go.Heatmap(
                z=matrix_data,
                x=metrics,
                y=y_labels,
                colorscale=[
                    [0, "#ff0000"],
                    [0.4, "#ffff00"],
                    [0.7, "#00ff00"]
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
                height=350,
                margin=dict(l=50, r=30, t=80, b=50),
                autosize=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Métricas de Confiança")
        confidence_value = recommendation.get('confidence_value', 0.0)
        level, description = get_confidence_level(confidence_value)
        
        st.metric(
            label="Índice de Confiança",
            value=f"{confidence_value:.2%}",
            delta=level,
            help=f"{description}\n\nParâmetros:\n- Alto: ≥ 70%\n- Médio: 40-69%\n- Baixo: < 40%"
        )
        
        # Technical Metrics Details
        with st.expander("Ver Detalhes dos Cálculos"):
            st.write("### Cálculos Detalhados das Métricas")
            
            gini_value = calcular_gini(
                {dlt: data['score'] for dlt, data in recommendation['evaluation_matrix'].items()}
            )
            entropy_value = calcular_entropia(
                {dlt: data['score'] for dlt, data in recommendation['evaluation_matrix'].items()}
            )
            
            st.latex(r"\text{Índice de Gini} = 1 - \sum_{i=1}^{n} p_i^2")
            st.write(f"Valor calculado: {gini_value:.3f}")
            
            st.latex(r"\text{Entropia} = -\sum_{i=1}^{n} p_i \log_2(p_i)")
            st.write(f"Valor calculado: {entropy_value:.3f}")
    
    return recommendation

def show_interactive_decision_tree():
    """Interactive decision tree with enhanced state management"""
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
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
    
    # Show progress animation
    progress_fig = create_progress_animation(current_phase, st.session_state.answers, questions)
    st.plotly_chart(progress_fig, use_container_width=True)
    
    # Show current question
    current_question = next((q for q in questions if q["id"] not in st.session_state.answers), None)
    if current_question:
        st.markdown(f"**Fase Atual:** {current_phase}")
        st.markdown(f"**Característica:** {current_question['characteristic']}")
        st.info(f"Dica: {current_question['tooltip']}")
        
        response = st.radio(current_question["text"], current_question["options"])
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
    """Reset the decision tree process"""
    if st.button("Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

def run_decision_tree():
    """Main entry point for the decision tree framework"""
    st.title("Framework de Seleção de DLT")
    show_interactive_decision_tree()
