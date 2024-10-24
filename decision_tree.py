import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
import networkx as nx
import plotly.figure_factory as ff
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao, get_metric_explanation)

def show_recommendation(answers, weights):
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação Final")
    
    # Enhanced recommendation display with academic validation
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("DLT Recomendada")
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3 style='color: #1f77b4;'>{recommendation['dlt']}</h3>
            <p><strong>Grupo de Consenso:</strong> {recommendation['consensus_group']}</p>
            <p><strong>Algoritmo:</strong> {recommendation['consensus']}</p>
            <div style='margin-top: 10px; padding: 10px; background-color: #e8f4f8; border-radius: 5px;'>
                <p><strong>Validação Acadêmica:</strong></p>
                <ul>
                    <li>Score: {recommendation['academic_validation'].get('score', 'N/A')}/5.0</li>
                    <li>Citações: {recommendation['academic_validation'].get('citations', 'N/A')}</li>
                    <li>Referência: {recommendation['academic_validation'].get('reference', 'N/A')}</li>
                </ul>
            </div>
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
        
        # Add validation metrics
        if 'academic_validation' in recommendation:
            validation_score = recommendation['academic_validation'].get('score', 0)
            st.metric(
                label="Validação Acadêmica",
                value=f"{validation_score:.1f}/5.0",
                delta=f"{'↑' if validation_score > 4.0 else '→' if validation_score > 3.0 else '↓'}",
                help="Score baseado em publicações acadêmicas e implementações práticas"
            )

    # Enhanced evaluation matrix with detailed explanations
    st.subheader("Matriz de Avaliação Detalhada")
    if 'evaluation_matrix' in recommendation:
        # Add metric explanations
        st.markdown("""
        ### Interpretação das Métricas
        
        #### 1. Segurança
        - **Alta (4-5):** Forte proteção contra ataques e garantia de privacidade
        - **Média (2-3):** Proteção adequada para casos gerais
        - **Baixa (0-1):** Requer medidas adicionais de segurança
        
        #### 2. Escalabilidade
        - **Alta (4-5):** Suporta grande volume de transações
        - **Média (2-3):** Adequada para volume moderado
        - **Baixa (0-1):** Limitações em alta demanda
        
        #### 3. Eficiência Energética
        - **Alta (4-5):** Baixo consumo de energia
        - **Média (2-3):** Consumo moderado
        - **Baixa (0-1):** Alto consumo energético
        
        #### 4. Governança
        - **Alta (4-5):** Controle e flexibilidade elevados
        - **Média (2-3):** Controle moderado
        - **Baixa (0-1):** Controle limitado
        """)
        
        matrix_data = []
        y_labels = []
        
        # Color scale explanation with icons
        st.markdown("""
        **Escala de Cores:**
        - 🔴 Vermelho (0-2): Baixo desempenho
        - 🟡 Amarelo (2-3.5): Desempenho médio
        - 🟢 Verde (3.5-5): Alto desempenho
        """)
        
        # Prepare matrix data
        for dlt, data in recommendation['evaluation_matrix'].items():
            y_labels.append(dlt)
            row = []
            for metric, value in data['metrics'].items():
                try:
                    row.append(float(value))
                except (ValueError, TypeError):
                    row.append(0.0)
            matrix_data.append(row)
            
        # Create enhanced heatmap
        fig = go.Figure(data=go.Heatmap(
            z=matrix_data,
            x=list(recommendation['evaluation_matrix'][y_labels[0]]['metrics'].keys()),
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
            title={
                'text': "Matriz de Avaliação das DLTs",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Métricas",
            yaxis_title="DLTs",
            height=400,
            margin=dict(l=60, r=30, t=100, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add comparative analysis
        st.subheader("Análise Comparativa")
        st.markdown("""
        Esta análise mostra como a DLT recomendada se compara com alternativas em aspectos chave:
        
        1. **Adequação ao Caso de Uso**
           - Avaliação da compatibilidade com requisitos específicos
           - Análise de implementações similares
        
        2. **Performance Técnica**
           - Métricas de desempenho e escalabilidade
           - Eficiência energética e custos operacionais
        
        3. **Maturidade da Tecnologia**
           - Tempo de existência e estabilidade
           - Tamanho e atividade da comunidade
        """)
        
        # Save recommendation to database
        if st.session_state.get('username'):
            save_recommendation(
                st.session_state.username,
                'Healthcare DLT Selection',
                recommendation
            )

    return recommendation

def show_initial_table():
    st.subheader("Tabela de DLTs e Características")
    dlt_data = {
        'DLT': ['Hyperledger Fabric', 'VeChain', 'Quorum (Mediledger)', 'IOTA', 'Ripple (XRP Ledger)', 'Stellar', 'Bitcoin', 'Ethereum (PoW)', 'Ethereum 2.0 (PoS)'],
        'Grupo de Algoritmo': ['Alta Segurança e Controle', 'Alta Eficiência Operacional', 'Escalabilidade e Governança', 'Alta Escalabilidade IoT', 'Alta Eficiência', 'Alta Eficiência', 'Alta Segurança', 'Alta Segurança', 'Escalabilidade'],
        'Algoritmo de Consenso': ['RAFT/IBFT', 'Proof of Authority (PoA)', 'RAFT/IBFT', 'Tangle', 'RCA', 'SCP', 'PoW', 'PoW', 'PoS'],
        'Caso de Uso': ['Rastreabilidade médica', 'Rastreamento de suprimentos', 'Monitoramento', 'IoT em saúde', 'Transações', 'Pagamentos', 'Dados críticos', 'Contratos inteligentes', 'Ensaios clínicos']
    }
    st.table(dlt_data)

def show_interactive_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")
    show_initial_table()
    
    questions = [
        {
            "id": "privacy",
            "phase": "Aplicação",
            "characteristic": "Privacidade",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere requisitos de LGPD e HIPAA para proteção de dados sensíveis",
            "impact": ["Proteção de dados", "Conformidade regulatória"]
        },
        {
            "id": "consensus",
            "phase": "Consenso",
            "characteristic": "Descentralização",
            "text": "É necessário alto grau de descentralização?",
            "options": ["Sim", "Não"],
            "tooltip": "Avalie a necessidade de descentralização do processo decisório",
            "impact": ["Distribuição de poder", "Autonomia da rede"]
        },
        {
            "id": "infrastructure",
            "phase": "Infraestrutura",
            "characteristic": "Escalabilidade",
            "text": "A infraestrutura precisa ser altamente escalável?",
            "options": ["Sim", "Não"],
            "tooltip": "Considere o volume de transações e capacidade de crescimento",
            "impact": ["Performance", "Capacidade"]
        },
        {
            "id": "internet",
            "phase": "Internet",
            "characteristic": "Conectividade",
            "text": "É necessária conexão permanente com a internet?",
            "options": ["Sim", "Não"],
            "tooltip": "Avalie a necessidade de conectividade constante",
            "impact": ["Disponibilidade", "Acessibilidade"]
        }
    ]

    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    progress = len(st.session_state.answers) / len(questions)
    
    phase_colors = {
        "Aplicação": "#2ecc71",
        "Consenso": "#3498db",
        "Infraestrutura": "#e74c3c",
        "Internet": "#f1c40f",
        "Completo": "#9b59b6"
    }
    
    st.markdown(f"""
    <div style='background-color: {phase_colors.get(current_phase, "#95a5a6")}; padding: 10px; border-radius: 5px; color: white;'>
        Fase Atual: {current_phase} - Progresso: {int(progress * 100)}%
    </div>
    """, unsafe_allow_html=True)

    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    if current_question:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Fase: {current_question['phase']}")
            st.markdown(f"**Característica: {current_question['characteristic']}**")
            response = st.radio(
                current_question["text"], 
                current_question["options"],
                help=current_question["tooltip"]
            )
            st.info(current_question["tooltip"])
        
        with col2:
            st.markdown("### Impacto da Decisão")
            for impact in current_question["impact"]:
                st.write(f"- {impact}")

        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question["id"]] = response
            st.experimental_rerun()

    if st.session_state.answers:
        st.subheader("Visualização do Fluxo de Decisão")
        show_decision_flow(st.session_state.answers, questions)

    if len(st.session_state.answers) == len(questions):
        weights = {
            "security": float(0.4),
            "scalability": float(0.25),
            "energy_efficiency": float(0.20),
            "governance": float(0.15)
        }
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights)

def show_decision_flow(answers, questions):
    G = nx.DiGraph()
    
    # Color coding for phases
    phase_colors = {
        "Aplicação": "#2ecc71",
        "Consenso": "#3498db",
        "Infraestrutura": "#e74c3c",
        "Internet": "#f1c40f"
    }
    
    node_attrs = {
        "Início": {
            "color": "#1f77b4",
            "size": 40,
            "symbol": "circle",
            "tooltip": "Início do processo de decisão"
        }
    }
    
    pos = {}
    pos["Início"] = (0, 0)
    
    for i, q in enumerate(questions):
        x = (i + 1) * 2
        y = 0
        q_id = f"{q['characteristic']}"
        pos[q_id] = (x, y)
        
        node_attrs[q_id] = {
            "color": phase_colors.get(q["phase"], "#95a5a6"),
            "size": 35,
            "symbol": "diamond",
            "tooltip": f"{q['phase']}: {q['text']}"
        }
        
        if q["id"] in answers:
            answer = answers[q["id"]]
            answer_id = f"{q['characteristic']}: {answer}"
            pos[answer_id] = (x, -1)
            node_attrs[answer_id] = {
                "color": phase_colors.get(q["phase"], "#95a5a6"),
                "size": 30,
                "symbol": "square",
                "tooltip": f"Resposta: {answer}"
            }
            
            G.add_edge("Início", q_id)
            G.add_edge(q_id, answer_id)

    edge_trace = []
    node_trace = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        ))

    for node in G.nodes():
        x, y = pos[node]
        attrs = node_attrs[node]
        node_trace.append(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            name=node,
            marker=dict(
                symbol=attrs["symbol"],
                size=attrs["size"],
                color=attrs["color"]
            ),
            text=[node],
            textposition="top center",
            hovertext=attrs["tooltip"],
            hoverinfo='text'
        ))

    fig = go.Figure(data=edge_trace + node_trace)
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        title={
            'text': "Fluxo de Decisão Interativo",
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)

def restart_decision_tree():
    if st.button("Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

def run_decision_tree():
    show_interactive_decision_tree()
    st.markdown("---")
    restart_decision_tree()
