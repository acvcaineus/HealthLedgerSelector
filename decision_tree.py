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
        
        # Evaluation Matrix with explanation
        with st.expander("Ver Matriz de Avaliação das DLTs", expanded=True):
            st.write("Esta matriz mostra a comparação das diferentes DLTs baseada nas métricas principais.")
            
            matrix_data = []
            y_labels = []
            
            metrics_pt = {
                "security": "Segurança",
                "scalability": "Escalabilidade",
                "energy_efficiency": "Eficiência Energética",
                "governance": "Governança"
            }
            
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

        # Algorithm Analysis Matrix
        with st.expander("Ver Matriz de Análise dos Algoritmos"):
            st.write("### Matriz de Avaliação dos Algoritmos de Consenso")
            st.write("Esta matriz compara os diferentes algoritmos de consenso baseados nas métricas principais.")
            
            alg_comparison = compare_algorithms(recommendation['consensus_group'])
            alg_matrix = []
            metrics = ["Segurança", "Escalabilidade", "Eficiência Energética", "Governança"]
            
            for alg in recommendation['algorithms']:
                row = []
                for metric in metrics:
                    value = alg_comparison[metric][alg]
                    row.append(value)
                alg_matrix.append(row)
            
            fig_alg = go.Figure(data=go.Heatmap(
                z=alg_matrix,
                x=metrics,
                y=recommendation['algorithms'],
                colorscale='Viridis',
                hoverongaps=False,
                hovertemplate="<b>Algoritmo:</b> %{y}<br>" +
                             "<b>Métrica:</b> %{x}<br>" +
                             "<b>Valor:</b> %{z:.2f}<br>" +
                             "<extra></extra>"
            ))
            
            fig_alg.update_layout(
                title="Comparação dos Algoritmos de Consenso",
                height=350,
                margin=dict(l=50, r=30, t=80, b=50),
                autosize=True
            )
            
            st.plotly_chart(fig_alg, use_container_width=True)

        # DLT-Algorithm Compatibility Matrix
        with st.expander("Ver Matriz de Compatibilidade DLT-Algoritmo"):
            st.write("### Matriz de Compatibilidade entre DLTs e Algoritmos")
            st.write("Esta matriz mostra a compatibilidade entre as DLTs recomendadas e os algoritmos de consenso.")
            
            combined_scores = calculate_compatibility_scores(recommendation)
            
            fig_compat = go.Figure(data=go.Heatmap(
                z=combined_scores['matrix'],
                x=combined_scores['algorithms'],
                y=combined_scores['dlts'],
                colorscale='RdYlGn',
                hoverongaps=False,
                hovertemplate="<b>DLT:</b> %{y}<br>" +
                             "<b>Algoritmo:</b> %{x}<br>" +
                             "<b>Compatibilidade:</b> %{z:.2f}<br>" +
                             "<extra></extra>"
            ))
            
            fig_compat.update_layout(
                title="Matriz de Compatibilidade",
                height=350,
                margin=dict(l=50, r=30, t=80, b=50),
                autosize=True
            )
            
            st.plotly_chart(fig_compat, use_container_width=True)
    
    with col2:
        st.subheader("Métricas de Confiança")
        confidence_value = recommendation.get('confidence_value', 0.0)
        st.metric(
            label="Índice de Confiança",
            value=f"{confidence_value:.2%}",
            delta=f"{'Alto' if confidence_value > 0.7 else 'Médio'}",
            help="Baseado na diferença entre o score máximo e a média dos scores"
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
