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
    values.append(values[0])
    categories.append(categories[0])
    
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

def create_tree_depth_visualization(depth, max_depth=10):
    """Create a visualization for decision tree depth"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=depth,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, max_depth]},
            'steps': [
                {'range': [0, 3], 'color': "lightgreen"},
                {'range': [3, 6], 'color': "yellow"},
                {'range': [6, max_depth], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': depth
            }
        },
        title={'text': "Profundidade da Árvore"}
    ))
    
    fig.update_layout(height=300)
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

def show_detailed_comparisons(recommendation):
    """Show detailed comparisons between DLTs and algorithms"""
    st.header("Comparações Detalhadas")
    
    # Algorithm Evaluation Matrix
    st.subheader("Matriz de Avaliação de Algoritmos")
    algorithms_data = compare_algorithms(recommendation['consensus_group'])
    
    fig = go.Figure(data=go.Heatmap(
        z=[[v[alg] for alg in recommendation['algorithms']] for v in algorithms_data.values()],
        x=recommendation['algorithms'],
        y=list(algorithms_data.keys()),
        colorscale='RdYlGn',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Comparação de Algoritmos de Consenso",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # DLT-Algorithm Compatibility Matrix
    st.subheader("Matriz de Compatibilidade DLT-Algoritmo")
    compatibility = calculate_compatibility_scores(recommendation)
    
    fig = go.Figure(data=go.Heatmap(
        z=compatibility['matrix'],
        x=compatibility['algorithms'],
        y=compatibility['dlts'],
        colorscale='RdYlGn',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Compatibilidade entre DLTs e Algoritmos",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

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
        
        # User Answers Impact
        with st.expander("Impacto das Respostas"):
            st.write("### Como suas respostas influenciaram a decisão")
            for q in questions:
                if q["id"] in answers:
                    impact = "Alto" if answers[q["id"]] == "Sim" else "Baixo"
                    st.write(f"**{q['text']}**")
                    st.write(f"Sua resposta: {answers[q['id']]} (Impacto: {impact})")
        
        # Consensus Algorithm Characteristics
        with st.expander("Características do Algoritmo de Consenso"):
            st.write("### Pesos das Características")
            for metric, weight in weights.items():
                st.write(f"**{metric.replace('_', ' ').title()}**: {weight*100:.0f}%")
        
        # Application Scenarios
        with st.expander("Cenários de Aplicação"):
            scenarios = {
                "DLT Permissionada Privada": [
                    "Prontuários Eletrônicos (EMR)",
                    "Integração de Dados Sensíveis",
                    "Sistemas de Pagamento Descentralizados"
                ],
                "DLT Pública": [
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
                ]
            }
            
            st.write("### Cenários Recomendados de Uso")
            if recommendation['dlt'] in scenarios:
                for scenario in scenarios[recommendation['dlt']]:
                    st.write(f"- {scenario}")
        
        # Evaluation Matrix
        with st.expander("Matriz de Avaliação"):
            st.write("### Matriz de Avaliação Comparativa")
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
