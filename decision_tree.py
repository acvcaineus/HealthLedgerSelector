import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation
import networkx as nx
import plotly.figure_factory as ff

def show_interactive_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")

    questions = [
        {
            "id": "privacy",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"],
            "phase": "Segurança"
        },
        {
            "id": "integration",
            "text": "É necessária integração com outros sistemas de saúde?",
            "options": ["Sim", "Não"],
            "phase": "Interoperabilidade"
        },
        {
            "id": "data_volume",
            "text": "O sistema precisa lidar com grandes volumes de registros médicos?",
            "options": ["Sim", "Não"],
            "phase": "Escalabilidade"
        },
        {
            "id": "energy_efficiency",
            "text": "A eficiência energética é uma preocupação importante?",
            "options": ["Sim", "Não"],
            "phase": "Eficiência"
        }
    ]

    # Show progress bar
    progress = len(st.session_state.answers) / len(questions)
    st.progress(progress, text=f"Progresso: {int(progress * 100)}%")

    current_question = None
    for q in questions:
        if q["id"] not in st.session_state.answers:
            current_question = q
            break

    if current_question:
        st.subheader(f"Fase: {current_question['phase']}")
        st.subheader(f"Pergunta {len(st.session_state.answers) + 1} de {len(questions)}")
        response = st.radio(current_question["text"], current_question["options"])

        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question["id"]] = response
            st.rerun()

    # Show decision flow diagram
    if st.session_state.answers:
        st.subheader("Fluxo de Decisão")
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
    # Create nodes for the decision flow
    nodes = []
    edges = []
    node_colors = []

    # Add start node
    nodes.append("Início")
    node_colors.append('#1f77b4')  # Blue

    # Add question nodes and edges
    for q in questions:
        q_id = q["id"]
        nodes.append(q["text"])
        edges.append(("Início", q["text"]))
        
        if q_id in answers:
            node_colors.append('#2ecc71')  # Green for answered
            nodes.append(answers[q_id])
            edges.append((q["text"], answers[q_id]))
        else:
            node_colors.append('#e74c3c')  # Red for unanswered

    # Create the graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Create positions for the nodes
    pos = nx.spring_layout(G)

    # Create the plotly figure
    edge_trace = go.Scatter(
        x=[], y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_trace = go.Scatter(
        x=[], y=[],
        mode='markers+text',
        hoverinfo='text',
        text=nodes,
        marker=dict(
            showscale=False,
            color=node_colors,
            size=30,
        ))

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20,l=5,r=5,t=40),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                   )
    
    st.plotly_chart(fig)

def show_recommendation(answers, weights):
    recommendation = get_recommendation(answers, weights)

    st.header("Recomendação")
    st.write(f"**DLT Recomendada:** {recommendation['dlt']}")
    st.write(f"**Grupo de Consenso:** {recommendation['consensus_group']}")
    st.write(f"**Algoritmo de Consenso:** {recommendation['consensus']}")

    # Visual evaluation matrix (heatmap)
    st.subheader("Matriz de Avaliação (Visual)")
    if 'evaluation_matrix' in recommendation:
        matrix_data = []
        y_labels = []
        metric_explanations = {
            "security": "Nível de segurança e proteção dos dados",
            "scalability": "Capacidade de crescimento e processamento",
            "energy_efficiency": "Consumo e eficiência energética",
            "governance": "Flexibilidade e controle da rede",
            "academic_validation": "Validação em estudos acadêmicos"
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

        fig = go.Figure(data=go.Heatmap(
            z=matrix_data,
            x=list(recommendation['evaluation_matrix'][y_labels[0]]['metrics'].keys()),
            y=y_labels,
            colorscale='Viridis',
            hoverongaps=False,
            hovertemplate="DLT: %{y}<br>Métrica: %{x}<br>Valor: %{z:.2f}<extra></extra>"
        ))

        fig.update_layout(
            title="Matriz de Avaliação das DLTs",
            xaxis_title="Métricas",
            yaxis_title="DLTs"
        )
        st.plotly_chart(fig)

        # Detailed explanation section
        st.subheader("Explicação da Recomendação")
        st.write(f"### Por que {recommendation['dlt']}?")
        st.write("Baseado nas suas respostas e nos critérios de avaliação:")
        
        metrics_by_category = {
            "Segurança": ["security"],
            "Desempenho": ["scalability", "energy_efficiency"],
            "Governança": ["governance"],
            "Validação": ["academic_validation"]
        }

        for category, metrics in metrics_by_category.items():
            with st.expander(f"{category}"):
                for metric in metrics:
                    if metric in recommendation['evaluation_matrix'][recommendation['dlt']]['metrics']:
                        value = float(recommendation['evaluation_matrix'][recommendation['dlt']]['metrics'][metric])
                        st.write(f"- **{metric}**: {value:.2f}")
                        st.write(f"  *{metric_explanations.get(metric, '')}*")

    # Consensus algorithm scores visualization
    st.subheader("Pontuações dos Algoritmos de Consenso")
    if 'algorithms' in recommendation:
        consensus_scores = {}
        for alg in recommendation['algorithms']:
            if alg in consensus_algorithms:
                total_score = 0.0
                metric_scores = {}
                for metric, value in consensus_algorithms[alg].items():
                    try:
                        metric_weight = float(weights.get(metric, 0.25))
                        value = float(value)  # Ensure value is float
                        weighted_score = value * metric_weight
                        total_score += weighted_score
                        metric_scores[metric] = weighted_score
                    except (ValueError, TypeError) as e:
                        st.warning(f"Erro ao calcular pontuação para {alg}, {metric}: {e}")
                        continue
                consensus_scores[alg] = float(total_score)

        if consensus_scores:
            fig = go.Figure(data=[
                go.Bar(
                    x=list(consensus_scores.keys()),
                    y=[float(score) for score in consensus_scores.values()],
                    text=[f"{score:.2f}" for score in consensus_scores.values()],
                    textposition='auto',
                )
            ])
            fig.update_layout(
                title="Pontuação dos Algoritmos de Consenso",
                xaxis_title="Algoritmos",
                yaxis_title="Pontuação Ponderada",
                showlegend=False
            )
            st.plotly_chart(fig)

    return recommendation

def restart_decision_tree():
    if st.button("Reiniciar"):
        st.session_state.answers = {}
        st.rerun()

def run_decision_tree():
    show_interactive_decision_tree()
    st.markdown("---")
    restart_decision_tree()
