import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation
from database import save_recommendation
from dlt_data import questions

def create_progress_animation(current_phase, answers):
    """Create an animated progress visualization."""
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    fig = go.Figure()
    
    phase_progress = {phase: 0 for phase in phases}
    phase_total = {phase: 0 for phase in phases}
    phase_characteristics = {phase: set() for phase in phases}
    
    for q in questions:
        phase = q['phase']
        phase_total[phase] += 1
        phase_characteristics[phase].add(q['characteristic'])
        if q['id'] in answers:
            phase_progress[phase] += 1
    
    for i, phase in enumerate(phases):
        if phase == current_phase:
            color = '#3498db'
            size = 45
        elif phase_progress[phase] > 0:
            color = '#2ecc71'
            size = 40
        else:
            color = '#bdc3c7'
            size = 35
            
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
        
        fig.add_annotation(
            x=i, y=-0.2,
            text=f"{phase}<br>({phase_progress[phase]}/{phase_total[phase]})",
            showarrow=False,
            font=dict(size=12)
        )
        
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

def create_evaluation_matrices(recommendation):
    if not recommendation or 'evaluation_matrix' not in recommendation:
        return
        
    st.subheader("Matriz de Avaliação Detalhada")
    
    # DLT Matrix Section
    with st.expander("ℹ️ Entenda a Matriz de DLTs"):
        st.markdown("""
        ### Matriz de Avaliação de DLTs
        
        Esta matriz mostra a comparação detalhada entre diferentes DLTs baseada em quatro métricas principais:
        
        - **Segurança**: Capacidade de proteger dados e transações
        - **Escalabilidade**: Capacidade de crescer mantendo o desempenho
        - **Eficiência Energética**: Consumo de energia por transação
        - **Governança**: Flexibilidade e controle do sistema
        
        Os valores são normalizados de 0 a 1, onde 1 representa o melhor desempenho.
        """)
    
    # Create DLT comparison heatmap for weighted scores
    st.subheader("Comparação de Métricas das DLTs")
    metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
    dlts = list(recommendation['evaluation_matrix'].keys())
    
    # Prepare data for weighted metrics heatmap
    weighted_values = []
    for metric in metrics:
        row = []
        for dlt in dlts:
            weighted_score = recommendation['evaluation_matrix'][dlt]['weighted_metrics'][metric]
            row.append(weighted_score)
        weighted_values.append(row)
    
    # Get DLT types for labels
    dlt_types = [recommendation['evaluation_matrix'][dlt]['type'] for dlt in dlts]
    
    # Create weighted metrics heatmap
    fig_weighted = go.Figure(data=go.Heatmap(
        z=weighted_values,
        x=dlts,
        y=['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
        colorscale='RdBu',
        hoverongaps=False,
        hovertemplate="<b>DLT:</b> %{x}<br>" +
                     "<b>Tipo:</b> %{customdata}<br>" +
                     "<b>Métrica:</b> %{y}<br>" +
                     "<b>Score Ponderado:</b> %{z:.2f}<br>" +
                     "<extra></extra>",
        customdata=[dlt_types for _ in range(len(metrics))]
    ))
    
    fig_weighted.update_layout(
        title="Scores Ponderados por Tipo de DLT",
        xaxis_title="DLTs",
        yaxis_title="Métricas",
        height=400
    )
    
    st.plotly_chart(fig_weighted, use_container_width=True)
    
    # Consensus Groups Matrix
    st.subheader("Matriz de Grupos de Algoritmos de Consenso")
    with st.expander("ℹ️ Entenda os Grupos de Consenso"):
        st.markdown("""
        ### Grupos de Algoritmos de Consenso
        
        Os algoritmos são agrupados com base em características similares:
        
        1. **Alta Segurança e Controle**
           - PBFT, PoW
           - Ideal para dados sensíveis de saúde
        
        2. **Alta Eficiência Operacional**
           - PoA, RAFT
           - Otimizado para redes menores e controladas
        
        3. **Escalabilidade e Governança**
           - PoS, DPoS
           - Equilibra performance e descentralização
        
        4. **Alta Escalabilidade IoT**
           - Tangle, DAG
           - Especializado em dispositivos IoT
        """)
    
    # Create consensus groups comparison
    consensus_groups = {
        'Alta Segurança': ['PBFT', 'PoW'],
        'Alta Eficiência': ['PoA', 'RAFT'],
        'Escalabilidade': ['PoS', 'DPoS'],
        'IoT': ['Tangle', 'DAG']
    }
    
    consensus_metrics = {
        'Segurança': [0.9, 0.7, 0.8, 0.75],
        'Escalabilidade': [0.7, 0.9, 0.85, 0.95],
        'Eficiência': [0.8, 0.95, 0.9, 0.85],
        'Governança': [0.85, 0.8, 0.9, 0.7]
    }
    
    fig_consensus = go.Figure(data=go.Heatmap(
        z=list(consensus_metrics.values()),
        x=list(consensus_groups.keys()),
        y=list(consensus_metrics.keys()),
        colorscale='RdBu',
        hovertemplate="<b>Grupo:</b> %{x}<br>" +
                     "<b>Métrica:</b> %{y}<br>" +
                     "<b>Score:</b> %{z:.2f}<br>" +
                     "<extra></extra>"
    ))
    
    fig_consensus.update_layout(
        title="Comparação de Grupos de Consenso",
        xaxis_title="Grupos de Consenso",
        yaxis_title="Métricas",
        height=400
    )
    
    st.plotly_chart(fig_consensus, use_container_width=True)
    
    # Consensus Algorithms Matrix
    st.subheader("Matriz de Algoritmos de Consenso")
    with st.expander("ℹ️ Entenda os Algoritmos de Consenso"):
        st.markdown("""
        ### Algoritmos de Consenso Específicos
        
        Cada algoritmo tem características únicas:
        
        - **PBFT**: Alta segurança, ideal para dados sensíveis
        - **PoW**: Máxima descentralização, alto custo energético
        - **PoS**: Eficiente energeticamente, boa escalabilidade
        - **DPoS**: Alta performance, governança democrática
        - **PoA**: Eficiente para redes permissionadas
        - **Tangle**: Otimizado para IoT, alta escalabilidade
        
        A escolha depende dos requisitos específicos do projeto de saúde.
        """)
    
    # Create specific algorithms comparison
    algorithm_metrics = {
        'Tempo de Confirmação': [1, 600, 15, 0.5],
        'Throughput (TPS)': [3000, 7, 100000, 4000],
        'Custo Energético': [0.001, 885, 0.01, 0.1],
        'Descentralização': [5, 10, 8, 7]
    }
    
    fig_algorithms = go.Figure(data=go.Heatmap(
        z=list(algorithm_metrics.values()),
        x=['PBFT', 'PoW', 'PoS', 'DPoS'],
        y=list(algorithm_metrics.keys()),
        colorscale='RdBu',
        hovertemplate="<b>Algoritmo:</b> %{x}<br>" +
                     "<b>Métrica:</b> %{y}<br>" +
                     "<b>Valor:</b> %{z}<br>" +
                     "<extra></extra>"
    ))
    
    fig_algorithms.update_layout(
        title="Comparação de Algoritmos de Consenso",
        xaxis_title="Algoritmos",
        yaxis_title="Métricas",
        height=400
    )
    
    st.plotly_chart(fig_algorithms, use_container_width=True)
    
    # Display final scores
    st.subheader("Scores Finais")
    cols = st.columns(len(dlts))
    for i, dlt in enumerate(dlts):
        with cols[i]:
            st.metric(
                label=dlt,
                value=f"{recommendation['weighted_scores'][dlt]:.2f}",
                delta=f"Raw: {recommendation['raw_scores'][dlt]:.2f}",
                help=f"Score ponderado: {recommendation['weighted_scores'][dlt]:.2f}\n"
                     f"Score bruto: {recommendation['raw_scores'][dlt]:.2f}\n"
                     f"Tipo: {recommendation['evaluation_matrix'][dlt]['type']}"
            )

def run_decision_tree():
    """Main function to run the decision tree interface."""
    st.title("Framework de Seleção de DLT")
    
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    # Add reset button
    if st.button("🔄 Reiniciar", help="Clique para recomeçar o processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()
    
    # Get current phase
    current_phase = None
    for q in questions:
        if q['id'] not in st.session_state.answers:
            current_phase = q['phase']
            break
    
    # Display progress animation
    if current_phase:
        progress_fig = create_progress_animation(current_phase, st.session_state.answers)
        st.plotly_chart(progress_fig, use_container_width=True)
    
    # Display current question
    current_question = None
    for q in questions:
        if q['id'] not in st.session_state.answers:
            current_question = q
            break
    
    if current_question:
        st.subheader(f"Fase: {current_question['phase']}")
        st.info(f"Característica: {current_question['characteristic']}")
        
        response = st.radio(
            current_question['text'],
            current_question['options']
        )
        
        if st.button("Próxima Pergunta"):
            st.session_state.answers[current_question['id']] = response
            st.experimental_rerun()
    
    # Show recommendation when all questions are answered
    if len(st.session_state.answers) == len(questions):
        recommendation = get_recommendation(st.session_state.answers)
        
        st.header("Recomendação")
        st.write(f"DLT Recomendada: {recommendation['dlt']}")
        st.write(f"Tipo de DLT: {recommendation['dlt_type']}")
        st.write(f"Algoritmo de Consenso: {recommendation['consensus']}")
        
        # Display evaluation matrices
        create_evaluation_matrices(recommendation)
        
        # Add save button for authenticated users
        if st.session_state.get('authenticated', False):
            if st.button("💾 Salvar Recomendação"):
                save_recommendation(
                    st.session_state.username,
                    "Healthcare",
                    recommendation
                )
                st.success("Recomendação salva com sucesso!")
