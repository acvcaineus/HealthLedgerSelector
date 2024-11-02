import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from decision_logic import get_recommendation
from database import save_recommendation
from dlt_data import questions, dlt_metrics

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
    metrics_pt = ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança']
    dlts = list(recommendation['evaluation_matrix'].keys())
    
    # Prepare data for weighted metrics heatmap
    weighted_values = []
    for dlt in dlts:
        row = []
        for metric in metrics:
            weighted_score = recommendation['evaluation_matrix'][dlt]['weighted_metrics'][metric]
            row.append(weighted_score)
        weighted_values.append(row)
    
    # Get DLT types for labels
    dlt_types = [recommendation['evaluation_matrix'][dlt]['type'] for dlt in dlts]
    
    # Create weighted metrics heatmap with swapped axes
    fig_weighted = go.Figure(data=go.Heatmap(
        z=weighted_values,
        y=dlts,  # Swapped with x
        x=metrics_pt,  # Swapped with y
        colorscale='RdBu',
        hoverongaps=False,
        hovertemplate="<b>DLT:</b> %{y}<br>" +  # Updated for swapped axes
                     "<b>Tipo:</b> %{customdata}<br>" +
                     "<b>Métrica:</b> %{x}<br>" +  # Updated for swapped axes
                     "<b>Score Ponderado:</b> %{z:.2f}<br>" +
                     "<extra></extra>",
        customdata=dlt_types
    ))
    
    fig_weighted.update_layout(
        title="Scores Ponderados por Tipo de DLT",
        yaxis_title="DLTs",  # Swapped with xaxis
        xaxis_title="Métricas",  # Swapped with yaxis
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
        y=list(consensus_groups.keys()),  # Swapped with x
        x=list(consensus_metrics.keys()),  # Swapped with y
        colorscale='RdBu',
        hovertemplate="<b>Grupo:</b> %{y}<br>" +  # Updated for swapped axes
                     "<b>Métrica:</b> %{x}<br>" +  # Updated for swapped axes
                     "<b>Score:</b> %{z:.2f}<br>" +
                     "<extra></extra>"
    ))
    
    fig_consensus.update_layout(
        title="Comparação de Grupos de Consenso",
        yaxis_title="Grupos de Consenso",  # Swapped with xaxis
        xaxis_title="Métricas",  # Swapped with yaxis
        height=400
    )
    
    st.plotly_chart(fig_consensus, use_container_width=True)
    
    # Create score comparison table
    scores_df = pd.DataFrame({
        'DLT': dlts,
        'Score Total': [recommendation['weighted_scores'][dlt] for dlt in dlts],
        'Segurança': [recommendation['evaluation_matrix'][dlt]['raw_metrics']['security'] for dlt in dlts],
        'Escalabilidade': [recommendation['evaluation_matrix'][dlt]['raw_metrics']['scalability'] for dlt in dlts],
        'Eficiência': [recommendation['evaluation_matrix'][dlt]['raw_metrics']['energy_efficiency'] for dlt in dlts],
        'Governança': [recommendation['evaluation_matrix'][dlt]['raw_metrics']['governance'] for dlt in dlts]
    }).sort_values('Score Total', ascending=False)
    
    st.subheader("Tabela Comparativa de DLTs")
    st.table(scores_df)

