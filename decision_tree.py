import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, compare_algorithms, calculate_compatibility_scores
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def create_radar_chart(data, title):
    """Create a radar chart for metrics visualization"""
    categories = list(data.keys())
    values = list(data.values())
    values.append(values[0])  # Complete the loop
    categories.append(categories[0])  # Complete the loop
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=title
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title=title,
        height=400
    )
    return fig

def create_entropy_evolution(entropy_values):
    """Create entropy evolution graph"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(entropy_values))),
        y=entropy_values,
        mode='lines+markers',
        name='Entropia',
        hovertemplate='Passo %{x}<br>Entropia: %{y:.3f}'
    ))
    
    fig.update_layout(
        title='Evolução da Entropia no Processo Decisório',
        xaxis_title='Passos do Processo',
        yaxis_title='Valor da Entropia',
        height=400
    )
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
    
    # Calculate metrics
    gini_value = calcular_gini(classes)
    entropy_value = calcular_entropia(classes)
    depth = calcular_profundidade_decisorio(list(range(len(answers))))
    
    # Metrics Dashboard
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Índice de Gini",
            f"{gini_value:.3f}",
            help="Medida de pureza da classificação (0-1)"
        )
    with col2:
        st.metric(
            "Entropia",
            f"{entropy_value:.3f}",
            help="Medida de incerteza na decisão"
        )
    with col3:
        st.metric(
            "Profundidade",
            f"{depth:.1f}",
            help="Complexidade do processo decisório"
        )
    
    # Gini Index Analysis with Radar Chart
    with st.expander("Análise do Índice de Gini", expanded=True):
        st.write("""
        ### Índice de Gini da Classificação
        
        O índice de Gini mede a pureza da classificação, indicando quão bem definidas estão as classes.
        - **Valores próximos a 0**: Indicam boa separação entre as classes
        - **Valores próximos a 1**: Indicam maior mistura entre as classes
        """)
        
        gini_data = {
            "Segurança": float(recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['security']),
            "Escalabilidade": float(recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['scalability']),
            "Eficiência": float(recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['energy_efficiency']),
            "Governança": float(recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['governance'])
        }
        
        gini_fig = create_radar_chart(gini_data, "Distribuição de Métricas")
        st.plotly_chart(gini_fig, use_container_width=True)

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
        
        # Detailed Justification
        with st.expander("Ver Justificativa da Recomendação"):
            st.write("### Por que esta DLT foi recomendada?")
            st.write(f"A {recommendation['dlt']} foi selecionada pelos seguintes motivos:")
            metrics_pt = {
                "security": "Segurança",
                "scalability": "Escalabilidade",
                "energy_efficiency": "Eficiência Energética",
                "governance": "Governança"
            }
            for metric, value in recommendation['evaluation_matrix'][recommendation['dlt']]['metrics'].items():
                st.write(f"- **{metrics_pt[metric]}**: {float(value):.2f}")
        
        # Evaluation Matrix
        with st.expander("Ver Matriz de Avaliação"):
            st.write("### Matriz de Avaliação Comparativa")
            matrix_data = []
            y_labels = []
            
            for dlt, data in recommendation['evaluation_matrix'].items():
                y_labels.append(dlt)
                row = []
                for metric in metrics_pt.keys():
                    try:
                        row.append(float(data['metrics'][metric]))
                    except (ValueError, TypeError):
                        row.append(0.0)
                matrix_data.append(row)
            
            fig = go.Figure(data=go.Heatmap(
                z=matrix_data,
                x=list(metrics_pt.values()),
                y=y_labels,
                colorscale='RdYlGn',
                hoverongaps=False,
                hovertemplate="<b>DLT:</b> %{y}<br>" +
                             "<b>Métrica:</b> %{x}<br>" +
                             "<b>Valor:</b> %{z:.2f}<br>" +
                             "<extra></extra>"
            ))
            
            fig.update_layout(
                title="Comparação Detalhada das DLTs",
                height=350,
                margin=dict(l=50, r=30, t=80, b=50)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Métricas de Confiança")
        confidence_value = recommendation.get('confidence_value', 0.0)
        
        confidence_label = (
            "Alto" if confidence_value >= 0.7 else
            "Médio" if confidence_value >= 0.4 else
            "Baixo"
        )
        
        confidence_description = (
            "Forte indicação de que esta é a melhor escolha" if confidence_value >= 0.7 else
            "Recomendação adequada, mas existem alternativas próximas" if confidence_value >= 0.4 else
            "Recomendação com reservas, considere analisar alternativas"
        )
        
        st.metric(
            label="Índice de Confiança",
            value=f"{confidence_value:.2%}",
            delta=confidence_label,
            help=f"{confidence_description}\n\nParâmetros:\n- Alto: ≥ 70%\n- Médio: 40-69%\n- Baixo: < 40%"
        )
        
        # Save recommendation if user is authenticated
        if st.session_state.get('authenticated'):
            save_recommendation(
                st.session_state.username,
                "Healthcare",
                recommendation
            )
            st.success("Recomendação salva com sucesso!")

def run_decision_tree():
    """Main entry point for the decision tree framework"""
    st.title("Framework de Seleção de DLT")
    
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    questions = [
        {
            "id": "privacy",
            "phase": "Aplicação",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere requisitos de LGPD e HIPAA"
        },
        {
            "id": "integration",
            "phase": "Aplicação",
            "text": "É necessária integração com outros sistemas de saúde?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere interoperabilidade com sistemas existentes"
        },
        {
            "id": "data_volume",
            "phase": "Infraestrutura",
            "text": "O sistema precisa lidar com grandes volumes de registros?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere o volume de transações esperado"
        },
        {
            "id": "energy_efficiency",
            "phase": "Infraestrutura",
            "text": "A eficiência energética é uma preocupação importante?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere o consumo de energia do sistema"
        }
    ]
    
    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    current_question = next((q for q in questions if q["id"] not in st.session_state.answers), None)
    
    if current_question:
        st.markdown(f"**Fase Atual:** {current_phase}")
        st.markdown(f"**Pergunta:** {current_question['text']}")
        st.info(f"Dica: {current_question['tooltip']}")
        
        response = st.radio("Selecione sua resposta:", current_question["options"])
        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question["id"]] = response
            st.experimental_rerun()
    
    if len(st.session_state.answers) == len(questions):
        weights = {
            "security": 0.4,
            "scalability": 0.25,
            "energy_efficiency": 0.20,
            "governance": 0.15
        }
        show_recommendation(st.session_state.answers, weights, questions)
        
        if st.button("Reiniciar Processo"):
            st.session_state.answers = {}
            st.experimental_rerun()
