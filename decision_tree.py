import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)
from dlt_data import questions

def create_progress_animation(current_phase, answers):
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    fig = go.Figure()
    
    # Calculate progress for each phase
    phase_progress = {phase: 0 for phase in phases}
    phase_total = {phase: 0 for phase in phases}
    
    # Collect phase information from questions
    for q in questions:
        phase = [char for char in q.get('characteristics', []) if char in phases][0] if q.get('characteristics') else None
        if phase:
            phase_total[phase] += 1
            if q['id'] in answers:
                phase_progress[phase] += 1
    
    # Add animated nodes with progress indicators
    for i, phase in enumerate(phases):
        # Set color and size based on phase status
        if phase == current_phase:
            color = '#3498db'  # Blue for current
            size = 45
        elif phase_progress[phase] > 0:
            color = '#2ecc71'  # Green for completed
            size = 40
        else:
            color = '#bdc3c7'  # Gray for pending
            size = 35
        
        # Create tooltip text
        tooltip = f"<b>{phase}</b><br>"
        tooltip += f"Progresso: {phase_progress[phase]}/{phase_total[phase]}"
        
        fig.add_trace(go.Scatter(
            x=[i], y=[0],
            mode='markers',
            marker=dict(size=size, color=color),
            hovertext=tooltip,
            hoverinfo='text',
            showlegend=False
        ))
        
        # Add connecting lines between phases
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
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig

def create_metrics_explanation():
    """Cria explicações detalhadas para cada métrica em português."""
    return {
        "security": {
            "title": "Segurança",
            "description": "Mede o nível de proteção dos dados e resistência a ataques",
            "calculation": "Baseado em características como criptografia, imutabilidade e consenso",
            "healthcare_context": "Crucial para proteger dados sensíveis de pacientes e registros médicos"
        },
        "scalability": {
            "title": "Escalabilidade",
            "description": "Capacidade de crescer mantendo o desempenho",
            "calculation": "Avaliada por transações por segundo e tempo de confirmação",
            "healthcare_context": "Importante para sistemas com grande volume de registros médicos"
        },
        "energy_efficiency": {
            "title": "Eficiência Energética",
            "description": "Consumo de energia por transação",
            "calculation": "Medido em kWh por transação",
            "healthcare_context": "Relevante para sustentabilidade operacional de sistemas de saúde"
        },
        "governance": {
            "title": "Governança",
            "description": "Controle e gerenciamento da rede",
            "calculation": "Baseado em mecanismos de consenso e participação",
            "healthcare_context": "Essencial para conformidade com regulamentações de saúde"
        }
    }

def show_recommendation(answers, weights):
    recommendation = get_recommendation(answers, weights)
    metrics_explanation = create_metrics_explanation()
    
    st.header("Recomendação Final")
    
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
        
        with st.expander("📊 Como as Métricas são Calculadas"):
            st.write("### Sistema de Pontuação")
            st.markdown("""
            Cada métrica é avaliada em uma escala de 0 a 5, onde:
            - 0-1: Baixo desempenho
            - 2-3: Desempenho moderado
            - 4-5: Alto desempenho
            """)
            
            for metric, explanation in metrics_explanation.items():
                st.write(f"### {explanation['title']}")
                st.write(f"**Descrição:** {explanation['description']}")
                st.write(f"**Cálculo:** {explanation['calculation']}")
                st.write(f"**Contexto na Saúde:** {explanation['healthcare_context']}")
                st.write("---")

        with st.expander("🎯 Índice de Confiança"):
            st.write("### Como o Índice de Confiança é Calculado")
            st.markdown("""
            O índice de confiança é calculado através de uma fórmula que considera:
            
            1. **Diferença de Scores:**
               - Score máximo vs. média dos scores
               - Maior diferença = maior confiança
            
            2. **Pesos das Características:**
               - Segurança: 40%
               - Escalabilidade: 25%
               - Eficiência Energética: 20%
               - Governança: 15%
            
            3. **Validação Acadêmica:**
               - Pontuação adicional baseada em estudos científicos
               - Citações e implementações reais
            
            **Fórmula:**
            ```
            Confiança = (max_score - média_scores) / max_score
            ```
            
            **Interpretação:**
            - > 0.7: Alta confiança
            - 0.5-0.7: Confiança moderada
            - < 0.5: Baixa confiança
            """)

    with col2:
        st.subheader("Métricas")
        confidence_score = recommendation.get('confidence', False)
        confidence_value = recommendation.get('confidence_value', 0.0)
        
        st.info("""
        **Índice de Confiança**
        
        Este valor indica o quão confiável é a recomendação baseado na diferença entre
        a melhor opção e as alternativas. Quanto maior o valor, mais clara é a escolha.
        """)
        
        st.metric(
            label="Índice de Confiança",
            value=f"{confidence_value:.2%}",
            delta=f"{'Alto' if confidence_score else 'Médio'}",
            help="Baseado na diferença entre o score máximo e a média dos scores"
        )

    # Save recommendation option
    if st.button("💾 Salvar Recomendação"):
        if st.session_state.get('username'):
            save_recommendation(
                st.session_state.username,
                'Healthcare DLT Selection',
                recommendation
            )
            st.success("✅ Recomendação salva com sucesso!")
        else:
            st.warning("⚠️ Faça login para salvar a recomendação.")
    
    return recommendation

def run_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    st.title("Framework de Seleção de DLT")
    
    # Define weights for characteristics
    weights = {
        "security": float(0.4),
        "scalability": float(0.25),
        "energy_efficiency": float(0.20),
        "governance": float(0.15)
    }
    
    # Calculate current phase
    current_phase = 'Aplicação'
    if len(st.session_state.answers) >= 2:
        current_phase = 'Consenso'
    if len(st.session_state.answers) >= 4:
        current_phase = 'Infraestrutura'
    if len(st.session_state.answers) >= 6:
        current_phase = 'Internet'
    if len(st.session_state.answers) >= 8:
        current_phase = 'Completo'
    
    # Show progress animation
    progress_fig = create_progress_animation(current_phase, st.session_state.answers)
    st.plotly_chart(progress_fig, use_container_width=True)
    
    # Show progress bar
    progress = len(st.session_state.answers) / len(questions)
    st.progress(progress)
    
    # Display current question or recommendation
    if len(st.session_state.answers) < len(questions):
        current_question = questions[len(st.session_state.answers)]
        
        st.subheader(f"Fase: {current_phase}")
        st.info(f"Características relevantes: {', '.join(current_question['characteristics'])}")
        
        response = st.radio(
            current_question["text"],
            current_question["options"]
        )
        
        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question["id"]] = response
            st.experimental_rerun()
    else:
        show_recommendation(st.session_state.answers, weights)
        
        if st.button("Reiniciar", help="Começar um novo processo de seleção"):
            st.session_state.answers = {}
            st.experimental_rerun()
