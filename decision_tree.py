import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from decision_logic import get_recommendation, get_consensus_group_algorithms
from database import save_recommendation
from dlt_data import questions

def create_evaluation_matrices(recommendation):
    """Create and display evaluation matrices."""
    if not recommendation or 'evaluation_matrix' not in recommendation:
        return
        
    st.subheader("Matriz de Avaliação Detalhada")
    
    st.markdown('''
    <style>
        .recommended {
            background-color: #e6f3ff;
            font-weight: bold;
        }
        .metric-high {
            color: #2ecc71;
            font-weight: bold;
        }
        .metric-low {
            color: #e74c3c;
        }
        .selected-group {
            background-color: #eafaf1;
        }
        .non-selected-group {
            color: #95a5a6;
        }
    </style>
    ''', unsafe_allow_html=True)
    
    st.info("""
    💡 **Como interpretar os scores:**
    - ✅ Valores ≥ 0.8: Pontos fortes
    - ❌ Valores < 0.8: Áreas que precisam de atenção
    - A pontuação total considera as características com os seguintes pesos:
      - Segurança: 40%
      - Escalabilidade: 25%
      - Eficiência Energética: 20%
      - Governança: 15%
    """)
    
    # Display selected consensus group information
    st.subheader("Grupo de Consenso Selecionado")
    st.info(f"""
    Com base nas características da DLT {recommendation['dlt']} e nos requisitos informados, 
    o grupo de consenso selecionado é: **{recommendation['consensus_group']}**
    
    **Motivo da Seleção:**
    {recommendation['consensus_group_explanation']}
    """)
    
    # Get algorithms for the selected group
    group_info = get_consensus_group_algorithms(recommendation['consensus_group'])
    
    # Display available algorithms
    st.write("**Algoritmos disponíveis neste grupo:**")
    for algorithm in group_info['algorithms']:
        characteristics = group_info['characteristics'][algorithm]
        st.write(f"- **{algorithm}**")
        cols = st.columns(4)
        cols[0].metric("Segurança", f"{characteristics['security']:.2f}")
        cols[1].metric("Escalabilidade", f"{characteristics['scalability']:.2f}")
        cols[2].metric("Eficiência", f"{characteristics['energy_efficiency']:.2f}")
        cols[3].metric("Governança", f"{characteristics['governance']:.2f}")
    
    # Correlation table with highlighting
    st.subheader("Matriz de Correlação DLT-Grupo-Algoritmo")
    st.markdown("""
    💡 **Como interpretar a correlação:**
    - Cada DLT está associada a um grupo de consenso específico baseado em suas características
    - Os algoritmos disponíveis são os mais adequados para cada combinação DLT-Grupo
    - As linhas destacadas mostram a combinação recomendada
    """)
    
    # Create correlation table with selected group highlighted
    correlation_data = {
        'DLT': ['Hyperledger Fabric', 'Corda', 'Quorum', 'VeChain', 'IOTA', 
                'Ripple', 'Stellar', 'Bitcoin', 'Ethereum (PoW)', 'Ethereum 2.0'],
        'Grupo de Consenso': ['Alta Segurança e Controle', 'Alta Segurança e Controle',
                            'Escalabilidade e Governança', 'Alta Eficiência',
                            'Alta Escalabilidade IoT', 'Alta Eficiência',
                            'Alta Eficiência', 'Alta Segurança e Controle',
                            'Alta Segurança e Controle', 'Escalabilidade e Governança']
    }
    
    # Add algorithms column based on consensus group
    correlation_data['Algoritmos Disponíveis'] = [
        ', '.join(get_consensus_group_algorithms(group)['algorithms'])
        for group in correlation_data['Grupo de Consenso']
    ]
    
    correlation_df = pd.DataFrame(correlation_data)
    
    # Apply highlighting to the selected DLT and group
    def highlight_selected(row):
        if row['DLT'] == recommendation['dlt']:
            return ['background-color: #eafaf1'] * len(row)
        elif row['Grupo de Consenso'] == recommendation['consensus_group']:
            return ['background-color: #f0f9ff'] * len(row)
        return [''] * len(row)
    
    styled_df = correlation_df.style.apply(highlight_selected, axis=1)
    st.table(styled_df)
    
    # Add explanation for group selection
    st.info(f"""
    **Por que este grupo de consenso foi selecionado?**
    - A DLT {recommendation['dlt']} pertence ao grupo {recommendation['consensus_group']}
    - O algoritmo {recommendation['consensus']} foi selecionado com score {recommendation['consensus_score']:.2f}
    - Este grupo oferece o melhor equilíbrio entre segurança ({recommendation['consensus_characteristics']['security']:.2f}),
      escalabilidade ({recommendation['consensus_characteristics']['scalability']:.2f}),
      eficiência energética ({recommendation['consensus_characteristics']['energy_efficiency']:.2f}) e
      governança ({recommendation['consensus_characteristics']['governance']:.2f})
    """)
    
    # Display comparison table
    scores_df = pd.DataFrame({
        'Tipo de DLT': [recommendation['evaluation_matrix'][dlt]['type'] for dlt in recommendation['evaluation_matrix']],
        'DLT': list(recommendation['evaluation_matrix'].keys()),
        'Score Total': [recommendation['weighted_scores'][dlt] for dlt in recommendation['evaluation_matrix']],
        'Segurança': [recommendation['evaluation_matrix'][dlt]['metrics']['security'] for dlt in recommendation['evaluation_matrix']],
        'Escalabilidade': [recommendation['evaluation_matrix'][dlt]['metrics']['scalability'] for dlt in recommendation['evaluation_matrix']],
        'Eficiência': [recommendation['evaluation_matrix'][dlt]['metrics']['energy_efficiency'] for dlt in recommendation['evaluation_matrix']],
        'Governança': [recommendation['evaluation_matrix'][dlt]['metrics']['governance'] for dlt in recommendation['evaluation_matrix']]
    }).sort_values('Score Total', ascending=False)
    
    def highlight_recommended(row):
        return ['background-color: #e6f3ff' if row.name == 0 else '' for _ in row]
    
    def highlight_metrics(val):
        if isinstance(val, float):
            if val >= 0.8:
                return 'color: #2ecc71; font-weight: bold'
            elif val <= 0.4:
                return 'color: #e74c3c'
        return ''
    
    scores_styled = scores_df.style\
        .apply(highlight_recommended, axis=1)\
        .map(highlight_metrics, subset=['Segurança', 'Escalabilidade', 'Eficiência', 'Governança'])
    
    st.subheader("Tabela Comparativa de DLTs")
    st.table(scores_styled)
    st.caption("💡 A linha destacada em azul indica a DLT recomendada. Métricas em verde são pontos fortes (≥0.8) e em vermelho são pontos de atenção (≤0.4).")

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

def run_decision_tree():
    """Main function to run the decision tree interface."""
    st.title("Framework de Seleção de DLT")
    
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    if st.button("🔄 Reiniciar", help="Clique para recomeçar o processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()
    
    current_phase = None
    for q in questions:
        if q['id'] not in st.session_state.answers:
            current_phase = q['phase']
            break
    
    if current_phase:
        progress_fig = create_progress_animation(current_phase, st.session_state.answers)
        st.plotly_chart(progress_fig, use_container_width=True)
    
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
    
    if len(st.session_state.answers) == len(questions):
        recommendation = get_recommendation(st.session_state.answers)
        
        st.header("Recomendação")
        st.write(f"DLT Recomendada: {recommendation['dlt']}")
        st.write(f"Tipo de DLT: {recommendation['dlt_type']}")
        st.write(f"Algoritmo de Consenso: {recommendation['consensus']}")
        
        create_evaluation_matrices(recommendation)
        
        if st.session_state.get('authenticated', False):
            if st.button("💾 Salvar Recomendação"):
                save_recommendation(
                    st.session_state.username,
                    "Healthcare",
                    recommendation
                )
                st.success("Recomendação salva com sucesso!")
