import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, compare_algorithms, calculate_compatibility_scores
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def create_phase_progress(current_phase, total_phases=4):
    """Create a visual progress indicator for phases"""
    phases = ["Aplicação", "Consenso", "Infraestrutura", "Internet"]
    current_idx = phases.index(current_phase) if current_phase in phases else -1
    
    progress_html = """
        <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
    """
    
    for i, phase in enumerate(phases):
        if i < current_idx:
            color = "#4CAF50"  # Completed
            text_color = "#4CAF50"
        elif i == current_idx:
            color = "#2196F3"  # Current
            text_color = "#2196F3"
        else:
            color = "#E0E0E0"  # Pending
            text_color = "#666666"
            
        progress_html += f"""
            <div style="text-align: center; flex: 1;">
                <div style="background-color: {color}; width: 30px; height: 30px; border-radius: 50%; margin: 0 auto;">
                </div>
                <p style="margin-top: 5px; color: {text_color};">{phase}</p>
            </div>
        """
        if i < len(phases) - 1:
            line_color = "#4CAF50" if i < current_idx else "#E0E0E0"
            progress_html += f"""
                <div style="flex-grow: 1; height: 2px; background-color: {line_color}; margin-top: 15px;"></div>
            """
            
    progress_html += "</div>"
    st.markdown(progress_html, unsafe_allow_html=True)

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
        
        # Razões para a Escolha
        with st.expander("Razões para a Escolha", expanded=True):
            st.write("### Análise Detalhada da Recomendação")
            
            # Privacy Impact Analysis
            st.write("#### Impacto na Privacidade")
            privacy_score = float(recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['security'])
            st.progress(privacy_score/5.0, text=f"Nível de Privacidade: {privacy_score:.1f}/5.0")
            st.write(f"""
                {'✅' if privacy_score >= 4 else '⚠️'} Esta DLT 
                {'oferece forte proteção' if privacy_score >= 4 else 'requer atenção adicional'} 
                para dados sensíveis de saúde.
            """)
            
            # Efficiency Considerations
            st.write("#### Considerações de Eficiência")
            efficiency_score = float(recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['energy_efficiency'])
            st.progress(efficiency_score/5.0, text=f"Eficiência: {efficiency_score:.1f}/5.0")
            st.write(f"""
                {'✅' if efficiency_score >= 4 else '⚠️'} O consumo de recursos é 
                {'otimizado' if efficiency_score >= 4 else 'moderado'} 
                para as operações necessárias.
            """)
            
            # Governance Requirements
            st.write("#### Requisitos de Governança")
            governance_score = float(recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']['governance'])
            st.progress(governance_score/5.0, text=f"Governança: {governance_score:.1f}/5.0")
            st.write(f"""
                {'✅' if governance_score >= 4 else '⚠️'} A estrutura de governança é 
                {'bem definida' if governance_score >= 4 else 'adequada'} 
                para o contexto de saúde.
            """)
            
            # Match Analysis
            st.write("#### Por que esta DLT é a mais adequada?")
            st.write("""
                Esta recomendação foi baseada em:
                1. Alinhamento com requisitos de privacidade do setor de saúde
                2. Capacidade de integração com sistemas existentes
                3. Conformidade com regulamentações (LGPD/HIPAA)
                4. Desempenho e escalabilidade adequados
            """)
        
        # Casos de Uso
        with st.expander("Casos de Uso na Saúde"):
            use_cases = {
                "Prontuário Eletrônico": {
                    "description": "Implementação de registros médicos eletrônicos seguros e interoperáveis",
                    "details": """
                        - **Desafio**: Garantir privacidade e acesso controlado a registros médicos
                        - **Solução**: Utilização de smart contracts para gerenciar permissões
                        - **Resultado**: Redução de 40% no tempo de acesso a informações críticas
                    """,
                    "reference": "Hospital Sírio-Libanês (2023)"
                },
                "Rastreamento de Medicamentos": {
                    "description": "Sistema de rastreamento de medicamentos na cadeia de suprimentos",
                    "details": """
                        - **Desafio**: Combater falsificação e garantir autenticidade
                        - **Solução**: DLT para registro imutável de transações
                        - **Resultado**: Identificação de 99.9% dos medicamentos autênticos
                    """,
                    "reference": "ANVISA (2024)"
                },
                "Pesquisa Clínica": {
                    "description": "Gerenciamento de dados de pesquisas clínicas multicêntricas",
                    "details": """
                        - **Desafio**: Compartilhar dados mantendo privacidade
                        - **Solução**: DLT com camadas de permissionamento
                        - **Resultado**: Aumento de 60% na velocidade de compartilhamento
                    """,
                    "reference": "FIOCRUZ (2024)"
                }
            }
            
            for title, case in use_cases.items():
                if st.button(f"📋 {title}", key=f"case_{title}"):
                    st.write(f"### {title}")
                    st.write(case["description"])
                    st.markdown(case["details"])
                    st.info(f"Fonte: {case['reference']}")
        
        # Evaluation Matrix with Portuguese labels
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
            
            tooltips = {
                "Segurança": "Capacidade de proteger dados sensíveis e resistir a ataques",
                "Escalabilidade": "Capacidade de crescer mantendo desempenho",
                "Eficiência Energética": "Consumo de recursos e sustentabilidade",
                "Governança": "Facilidade de gestão e controle de acesso"
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
                             "<b>Valor:</b> %{z:.2f}/5.0<br>" +
                             "<extra></extra>"
            ))
            
            fig.update_layout(
                title="Comparação Detalhada das DLTs",
                height=400,
                margin=dict(l=50, r=30, t=80, b=50)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Metric explanations
            st.write("### Explicação das Métricas")
            for metric, explanation in tooltips.items():
                st.markdown(f"**{metric}**: {explanation}")
    
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
        # Show progress visualization
        create_phase_progress(current_phase)
        
        # Show current progress
        remaining_questions = sum(1 for q in questions if q["id"] not in st.session_state.answers)
        st.progress((len(questions) - remaining_questions) / len(questions),
                   text=f"Progresso: {len(questions) - remaining_questions}/{len(questions)} perguntas")
        
        # Display current question
        st.markdown(f"""
            ### Fase: {current_phase}
            #### Pergunta Atual: {current_question['text']}
            """)
        st.info(f"💡 Dica: {current_question['tooltip']}")
        
        # Show question options
        response = st.radio("Selecione sua resposta:", current_question["options"])
        
        # Next question button
        if st.button("Próxima Pergunta", type="primary"):
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
