import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def show_recommendation(answers, weights):
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação Final")
    
    # Clean recommendation display
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
    
    with col2:
        st.subheader("Métricas de Confiança")
        confidence_score = recommendation.get('confidence', False)
        st.metric(
            label="Índice de Confiança",
            value=f"{'Alto' if confidence_score else 'Médio'}",
            delta=f"{'↑' if confidence_score else '→'}",
            help="Baseado na diferença entre o score máximo e a média dos scores"
        )
    
    # Decision Tree Metrics
    st.subheader("Métricas da Árvore de Decisão")
    col1, col2 = st.columns(2)
    
    with col1:
        classes = {k: v['score'] for k, v in recommendation['evaluation_matrix'].items()}
        gini = calcular_gini(classes)
        st.metric(
            label="Índice de Gini",
            value=f"{gini:.3f}",
            help="Medida de pureza da classificação (menor é melhor)"
        )
    
    with col2:
        entropy = calcular_entropia(classes)
        st.metric(
            label="Entropia",
            value=f"{entropy:.3f}",
            help="Medida de incerteza na decisão (menor é melhor)"
        )

    # Clean evaluation matrix display
    st.subheader("Matriz de Avaliação")
    if 'evaluation_matrix' in recommendation:
        matrix_data = []
        y_labels = []
        
        for dlt, data in recommendation['evaluation_matrix'].items():
            y_labels.append(dlt)
            row = []
            for metric, value in data['metrics'].items():
                if metric != "academic_validation":  # Skip academic validation metrics
                    try:
                        row.append(float(value))
                    except (ValueError, TypeError):
                        row.append(0.0)
            matrix_data.append(row)
        
        metrics = [m for m in recommendation['evaluation_matrix'][y_labels[0]]['metrics'].keys() 
                  if m != "academic_validation"]
        
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
            title="Avaliação Comparativa das DLTs",
            xaxis_title="Métricas",
            yaxis_title="DLTs",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Save recommendation button
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

    return recommendation

def show_interactive_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")
    
    # Restored all previous questions
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
    
    st.progress(progress)
    st.markdown(f"**Fase Atual:** {current_phase}")

    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    if current_question:
        st.subheader(f"Característica: {current_question['characteristic']}")
        response = st.radio(
            current_question["text"],
            current_question["options"],
            help=current_question["tooltip"]
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
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights)

def restart_decision_tree():
    if st.button("Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

def run_decision_tree():
    show_interactive_decision_tree()
    st.markdown("---")
    restart_decision_tree()
