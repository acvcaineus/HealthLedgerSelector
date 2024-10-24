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

    # Phase explanations
    st.markdown("### Fases do Processo de Decisão")
    phases = {
        "Aplicação": ["privacy", "integration"],
        "Consenso": ["network_security", "scalability"],
        "Infraestrutura": ["data_volume", "energy_efficiency"],
        "Internet": ["governance_flexibility", "interoperability"]
    }
    
    for phase, questions in phases.items():
        with st.expander(f"📋 Fase: {phase}"):
            answered = sum(1 for q in questions if q in answers)
            total = len(questions)
            st.progress(answered / total)
            st.markdown(f"**Progresso:** {answered}/{total} perguntas respondidas")
            for q in questions:
                if q in answers:
                    st.markdown(f"✓ {q}: **{answers[q]}**")
    
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
    
    with col2:
        st.subheader("Métricas de Confiança")
        confidence_score = recommendation.get('confidence', False)
        st.metric(
            label="Índice de Confiança",
            value=f"{'Alto' if confidence_score else 'Médio'}",
            delta=f"{'↑' if confidence_score else '→'}",
            help="Baseado na diferença entre o score máximo e a média dos scores"
        )
    
    # Confidence metrics explanation
    with st.expander("🔍 Explicação das Métricas de Confiança"):
        st.markdown('''
            ### Como calculamos a confiança?
            - **Índice de Gini**: Mede a pureza da classificação
            - **Entropia**: Mede a incerteza na decisão
            - **Confiabilidade**: Baseada na diferença entre scores
            
            [Ver página de métricas completa](Métricas)
        ''')
    
    # Detailed calculations
    with st.expander("📊 Detalhes dos Cálculos"):
        st.markdown("### Cálculos Realizados")
        st.latex(r"Gini = 1 - \sum_{i=1}^{n} p_i^2")
        st.markdown("### Parâmetros Utilizados")
        classes = {k: v['score'] for k, v in recommendation['evaluation_matrix'].items()}
        for dlt, score in classes.items():
            st.write(f"- {dlt}: {score:.3f}")
    
    # Decision Tree Metrics in collapsible sections
    with st.expander("📈 Métricas da Árvore de Decisão"):
        col1, col2 = st.columns(2)
        
        with col1:
            gini = calcular_gini(classes)
            st.metric(
                label="Índice de Gini",
                value=f"{gini:.3f}",
                help="Medida de pureza da classificação (menor é melhor)"
            )
            st.markdown("""
                **Interpretação do Índice de Gini:**
                - 0.0 - 0.3: Excelente separação
                - 0.3 - 0.6: Boa separação
                - > 0.6: Separação moderada
            """)
        
        with col2:
            entropy = calcular_entropia(classes)
            st.metric(
                label="Entropia",
                value=f"{entropy:.3f}",
                help="Medida de incerteza na decisão (menor é melhor)"
            )
            st.markdown("""
                **Interpretação da Entropia:**
                - 0.0 - 1.0: Baixa incerteza
                - 1.0 - 2.0: Incerteza moderada
                - > 2.0: Alta incerteza
            """)

    # Evaluation matrix with explanations
    with st.expander("📊 Matriz de Avaliação"):
        st.markdown("""
        ### Interpretação das Métricas
        - **Segurança**: Proteção dos dados e resistência a ataques
        - **Escalabilidade**: Capacidade de crescimento
        - **Eficiência**: Consumo de recursos
        - **Governança**: Controle e gestão da rede
        """)
        
        matrix_data = []
        y_labels = []
        
        for dlt, data in recommendation['evaluation_matrix'].items():
            y_labels.append(dlt)
            row = []
            for metric, value in data['metrics'].items():
                if metric != "academic_validation":
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
    
    # Questions with phases
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
    
    # Phase progress visualization
    phase_colors = {
        "Aplicação": "#2ecc71",
        "Consenso": "#3498db",
        "Infraestrutura": "#e74c3c",
        "Internet": "#f1c40f"
    }
    
    st.markdown(f"""
        <div style='background-color: {phase_colors.get(current_phase, "#95a5a6")}; 
             padding: 10px; border-radius: 5px; color: white;'>
            <h3>Fase Atual: {current_phase}</h3>
            <p>Progresso: {int(progress * 100)}%</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.progress(progress)

    # Show phase explanation
    with st.expander(f"ℹ️ Sobre a fase: {current_phase}"):
        phase_explanations = {
            "Aplicação": "Esta fase avalia os requisitos básicos da aplicação em termos de privacidade e integração.",
            "Consenso": "Analisa as necessidades de segurança e escalabilidade da rede.",
            "Infraestrutura": "Avalia requisitos técnicos como volume de dados e eficiência.",
            "Internet": "Considera aspectos de governança e interoperabilidade."
        }
        st.markdown(phase_explanations.get(current_phase, "Todas as fases completadas."))

    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    if current_question:
        with st.expander("💡 Detalhes da Característica", expanded=True):
            st.subheader(f"Avaliando: {current_question['characteristic']}")
            st.markdown(f"**Fase:** {current_question['phase']}")
            st.markdown(f"**Descrição:** {current_question['tooltip']}")
        
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
