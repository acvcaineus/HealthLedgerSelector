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
            
        # Create tooltip text with enhanced explanations
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
        
        # Add phase label with progress and detailed explanation
        fig.add_annotation(
            x=i, y=-0.2,
            text=f"{phase}<br>({phase_progress[phase]}/{phase_total[phase]})",
            showarrow=False,
            font=dict(size=12)
        )
        
        # Add connecting lines with phase relationship indicators
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
    
    # Update layout with enhanced explanations
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

def create_metrics_radar_chart(metrics, weights):
    fig = go.Figure()
    
    # Add metrics trace with enhanced tooltips
    metric_names = list(metrics.keys())
    metric_values = [float(metrics[m]) for m in metric_names]
    
    fig.add_trace(go.Scatterpolar(
        r=metric_values,
        theta=metric_names,
        fill='toself',
        name='Métricas Atuais',
        hovertemplate="<b>%{theta}</b><br>" +
                     "Valor: %{r:.3f}<br>" +
                     "Peso: " + "<br>".join([f"{weights.get(m, 'N/A'):.2%}" for m in metric_names]) +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        title="Visão Geral das Métricas",
        showlegend=True
    )
    return fig

def show_metrics():
    st.header("Métricas Técnicas do Processo de Decisão")
    
    if 'recommendation' in st.session_state:
        rec = st.session_state.recommendation
        if 'evaluation_matrix' in rec:
            # Get the evaluation matrix data
            classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
            total = sum(classes.values())
            values = list(classes.values())
            
            # Calculate metrics
            gini = calcular_gini(classes)
            entropy = calcular_entropia(classes)
            
            # Show detailed calculations with enhanced explanations
            with st.expander("Detalhamento dos Cálculos"):
                st.write(f'''
                ### Índice de Gini
                Valor atual: {gini:.3f}
                Fórmula: 1 - Σ(pi²) = {1 - sum((v/total)**2 for v in values):.3f}
                
                ### Entropia
                Valor atual: {entropy:.3f} bits
                Fórmula: -Σ(pi * log2(pi)) = {-sum((v/total)*math.log2(v/total) for v in values if v != 0):.3f}
                
                ### Profundidade
                Valor atual: {len(st.session_state.answers):.2f}
                Total de nós: {len(st.session_state.answers) * 2 + 1}
                Nós podados: {(len(st.session_state.answers) * 2 + 1) - len(st.session_state.answers) - 1}
                
                ### Taxa de Poda
                Valor atual: {calcular_pruning(len(st.session_state.answers) * 2 + 1, 
                            (len(st.session_state.answers) * 2 + 1) - len(st.session_state.answers) - 1):.2%}
                Fórmula: (total_nós - nós_podados) / total_nós
                ''')
            
            # Show metric weights with detailed explanations
            st.subheader("Pesos das Métricas")
            weights = {
                "security": 0.4,
                "scalability": 0.25,
                "energy_efficiency": 0.20,
                "governance": 0.15
            }
            
            cols = st.columns(len(weights))
            for i, (metric, weight) in enumerate(weights.items()):
                with cols[i]:
                    st.metric(
                        label=f"Peso de {metric}",
                        value=f"{float(weight):.2%}",
                        help=f"Importância relativa da métrica {metric}"
                    )
            
            # Show confidence calculation with enhanced explanations
            if 'confidence_value' in rec:
                confidence_value = rec['confidence_value']
                scores = [float(v['score']) for v in rec['evaluation_matrix'].values()]
                max_score = max(scores)
                mean_score = sum(scores) / len(scores)
                
                with st.expander("Cálculo de Confiança"):
                    st.write(f'''
                    ### Cálculo de Confiança
                    - Score máximo: {max_score:.3f}
                    - Score médio: {mean_score:.3f}
                    - Confiança: {confidence_value:.2%}
                    - Threshold: 70%
                    ''')
            
            # Create and display radar chart with updated metrics
            metrics = {
                "Índice de Gini": gini,
                "Entropia": entropy / 4.0,  # Normalize to 0-1 range
                "Profundidade": len(st.session_state.answers) / 8.0,  # Normalize to 0-1 range
                "Taxa de Poda": calcular_pruning(
                    len(st.session_state.answers) * 2 + 1,
                    (len(st.session_state.answers) * 2 + 1) - len(st.session_state.answers) - 1
                )
            }
            
            fig_radar = create_metrics_radar_chart(metrics, weights)
            st.plotly_chart(fig_radar, use_container_width=True)

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
        
        # DLT Types comparison matrix with enhanced explanations
        st.subheader("Comparação de Tipos de DLT")
        eval_matrix = recommendation.get('evaluation_matrix', {})
        if eval_matrix:
            dlt_comparison_data = []
            dlts = list(eval_matrix.keys())
            metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
            
            for dlt in dlts:
                dlt_data = eval_matrix[dlt].get('metrics', {})
                values = [float(dlt_data.get(metric, 0)) for metric in metrics]
                dlt_comparison_data.append(go.Scatterpolar(
                    r=values,
                    theta=metrics,
                    name=dlt,
                    fill='toself'
                ))
            
            fig_dlt = go.Figure(data=dlt_comparison_data)
            fig_dlt.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=True,
                title="Comparação de Tipos de DLT"
            )
            st.plotly_chart(fig_dlt, use_container_width=True)
            
            with st.expander("Como interpretar a Comparação de Tipos de DLT?"):
                st.write('''
                ### Explicação do Gráfico Radar de DLTs
                - Cada eixo representa uma característica chave (Segurança, Escalabilidade, etc.)
                - Valores mais altos (mais distantes do centro) indicam melhor desempenho
                - A área preenchida mostra o perfil completo de cada DLT
                
                ### Por que estas métricas?
                - **Segurança**: Proteção dos dados e resistência a ataques
                - **Escalabilidade**: Capacidade de crescimento da rede
                - **Eficiência Energética**: Consumo de recursos
                - **Governança**: Facilidade de gestão e controle
                
                ### Score Final
                A DLT recomendada foi escolhida por ter o melhor equilíbrio entre estas características para seu caso.
                ''')
        
        # Consensus Algorithm Groups matrix with enhanced explanations
        st.subheader("Grupos de Algoritmos de Consenso")
        consensus_group = recommendation.get('consensus_group')
        if consensus_group in consensus_groups:
            group_data = consensus_groups[consensus_group]
            
            # Create matrix for consensus group characteristics
            characteristics = group_data.get('characteristics', {})
            fig_group = go.Figure(data=[
                go.Bar(
                    x=list(characteristics.keys()),
                    y=[float(v) for v in characteristics.values()],
                    text=[f"{float(v):.1f}" for v in characteristics.values()],
                    textposition='auto',
                )
            ])
            fig_group.update_layout(
                title=f"Características do Grupo: {consensus_group}",
                yaxis_range=[0, 5],
                showlegend=False
            )
            st.plotly_chart(fig_group, use_container_width=True)
            
            with st.expander("Como interpretar os Grupos de Algoritmos?"):
                st.write(f'''
                ### Explicação do Gráfico de Barras
                - Cada barra representa uma característica do grupo {consensus_group}
                - Altura das barras indica a força em cada aspecto
                - Valores mais altos (próximos a 5) são melhores
                
                ### Razão da Escolha
                Este grupo foi selecionado porque:
                - Alinhamento com suas respostas sobre {", ".join(group_data.get('characteristics', {}).keys())}
                - {group_data.get('description', 'Melhor adequação ao seu caso de uso')}
                ''')
        
        # Combined analytical matrix with enhanced explanations
        st.subheader("Matriz Analítica Combinada")
        if eval_matrix:
            # Prepare data for heatmap
            matrix_data = []
            y_labels = []
            metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
            
            for dlt, data in eval_matrix.items():
                y_labels.append(dlt)
                row = []
                for metric in metrics:
                    try:
                        row.append(float(data.get('metrics', {}).get(metric, 0)))
                    except (ValueError, TypeError):
                        row.append(0.0)
                matrix_data.append(row)
            
            fig_combined = go.Figure(data=go.Heatmap(
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
            
            fig_combined.update_layout(
                title="Análise Combinada de Métricas",
                xaxis_title="Métricas",
                yaxis_title="DLTs",
                height=400
            )
            st.plotly_chart(fig_combined, use_container_width=True)
            
            with st.expander("Como interpretar a Matriz Analítica Combinada?"):
                st.write('''
                ### Explicação do Mapa de Calor
                - Cores mais quentes (vermelho) indicam valores mais baixos
                - Cores mais frias (verde) indicam valores mais altos
                - Cada célula mostra o desempenho em uma métrica específica
                
                ### Como ler os resultados:
                - **Linhas**: Diferentes tipos de DLT
                - **Colunas**: Métricas avaliadas
                - **Cores**: Intensidade do desempenho
                
                ### Processo de Decisão
                A recomendação final considera:
                - Pontuação em cada métrica
                - Peso das características priorizadas
                - Adequação ao seu caso de uso
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
        
        # Add metrics explanation with enhanced details
        with st.expander("Como interpretar as métricas?"):
            st.write("""
            ### Índice de Confiança
            Indica a confiabilidade da recomendação baseada em:
            - Diferença entre scores
            - Consistência das respostas
            - Validação acadêmica
            
            **Alto** > 70% = Recomendação muito confiável
            **Médio** ≤ 70% = Recomendação aceitável
            """)
        
        # Academic validation section with enhanced details
        if recommendation.get('academic_validation'):
            with st.expander("Validação Acadêmica"):
                validation = recommendation['academic_validation']
                st.metric("Score Acadêmico", f"{validation['score']:.1f}/5.0")
                st.write(f"**Citações:** {validation['citations']}")
                st.write(f"**Referência:** {validation['reference']}")
                st.write(f"**Validação:** {validation['validation']}")
    
    # Show algorithm comparison with enhanced explanations
    st.subheader("Comparação de Algoritmos")
    comparison_data = compare_algorithms(recommendation['consensus_group'])
    
    if comparison_data:
        fig = go.Figure()
        
        algorithms = list(comparison_data["Segurança"].keys())
        metrics = list(comparison_data.keys())
        
        for alg in algorithms:
            values = [comparison_data[metric][alg] for metric in metrics]
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics,
                name=alg,
                fill='toself'
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=True,
            title="Comparação de Algoritmos de Consenso"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("Como interpretar a Comparação de Algoritmos?"):
            st.write('''
            ### Explicação do Gráfico Radar de Algoritmos
            - Cada algoritmo é representado por uma área colorida
            - Eixos mostram diferentes aspectos de desempenho
            - Maior área indica melhor desempenho geral
            
            ### Critérios de Avaliação:
            - **Segurança**: Resistência a ataques e falhas
            - **Escalabilidade**: Capacidade de processamento
            - **Eficiência**: Uso de recursos
            - **Governança**: Facilidade de gestão
            
            ### Escolha do Algoritmo
            O algoritmo recomendado apresenta o melhor equilíbrio entre:
            - Requisitos do seu projeto
            - Características da DLT escolhida
            - Pesos atribuídos a cada critério
            ''')
    
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

    st.markdown("---")  # Add a visual separator after the restart button
    
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
    
    # Show current phase details with enhanced explanations
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
