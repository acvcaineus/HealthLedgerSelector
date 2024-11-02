import streamlit as st
import plotly.graph_objects as go
import math
from decision_logic import get_recommendation, consensus_algorithms, consensus_groups, compare_algorithms
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_peso_caracteristica, get_metric_explanation)

def create_progress_animation(current_phase, answers, questions):
    """Create an animated progress visualization."""
    phases = ["Aplicação", "Consenso", "Infraestrutura", "Internet"]
    
    # Create base figure
    fig = go.Figure()
    
    # Calculate progress for each phase
    phase_progress = {phase: 0 for phase in phases}
    questions_per_phase = {phase: 0 for phase in phases}
    
    # Count total questions per phase
    for q in questions:
        questions_per_phase[q["phase"]] += 1
    
    # Calculate answered questions per phase
    for q in questions:
        if q["id"] in answers:
            phase_progress[q["phase"]] += 1
    
    # Convert to percentages
    for phase in phases:
        if questions_per_phase[phase] > 0:
            phase_progress[phase] = (phase_progress[phase] / questions_per_phase[phase]) * 100
    
    # Colors for different phases
    colors = {
        "Aplicação": "#1f77b4",  # Blue
        "Consenso": "#2ca02c",   # Green
        "Infraestrutura": "#ff7f0e",  # Orange
        "Internet": "#d62728"    # Red
    }
    
    # Add bars for each phase
    for i, phase in enumerate(phases):
        fig.add_trace(go.Bar(
            name=phase,
            x=[phase],
            y=[phase_progress[phase]],
            marker_color=colors[phase],
            text=f"{phase_progress[phase]:.0f}%",
            textposition='auto',
        ))
    
    # Update layout
    fig.update_layout(
        title="Progresso por Fase",
        yaxis_title="Progresso (%)",
        yaxis=dict(range=[0, 100]),
        showlegend=True,
        barmode='group',
        height=300
    )
    
    # Add phase descriptions
    descriptions = {
        "Aplicação": "Questões sobre privacidade e integração",
        "Consenso": "Questões sobre segurança e escalabilidade",
        "Infraestrutura": "Questões sobre volume de dados e eficiência",
        "Internet": "Questões sobre governança e interoperabilidade"
    }
    
    # Add annotations for current phase
    if current_phase in phases:
        fig.add_annotation(
            x=current_phase,
            y=phase_progress[current_phase],
            text="Fase Atual",
            showarrow=True,
            arrowhead=1
        )
    
    return fig

def show_metrics():
    st.header("Métricas Técnicas do Processo de Decisão")
    
    if 'recommendation' in st.session_state and 'answers' in st.session_state:
        rec = st.session_state.recommendation
        answers = st.session_state.answers
        
        # Calculate metrics
        if 'evaluation_matrix' in rec:
            classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
            gini = calcular_gini(classes)
            entropy = calcular_entropia(classes)
            depth = calcular_profundidade_decisoria(list(range(len(answers))))
            
            total_nos = len(answers) * 2 + 1
            nos_podados = total_nos - len(answers) - 1
            pruning_metrics = calcular_pruning(total_nos, nos_podados)
            
            # Display metrics in organized sections
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Métricas de Classificação")
                gini_exp = get_metric_explanation("gini", gini)
                st.metric(
                    label="Índice de Gini",
                    value=f"{gini:.3f}",
                    help=gini_exp["description"]
                )
                
                with st.expander("ℹ️ Detalhes do Índice de Gini"):
                    st.markdown(f"""
                    **Fórmula:** {gini_exp["formula"]}
                    
                    **Interpretação:** {gini_exp["interpretation"]}
                    
                    **Valor Atual:** {gini:.3f}
                    """)
                
                entropy_exp = get_metric_explanation("entropy", entropy)
                st.metric(
                    label="Entropia",
                    value=f"{entropy:.3f} bits",
                    help=entropy_exp["description"]
                )
            
            with col2:
                st.subheader("🌳 Métricas da Árvore")
                st.metric(
                    label="Profundidade da Árvore",
                    value=f"{depth:.1f}",
                    help="Número médio de decisões necessárias"
                )
                
                pruning_exp = get_metric_explanation("pruning", pruning_metrics)
                st.metric(
                    label="Taxa de Poda",
                    value=f"{pruning_metrics['pruning_ratio']:.2%}",
                    help=pruning_exp["description"]
                )
            
            # Priority Characteristic Weights Section
            st.subheader("⚖️ Pesos das Características")
            
            weights = {
                "security": 0.4,
                "scalability": 0.25,
                "energy_efficiency": 0.20,
                "governance": 0.15
            }
            
            characteristic_weights = {}
            for char in weights.keys():
                weight_metrics = calcular_peso_caracteristica(char, weights, answers)
                characteristic_weights[char] = weight_metrics
            
            # Create weight visualization
            fig = go.Figure()
            
            for char, metrics in characteristic_weights.items():
                fig.add_trace(go.Bar(
                    name=char.capitalize(),
                    x=[char],
                    y=[metrics['peso_ajustado']],
                    text=[f"{metrics['peso_ajustado']:.2%}"],
                    textposition='auto',
                    hovertemplate=(
                        f"<b>{char.capitalize()}</b><br>" +
                        "Peso Ajustado: %{y:.2%}<br>" +
                        f"Impacto das Respostas: {metrics['impacto_respostas']:.2%}<br>" +
                        f"Confiança: {metrics['confianca']:.2%}"
                    )
                ))
            
            fig.update_layout(
                title="Pesos Ajustados das Características",
                yaxis_title="Peso Relativo",
                barmode='group',
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)

def run_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")

    st.warning("⚠️ Atenção: Reiniciar o processo irá apagar todas as respostas já fornecidas!")
    if st.button("🔄 Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

    st.markdown("---")
    
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
    
    progress_fig = create_progress_animation(current_phase, st.session_state.answers, questions)
    st.plotly_chart(progress_fig, use_container_width=True)
    
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
        st.session_state.recommendation = get_recommendation(st.session_state.answers, weights)
        
        if st.session_state.recommendation["confidence"]:
            show_metrics()
