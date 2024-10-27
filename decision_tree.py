import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from decision_logic import get_recommendation, compare_algorithms, consensus_algorithms, reference_data
from database import save_recommendation
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def show_recommendation(answers, weights, questions):
    recommendation = get_recommendation(answers, weights)
    
    with st.spinner('Carregando recomendação...'):
        st.header("Recomendação Final")
        
        # Main recommendation display with improved styling
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
            
            # Enhanced explanations with improved styling
            with st.expander("🔍 Ver Explicação Detalhada da DLT"):
                st.write(f"### Por que {recommendation['dlt']}?")
                st.write("Esta DLT foi selecionada com base em suas respostas:")
                for question_id, answer in answers.items():
                    for q in questions:
                        if q['id'] == question_id:
                            st.markdown(f"- {q['text']}: **{answer}**")
                st.write("\n### Características Principais:")
                st.markdown(recommendation['characteristics'])
                st.write("\n### Casos de Uso:")
                st.markdown(recommendation['use_cases'])
            
            # Enhanced metrics visualization
            with st.expander("📊 Ver Métricas Detalhadas"):
                metrics_df = pd.DataFrame({
                    'Métrica': ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
                    'Valor': [
                        recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['security'],
                        recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['scalability'],
                        recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['energy_efficiency'],
                        recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['governance']
                    ]
                })
                
                # Create radar chart for metrics
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=metrics_df['Valor'],
                    theta=metrics_df['Métrica'],
                    fill='toself',
                    name='Métricas da DLT'
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 5]
                        )
                    ),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Enhanced confidence display
            st.subheader("Índices de Confiança")
            confidence_value = recommendation.get('confidence_value', 0.0)
            st.metric(
                label="Confiança da Recomendação",
                value=f"{confidence_value:.2%}",
                delta=f"{'Alta' if confidence_value > 0.7 else 'Média'}",
                help="Baseado na análise das respostas e métricas"
            )
            
            # Academic validation metrics
            if 'academic_validation' in recommendation:
                st.metric(
                    label="Validação Acadêmica",
                    value=f"{recommendation['academic_validation'].get('score', 0):.1f}/5.0",
                    help="Baseado em citações e implementações reais"
                )
    
    # Enhanced evaluation matrix display
    st.subheader("Matriz de Avaliação Comparativa")
    with st.spinner('Gerando matriz de avaliação...'):
        if 'evaluation_matrix' in recommendation:
            matrix_data = []
            y_labels = []
            
            for dlt, data in recommendation['evaluation_matrix'].items():
                y_labels.append(dlt)
                row = []
                for metric, value in data['metrics'].items():
                    if metric != 'academic_validation':
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
    
    # Save recommendation button with improved visibility
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Salvar Recomendação", key="save_recommendation", type="primary"):
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

    st.markdown("""
        ### Fases do Processo de Seleção
        O processo está dividido em 4 fases principais:
        1. **Aplicação**: Avaliação de requisitos de privacidade e integração
        2. **Consenso**: Análise de segurança e eficiência
        3. **Infraestrutura**: Avaliação de escalabilidade e performance
        4. **Internet**: Considerações sobre governança e interoperabilidade
    """)

    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    progress = len(st.session_state.answers) / len(questions)
    
    # Show progress bar with improved styling
    st.progress(progress, text=f"Progresso: {int(progress * 100)}%")
    st.markdown(f"### Fase Atual: {current_phase}")

    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    if current_question:
        with st.expander(f"ℹ️ {current_question['characteristic']}", expanded=True):
            st.info(f"💡 Dica: {current_question['tooltip']}")
            response = st.radio(
                current_question["text"],
                current_question["options"],
                key=f"question_{current_question['id']}"
            )

            if st.button("Próxima Pergunta", type="primary"):
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
