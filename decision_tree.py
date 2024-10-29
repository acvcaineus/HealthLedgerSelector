import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms, consensus_groups
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
    
    # Main recommendation display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("DLT Recomendada")
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3 style='color: #1f77b4;'>{recommendation.get('dlt', 'Não disponível')}</h3>
            <p><strong>Algoritmo de Consenso:</strong> {recommendation.get('consensus', 'Não disponível')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced algorithm group explanation
        with st.expander("Ver Detalhes do Grupo de Algoritmos"):
            st.write("### Grupo de Algoritmos")
            group_descriptions = {
                'Alta Segurança e Controle': """
                Este grupo é focado em algoritmos que priorizam a segurança e controle rigoroso sobre as transações.
                
                **Características principais:**
                - Alta resistência a ataques bizantinos
                - Controle preciso sobre os validadores
                - Ideal para dados sensíveis de saúde
                
                **Algoritmos típicos:**
                - PBFT (Practical Byzantine Fault Tolerance)
                - Proof of Work (PoW) com restrições
                """,
                'Alta Eficiência Operacional': """
                Grupo otimizado para eficiência e velocidade em redes menores e controladas.
                
                **Características principais:**
                - Baixa latência nas transações
                - Consumo energético otimizado
                - Ideal para redes hospitalares locais
                
                **Algoritmos típicos:**
                - Raft Consensus
                - Proof of Authority (PoA)
                """,
                'Escalabilidade e Governança Flexível': """
                Foco em balancear escalabilidade com flexibilidade na governança.
                
                **Características principais:**
                - Alta capacidade de processamento
                - Governança adaptável
                - Ideal para redes regionais de saúde
                
                **Algoritmos típicos:**
                - Proof of Stake (PoS)
                - Delegated Proof of Stake (DPoS)
                """,
                'Alta Escalabilidade em Redes IoT': """
                Especializado em lidar com grande volume de dispositivos IoT.
                
                **Características principais:**
                - Processamento paralelo eficiente
                - Baixo consumo por transação
                - Ideal para monitoramento em tempo real
                
                **Algoritmos típicos:**
                - Tangle (IOTA)
                - DAG-based consensus
                """,
                'Alta Segurança e Descentralização de Dados Críticos': """
                Máxima segurança e descentralização para dados críticos.
                
                **Características principais:**
                - Descentralização completa
                - Imutabilidade garantida
                - Ideal para registros médicos permanentes
                
                **Algoritmos típicos:**
                - Proof of Work (PoW)
                - Advanced Proof of Stake (PoS)
                """
            }
            
            # Display group description based on recommended DLT
            dlt_to_group = {
                "DLT Permissionada Privada": "Alta Segurança e Controle",
                "DLT Permissionada Simples": "Alta Eficiência Operacional",
                "DLT Híbrida": "Escalabilidade e Governança Flexível",
                "DLT Pública": "Alta Escalabilidade em Redes IoT",
                "DLT com Consenso Delegado": "Escalabilidade e Governança Flexível",
                "DLT Pública Permissionless": "Alta Segurança e Descentralização de Dados Críticos"
            }
            
            recommended_group = dlt_to_group.get(recommendation.get('dlt', ''), "Alta Segurança e Controle")
            st.markdown(group_descriptions.get(recommended_group, "Descrição não disponível"))
        
        # Enhanced consensus algorithm explanation
        with st.expander("Ver Detalhes do Algoritmo de Consenso"):
            consensus = recommendation.get('consensus', '')
            st.write(f"### {consensus}")
            
            consensus_details = {
                "Proof of Stake (PoS)": {
                    "description": """
                    O Proof of Stake (PoS) é um mecanismo de consenso que seleciona validadores com base em sua participação no sistema.
                    
                    **Como funciona:**
                    - Validadores depositam tokens como garantia
                    - Chance de validação proporcional ao stake
                    - Penalidades por comportamento malicioso
                    
                    **Vantagens para Saúde:**
                    - Baixo consumo energético
                    - Alta escalabilidade
                    - Segurança proporcional ao valor em stake
                    
                    **Aplicações Ideais:**
                    - Redes de hospitais
                    - Sistemas de prontuários eletrônicos
                    - Compartilhamento seguro de dados
                    """,
                    "metrics": consensus_algorithms.get("Proof of Stake (PoS)", {})
                },
                "Proof of Work (PoW)": {
                    "description": """
                    O Proof of Work (PoW) é um mecanismo que requer poder computacional para validar transações.
                    
                    **Como funciona:**
                    - Resolução de puzzles criptográficos
                    - Competição entre mineradores
                    - Alta segurança através de trabalho computacional
                    
                    **Vantagens para Saúde:**
                    - Máxima segurança
                    - Imutabilidade garantida
                    - Descentralização completa
                    
                    **Aplicações Ideais:**
                    - Registros permanentes
                    - Auditorias de longo prazo
                    - Dados críticos de pesquisa
                    """,
                    "metrics": consensus_algorithms.get("Proof of Work (PoW)", {})
                },
                "Practical Byzantine Fault Tolerance (PBFT)": {
                    "description": """
                    PBFT é um protocolo de consenso que oferece alta segurança em redes permissionadas.
                    
                    **Como funciona:**
                    - Votação em múltiplas rodadas
                    - Tolerância a nós maliciosos
                    - Consenso rápido e definitivo
                    
                    **Vantagens para Saúde:**
                    - Alta performance
                    - Finalidade imediata
                    - Controle de acesso
                    
                    **Aplicações Ideais:**
                    - Redes hospitalares privadas
                    - Sistemas de autorização
                    - Registros médicos sensíveis
                    """,
                    "metrics": consensus_algorithms.get("Practical Byzantine Fault Tolerance (PBFT)", {})
                }
            }
            
            if consensus in consensus_details:
                st.markdown(consensus_details[consensus]["description"])
                
                # Show metrics in a more visual way
                metrics = consensus_details[consensus]["metrics"]
                if metrics:
                    st.write("### Métricas do Algoritmo")
                    cols = st.columns(len(metrics))
                    for i, (metric, value) in enumerate(metrics.items()):
                        with cols[i]:
                            st.metric(
                                label=metric.replace('_', ' ').title(),
                                value=f"{float(value):.1f}/5.0",
                                delta=f"{'Excelente' if float(value) >= 4.5 else 'Bom' if float(value) >= 3.5 else 'Regular'}"
                            )
            else:
                st.warning("Detalhes específicos não disponíveis para este algoritmo de consenso.")

    with col2:
        st.subheader("Métricas")
        confidence_score = recommendation.get('confidence', False)
        confidence_value = recommendation.get('confidence_value', 0.0)
        st.metric(
            label="Índice de Confiança",
            value=f"{confidence_value:.2%}",
            delta=f"{'Alto' if confidence_score else 'Médio'}",
            help="Baseado na diferença entre o score máximo e a média dos scores"
        )
        
    # Add confidence index explanation
    with st.expander("Ver Explicação do Índice de Confiança"):
        st.write("### Como o Índice de Confiança é Calculado")
        st.write("""O índice de confiança é calculado usando os seguintes parâmetros:
        1. **Diferença entre Scores**: A diferença entre o score mais alto e a média dos scores
        2. **Consistência das Respostas**: Avaliação da coerência entre as respostas fornecidas
        3. **Threshold de Confiança**: 0.7 (70%) - valor mínimo para alta confiança
        
        Fórmula: `Confiabilidade = (max_score - mean_score) / max_score`
        """)
        
        value = recommendation.get('confidence_value', 0.0)
        st.metric(
            "Valor do Índice de Confiança",
            f"{value:.2%}",
            help="Valores acima de 70% indicam alta confiabilidade"
        )
    
    # Enhanced evaluation matrix display
    st.subheader("Matriz de Avaliação Detalhada")
    eval_matrix = recommendation.get('evaluation_matrix', {})
    if eval_matrix:
        matrix_data = []
        y_labels = []
        
        for dlt, data in eval_matrix.items():
            y_labels.append(dlt)
            row = []
            for metric, value in data.get('metrics', {}).items():
                if metric != 'academic_validation':
                    try:
                        row.append(float(value))
                    except (ValueError, TypeError):
                        row.append(0.0)
            matrix_data.append(row)
        
        if y_labels:
            metrics = [m for m in eval_matrix[y_labels[0]].get('metrics', {}).keys() 
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
    
    # Save recommendation option
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