def display_recommendation_details(recommendation):
    """Display detailed recommendation information."""
    st.header("Recomendação")
    st.write(f"DLT Recomendada: {recommendation['dlt']}")
    st.write(f"Tipo de DLT: {recommendation['dlt_type']}")
    
    # Get consensus group based on DLT type
    consensus_groups = {
        "DLT Permissionada Privada": "Alta Segurança e Controle",
        "DLT Permissionada Simples": "Alta Eficiência Operacional",
        "DLT Híbrida": "Escalabilidade e Governança Flexível",
        "DLT com Consenso Delegado": "Alta Escalabilidade em Redes IoT",
        "DLT Pública": "Alta Segurança e Descentralização",
        "DLT Pública Permissionless": "Escalabilidade e Governança Flexível"
    }
    
    consensus_group = consensus_groups.get(recommendation['dlt_type'], "Grupo não especificado")
    st.write(f"Grupo de Consenso: {consensus_group}")
    st.write(f"Algoritmo de Consenso: {recommendation['consensus']}")
    
    st.subheader("Explicação da Escolha")
    st.markdown(f"""
    ### Razões para a Escolha:
    1. **Características Priorizadas**:
       - Segurança: {recommendation['evaluation_matrix'][recommendation['dlt']]['raw_metrics']['security']:.2f}
       - Escalabilidade: {recommendation['evaluation_matrix'][recommendation['dlt']]['raw_metrics']['scalability']:.2f}
       - Eficiência Energética: {recommendation['evaluation_matrix'][recommendation['dlt']]['raw_metrics']['energy_efficiency']:.2f}
       - Governança: {recommendation['evaluation_matrix'][recommendation['dlt']]['raw_metrics']['governance']:.2f}
    
    2. **Compatibilidade com Cenário**:
       Esta DLT é especialmente adequada para cenários de saúde devido à sua {get_main_strength(recommendation)}
    
    3. **Vantagens do Algoritmo**:
       O algoritmo de consenso {recommendation['consensus']} foi escolhido por sua {get_algorithm_advantages(recommendation)}
    
    ### Cenários de Aplicação Recomendados:
    {get_recommended_scenarios(recommendation)}
    """)

def get_main_strength(recommendation):
    """Get the main strength of the recommended DLT."""
    metrics = recommendation['evaluation_matrix'][recommendation['dlt']]['raw_metrics']
    max_metric = max(metrics.items(), key=lambda x: x[1])
    
    strength_descriptions = {
        'security': "alta segurança e proteção de dados sensíveis",
        'scalability': "excelente escalabilidade e capacidade de processamento",
        'energy_efficiency': "eficiência energética superior",
        'governance': "governança flexível e controle granular"
    }
    
    return strength_descriptions.get(max_metric[0], "combinação equilibrada de características")

def get_algorithm_advantages(recommendation):
    """Get the advantages of the recommended consensus algorithm."""
    algorithm_advantages = {
        'PBFT': "alta segurança e finalidade imediata, ideal para dados sensíveis de saúde",
        'PoW': "forte descentralização e segurança",
        'PoS': "eficiência energética e boa escalabilidade",
        'DPoS': "alta performance e governança democrática",
        'PoA': "eficiência em redes permissionadas",
        'RAFT': "simplicidade e eficiência em redes menores",
        'Tangle': "escalabilidade superior em ambientes IoT"
    }
    
    return algorithm_advantages.get(recommendation['consensus'], 
                                  "combinação de características adequadas ao cenário de saúde")

def get_recommended_scenarios(recommendation):
    """Get recommended scenarios based on DLT type."""
    scenarios = {
        "DLT Permissionada Privada": """
        - Registros médicos eletrônicos (EMR)
        - Compartilhamento seguro de dados entre hospitais
        - Gerenciamento de prontuários eletrônicos""",
        
        "DLT Permissionada Simples": """
        - Sistemas locais de saúde
        - Gerenciamento de agendamentos
        - Controle de acesso a registros""",
        
        "DLT Híbrida": """
        - Interoperabilidade entre sistemas de saúde
        - Cadeia de suprimentos farmacêutica
        - Rastreamento de medicamentos""",
        
        "DLT com Consenso Delegado": """
        - Monitoramento de dispositivos IoT médicos
        - Coleta de dados em tempo real
        - Telemedicina""",
        
        "DLT Pública": """
        - Pesquisa médica descentralizada
        - Compartilhamento global de dados anônimos
        - Validação de credenciais médicas""",
        
        "DLT Pública Permissionless": """
        - Sistemas de pagamento em saúde
        - Marketplace de serviços médicos
        - Gestão de seguros de saúde"""
    }
    
    return scenarios.get(recommendation['dlt_type'], 
                        "- Aplicações gerais de saúde\n- Sistemas de registro médico\n- Gestão de dados clínicos")

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
        
        # Display detailed recommendation
        display_recommendation_details(recommendation)
        
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
