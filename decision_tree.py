import streamlit as st
import plotly.graph_objects as go
import math
from decision_logic import get_recommendation, consensus_algorithms, consensus_groups, compare_algorithms
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def create_progress_animation(current_phase, answers, questions):
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
        
        # Add phase label with progress
        fig.add_annotation(
            x=i, y=-0.2,
            text=f"{phase}<br>({phase_progress[phase]}/{phase_total[phase]})",
            showarrow=False,
            font=dict(size=12)
        )
        
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
    
    # Update layout
    fig.update_layout(
        showlegend=False,
        height=200,
        margin=dict(l=20, r=20, t=20, b=40),
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
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação Final")
    
    # Main recommendation display with enhanced explanations
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("DLT Recomendada")
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3 style='color: #1f77b4;'>{recommendation.get('dlt', 'Não disponível')}</h3>
            <p><strong>Algoritmo de Consenso:</strong> {recommendation.get('consensus', 'Não disponível')}</p>
            <p><strong>Grupo de Consenso:</strong> {recommendation.get('consensus_group', 'Não disponível')}</p>
            <p><em>{recommendation.get('group_description', '')}</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add detailed characteristic scores section
        st.subheader("Scores por Característica")
        with st.expander("Ver Detalhamento dos Scores"):
            scores = recommendation.get('evaluation_matrix', {}).get(recommendation['dlt'], {}).get('metrics', {})
            weights = {
                "security": 0.4,
                "scalability": 0.25,
                "energy_efficiency": 0.20,
                "governance": 0.15
            }
            
            for metric, weight in weights.items():
                score = float(scores.get(metric, 0))
                weighted_score = score * weight
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        label=f"{metric.title()}",
                        value=f"{score:.2f}/5.0",
                        help=f"Score base para {metric}"
                    )
                with col2:
                    st.metric(
                        label="Peso",
                        value=f"{weight:.1%}",
                        help=f"Peso atribuído para {metric}"
                    )
                with col3:
                    st.metric(
                        label="Score Ponderado",
                        value=f"{weighted_score:.2f}",
                        help=f"Score final após aplicação do peso"
                    )
                
                # Add progress bar to visualize score
                st.progress(score/5.0, text=f"Score relativo: {score/5.0:.1%}")
                st.markdown("---")
            
            st.markdown('''
            ### Como interpretar os scores:
            
            - **Score Base**: Valor de 0 a 5 atribuído para cada característica
            - **Peso**: Importância relativa da característica no cálculo final
            - **Score Ponderado**: Score Base × Peso = Contribuição final
            
            #### Pesos das Características:
            - Segurança: 40% (Maior peso devido à criticidade dos dados de saúde)
            - Escalabilidade: 25% (Importante para crescimento do sistema)
            - Eficiência Energética: 20% (Impacto em custos operacionais)
            - Governança: 15% (Flexibilidade administrativa)
            ''')
        
        # Add DLT Evaluation Matrix
        st.subheader("Matriz de Avaliação de DLTs")
        with st.expander("Ver Matriz de Avaliação de DLTs"):
            evaluation_matrix = recommendation.get('evaluation_matrix', {})
            dlt_matrix_data = []
            dlt_labels = []
            metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
            
            for dlt, data in evaluation_matrix.items():
                dlt_labels.append(dlt)
                row = []
                for metric in metrics:
                    value = float(data['metrics'].get(metric, 0))
                    row.append(value)
                dlt_matrix_data.append(row)
            
            # Create heatmap
            fig_dlt = go.Figure(data=go.Heatmap(
                z=dlt_matrix_data,
                x=['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
                y=dlt_labels,
                colorscale='Viridis',
                hoverongaps=False,
                hovertemplate="<b>DLT:</b> %{y}<br>" +
                             "<b>Métrica:</b> %{x}<br>" +
                             "<b>Score:</b> %{z:.2f}<br>" +
                             "<extra></extra>"
            ))
            
            fig_dlt.update_layout(
                title="Matriz de Avaliação das DLTs",
                height=400
            )
            
            st.plotly_chart(fig_dlt, use_container_width=True)
            
            st.markdown('''
            ### Como interpretar a Matriz de DLTs:
            - **Cores mais escuras**: Indicam scores mais altos
            - **Cores mais claras**: Indicam scores mais baixos
            - **Métricas avaliadas**: Segurança, Escalabilidade, Eficiência Energética e Governança
            ''')
        
        # Add Algorithm Groups Matrix
        st.subheader("Matriz de Avaliação dos Grupos de Algoritmos")
        with st.expander("Ver Matriz de Avaliação dos Grupos de Algoritmos"):
            group_matrix_data = []
            group_labels = []
            
            for group, data in consensus_groups.items():
                group_labels.append(group)
                row = []
                for metric in metrics:
                    value = float(data['characteristics'].get(metric, 0))
                    row.append(value)
                group_matrix_data.append(row)
            
            # Create heatmap
            fig_groups = go.Figure(data=go.Heatmap(
                z=group_matrix_data,
                x=['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
                y=group_labels,
                colorscale='Viridis',
                hoverongaps=False,
                hovertemplate="<b>Grupo:</b> %{y}<br>" +
                             "<b>Métrica:</b> %{x}<br>" +
                             "<b>Score:</b> %{z:.2f}<br>" +
                             "<extra></extra>"
            ))
            
            fig_groups.update_layout(
                title="Matriz de Avaliação dos Grupos de Algoritmos",
                height=400
            )
            
            st.plotly_chart(fig_groups, use_container_width=True)
            
            st.markdown('''
            ### Como interpretar a Matriz de Grupos:
            - Cada linha representa um grupo de algoritmos
            - As colunas mostram o desempenho em diferentes métricas
            - Os valores são médias dos algoritmos no grupo
            ''')
        
        # Add Algorithms Matrix
        st.subheader("Matriz de Avaliação dos Algoritmos")
        with st.expander("Ver Matriz de Avaliação dos Algoritmos"):
            alg_matrix_data = []
            alg_labels = []
            
            recommended_group = recommendation['consensus_group']
            group_algorithms = consensus_groups[recommended_group]['algorithms']
            
            for alg in group_algorithms:
                if alg in consensus_algorithms:
                    alg_labels.append(alg)
                    row = []
                    for metric in metrics:
                        value = float(consensus_algorithms[alg].get(metric, 0))
                        row.append(value)
                    alg_matrix_data.append(row)
            
            # Create heatmap
            fig_alg = go.Figure(data=go.Heatmap(
                z=alg_matrix_data,
                x=['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
                y=alg_labels,
                colorscale='Viridis',
                hoverongaps=False,
                hovertemplate="<b>Algoritmo:</b> %{y}<br>" +
                             "<b>Métrica:</b> %{x}<br>" +
                             "<b>Score:</b> %{z:.2f}<br>" +
                             "<extra></extra>"
            ))
            
            fig_alg.update_layout(
                title=f"Matriz de Avaliação dos Algoritmos do Grupo {recommended_group}",
                height=400
            )
            
            st.plotly_chart(fig_alg, use_container_width=True)
            
            st.markdown('''
            ### Como interpretar a Matriz de Algoritmos:
            - Mostra apenas os algoritmos do grupo recomendado
            - Permite comparação direta entre algoritmos
            - Facilita a visualização dos pontos fortes de cada algoritmo
            ''')

    with col2:
        st.subheader("Métricas de Confiança")
        confidence_score = recommendation.get('confidence', False)
        confidence_value = recommendation.get('confidence_value', 0.0)
        st.metric(
            label="Índice de Confiança",
            value=f"{confidence_value:.2%}",
            delta=f"{'Alto' if confidence_score else 'Médio'}",
            delta_color="normal"
        )
        
        if recommendation.get('academic_validation'):
            with st.expander("Validação Acadêmica"):
                validation = recommendation['academic_validation']
                st.metric("Score Acadêmico", f"{validation['score']:.1f}/5.0")
                st.write(f"**Citações:** {validation['citations']}")
                st.write(f"**Referência:** {validation['reference']}")
                st.write(f"**Validação:** {validation['validation']}")

    return recommendation

def run_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")

    # Add restart button at the top with warning
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
    
    # Show progress animation
    progress_fig = create_progress_animation(current_phase, st.session_state.answers, questions)
    st.plotly_chart(progress_fig, use_container_width=True)
    
    # Show current phase details
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
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights, questions)

def restart_decision_tree():
    if st.button("Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()
