import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from decision_logic import get_recommendation, consensus_algorithms, consensus_groups, compare_algorithms
from database import save_recommendation

def create_progress_animation(current_phase, answers, questions):
    """Create an animated progress visualization with improved features."""
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    fig = go.Figure()
    
    # Initialize progress tracking for each phase
    phase_progress = {phase: 0 for phase in phases}
    phase_total = {phase: 0 for phase in phases}
    phase_characteristics = {phase: set() for phase in phases}
    
    # Calculate progress and collect characteristics for each phase
    for q in questions:
        phase = q['phase']
        phase_total[phase] += 1
        phase_characteristics[phase].add(q['characteristic'])
        if q['id'] in answers:
            phase_progress[phase] += 1
    
    # Create visualization elements for each phase
    for i, phase in enumerate(phases):
        # Dynamic styling based on phase status
        if phase == current_phase:
            color = '#3498db'  # Blue for current phase
            size = 45
        elif phase_progress[phase] > 0:
            color = '#2ecc71'  # Green for completed phases
            size = 40
        else:
            color = '#bdc3c7'  # Gray for upcoming phases
            size = 35
            
        # Create detailed tooltip with phase information
        tooltip = f"<b>{phase}</b><br>"
        tooltip += f"Progresso: {phase_progress[phase]}/{phase_total[phase]}<br>"
        tooltip += "<br>Características:<br>"
        tooltip += "<br>".join([f"- {char}" for char in phase_characteristics[phase]])
        
        # Add phase marker
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
        
        # Add connecting lines between phases
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
    
    # Update layout for clean visualization
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
        
    st.subheader("🎯 Matrizes de Avaliação")
    
    # DLT Matrix - Fix the metrics data structure
    st.markdown("### Matriz de DLTs")
    dlt_data = {}
    metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
    
    for dlt, data in recommendation['evaluation_matrix'].items():
        dlt_data[dlt] = {
            metric: float(data['metrics'][metric])
            for metric in metrics
        }
    
    dlt_df = pd.DataFrame.from_dict(dlt_data, orient='index')
    dlt_df.columns = ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança']
    st.dataframe(dlt_df)
    
    # Create radar chart with correct data mapping
    fig_dlt = go.Figure()
    for dlt, data in dlt_data.items():
        values = [data[metric] for metric in metrics]
        values.append(values[0])  # Close the polygon
        fig_dlt.add_trace(go.Scatterpolar(
            r=values,
            theta=['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança', 'Segurança'],
            name=dlt,
            fill='toself'
        ))
    
    fig_dlt.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True,
        title="Comparação de DLTs"
    )
    st.plotly_chart(fig_dlt)
    
    # Algorithm Groups Matrix
    if 'consensus_group' in recommendation and recommendation['consensus_group'] in consensus_groups:
        st.markdown("### Matriz de Grupos de Algoritmos")
        group = recommendation['consensus_group']
        group_data = consensus_groups[group]['characteristics']
        group_df = pd.DataFrame([group_data])
        group_df.columns = ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança']
        st.dataframe(group_df)
        
        # Create radar chart for group
        fig_group = go.Figure()
        values = [group_data[metric] for metric in metrics]
        values.append(values[0])
        fig_group.add_trace(go.Scatterpolar(
            r=values,
            theta=['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança', 'Segurança'],
            name=group,
            fill='toself'
        ))
        fig_group.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True,
            title=f"Características do Grupo {group}"
        )
        st.plotly_chart(fig_group)
    
    # Consensus Algorithms Matrix
    if 'consensus_group' in recommendation:
        st.markdown("### Matriz de Algoritmos de Consenso")
        group = recommendation['consensus_group']
        algorithms = consensus_groups[group]['algorithms']
        
        algo_data = {
            alg: consensus_algorithms[alg]
            for alg in algorithms
            if alg in consensus_algorithms
        }
        
        algo_df = pd.DataFrame.from_dict(algo_data, orient='index')
        algo_df.columns = ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança']
        st.dataframe(algo_df)
        
        # Create radar chart for algorithms
        fig_algo = go.Figure()
        for alg, data in algo_data.items():
            values = [float(data[metric]) for metric in metrics]
            values.append(values[0])
            fig_algo.add_trace(go.Scatterpolar(
                r=values,
                theta=['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança', 'Segurança'],
                name=alg,
                fill='toself'
            ))
        
        fig_algo.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True,
            title=f"Comparação dos Algoritmos do Grupo {group}"
        )
        st.plotly_chart(fig_algo)

def run_decision_tree():
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    st.title("Framework de Seleção de DLT")

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
    
    progress_fig = create_progress_animation(current_phase, st.session_state.answers, questions)
    st.plotly_chart(progress_fig, use_container_width=True)
    
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
        st.session_state.recommendation = get_recommendation(st.session_state.answers, weights)
        
        # Display recommendation
        st.header("Recomendação")
        st.write(f"DLT Recomendada: {st.session_state.recommendation['dlt']}")
        st.write(f"Algoritmo de Consenso: {st.session_state.recommendation['consensus']}")
        
        # Add save button for authenticated users
        if st.session_state.get('authenticated', False):
            if st.button("💾 Salvar Recomendação"):
                save_recommendation(
                    st.session_state.username,
                    "Healthcare",
                    st.session_state.recommendation
                )
                st.success("Recomendação salva com sucesso!")
        
        # Show evaluation matrices
        create_evaluation_matrices(st.session_state.recommendation)