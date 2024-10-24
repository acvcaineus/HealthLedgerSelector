import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
import networkx as nx
import plotly.figure_factory as ff
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def show_interactive_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")
    
    questions = [
        {
            "id": "privacy",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"],
            "phase": "Segurança",
            "tooltip": "Considere requisitos de LGPD e HIPAA para proteção de dados sensíveis",
            "impact": ["Proteção de dados", "Conformidade regulatória"]
        },
        {
            "id": "integration",
            "text": "É necessária integração com outros sistemas de saúde?",
            "options": ["Sim", "Não"],
            "phase": "Interoperabilidade",
            "tooltip": "Avalie a necessidade de comunicação com sistemas legados ou externos",
            "impact": ["Comunicação entre sistemas", "Flexibilidade da solução"]
        },
        {
            "id": "data_volume",
            "text": "O sistema precisa lidar com grandes volumes de registros médicos?",
            "options": ["Sim", "Não"],
            "phase": "Escalabilidade",
            "tooltip": "Considere o volume de transações e armazenamento necessário",
            "impact": ["Capacidade de processamento", "Performance do sistema"]
        },
        {
            "id": "energy_efficiency",
            "text": "A eficiência energética é uma preocupação importante?",
            "options": ["Sim", "Não"],
            "phase": "Eficiência",
            "tooltip": "Avalie o impacto do consumo energético na operação",
            "impact": ["Sustentabilidade", "Custos operacionais"]
        }
    ]

    current_phase = next((q["phase"] for q in questions if q["id"] not in st.session_state.answers), "Completo")
    progress = len(st.session_state.answers) / len(questions)
    
    # Enhanced progress display with color coding
    progress_color = "#2ecc71" if progress > 0.75 else "#f1c40f" if progress > 0.5 else "#e74c3c"
    st.markdown(f"""
    <div style='background-color: {progress_color}; padding: 10px; border-radius: 5px; color: white;'>
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
    
    # Enhanced node attributes with tooltips
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
        q_id = f"Q{i+1}: {q['text']}"
        pos[q_id] = (x, y)
        
        node_attrs[q_id] = {
            "color": "#2ecc71" if q["id"] in answers else "#e74c3c",
            "size": 35,
            "symbol": "diamond",
            "tooltip": q["tooltip"]
        }
        
        if q["id"] in answers:
            answer = answers[q["id"]]
            answer_id = f"A{i+1}: {answer}"
            pos[answer_id] = (x, -1)
            node_attrs[answer_id] = {
                "color": "#3498db",
                "size": 30,
                "symbol": "square",
                "tooltip": f"Resposta selecionada: {answer}"
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

def show_recommendation(answers, weights):
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação Final")
    
    # Main recommendation display
    col1, col2 = st.columns(2)
    
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
            delta=f"{'↑' if confidence_score else '→'}"
        )

    # New section: Advantages and Disadvantages
    st.subheader("Análise da Recomendação")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Vantagens")
        advantages = {
            "DLT Permissionada Privada": [
                "Alta segurança e privacidade",
                "Controle de acesso granular",
                "Conformidade com regulamentações"
            ],
            "DLT Pública": [
                "Máxima descentralização",
                "Transparência total",
                "Resistência à censura"
            ],
            "DLT Híbrida": [
                "Flexibilidade de configuração",
                "Balanceamento de privacidade/transparência",
                "Escalabilidade customizável"
            ]
        }
        for adv in advantages.get(recommendation['dlt'], []):
            st.markdown(f"✓ {adv}")
    
    with col2:
        st.markdown("#### Desvantagens")
        disadvantages = {
            "DLT Permissionada Privada": [
                "Menor descentralização",
                "Custos de infraestrutura",
                "Complexidade de gestão"
            ],
            "DLT Pública": [
                "Menor privacidade",
                "Custos de transação variáveis",
                "Menor controle"
            ],
            "DLT Híbrida": [
                "Maior complexidade técnica",
                "Necessidade de governança híbrida",
                "Custos de manutenção"
            ]
        }
        for disadv in disadvantages.get(recommendation['dlt'], []):
            st.markdown(f"⚠ {disadv}")

    # Enhanced evaluation matrix
    st.subheader("Matriz de Avaliação Detalhada")
    if 'evaluation_matrix' in recommendation:
        matrix_data = []
        y_labels = []
        metrics_info = {
            "security": {
                "name": "Segurança",
                "description": "Proteção de dados e resistência a ataques",
                "scale": "1-5, onde 5 indica máxima segurança"
            },
            "scalability": {
                "name": "Escalabilidade",
                "description": "Capacidade de crescimento e processamento",
                "scale": "1-5, onde 5 indica máxima escalabilidade"
            },
            "energy_efficiency": {
                "name": "Eficiência Energética",
                "description": "Consumo e impacto ambiental",
                "scale": "1-5, onde 5 indica máxima eficiência"
            },
            "governance": {
                "name": "Governança",
                "description": "Controle e gestão da rede",
                "scale": "1-5, onde 5 indica melhor governança"
            },
            "academic_validation": {
                "name": "Validação Acadêmica",
                "description": "Respaldo em pesquisas científicas",
                "scale": "1-5, onde 5 indica maior validação"
            }
        }

        for dlt, data in recommendation['evaluation_matrix'].items():
            y_labels.append(dlt)
            row = []
            for metric, value in data['metrics'].items():
                try:
                    row.append(float(value))
                except (ValueError, TypeError):
                    row.append(0.0)
            matrix_data.append(row)

        # Create heatmap with enhanced tooltips
        fig = go.Figure(data=go.Heatmap(
            z=matrix_data,
            x=[metrics_info[m]["name"] for m in recommendation['evaluation_matrix'][y_labels[0]]['metrics'].keys()],
            y=y_labels,
            colorscale=[
                [0, "#ff0000"],    # Red for low values
                [0.5, "#ffff00"],  # Yellow for medium values
                [1, "#00ff00"]     # Green for high values
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

        # Metrics explanation with tooltips
        st.subheader("Explicação das Métricas")
        for metric, info in metrics_info.items():
            with st.expander(f"{info['name']} - {info['scale']}"):
                st.write(info['description'])
                if metric in recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']:
                    value = float(recommendation['evaluation_matrix'][recommendation['dlt']]['metrics'][metric])
                    st.metric(
                        label="Pontuação",
                        value=f"{value:.2f}/5.0",
                        help=f"Escala: {info['scale']}"
                    )

        # Comparative Analysis
        st.subheader("Análise Comparativa")
        comp_fig = go.Figure()
        
        for i, dlt in enumerate(y_labels):
            comp_fig.add_trace(go.Scatter(
                x=[metrics_info[m]["name"] for m in recommendation['evaluation_matrix'][dlt]['metrics'].keys()],
                y=[float(v) for v in recommendation['evaluation_matrix'][dlt]['metrics'].values()],
                name=dlt,
                mode='lines+markers',
                line=dict(width=2),
                marker=dict(size=8),
                hovertemplate="<b>%{x}</b><br>" +
                             "Valor: %{y:.2f}<br>" +
                             "<extra></extra>"
            ))

        comp_fig.update_layout(
            title="Comparação entre DLTs",
            xaxis_title="Métricas",
            yaxis_title="Pontuação",
            yaxis=dict(range=[0, 5]),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            hovermode="x unified"
        )
        
        st.plotly_chart(comp_fig, use_container_width=True)

    return recommendation

def restart_decision_tree():
    if st.button("Reiniciar Processo", help="Clique para começar um novo processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()

def run_decision_tree():
    show_interactive_decision_tree()
    st.markdown("---")
    restart_decision_tree()
