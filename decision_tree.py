import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from decision_logic import get_recommendation, get_consensus_group_algorithms
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
    """Create and display evaluation matrices."""
    try:
        if not recommendation or not isinstance(recommendation, dict):
            st.warning("Recomendação indisponível ou inválida.")
            return
            
        if 'evaluation_matrix' not in recommendation:
            st.warning("Matriz de avaliação não encontrada na recomendação.")
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
        dlt_name = recommendation.get('dlt', 'Não disponível')
        consensus_group = recommendation.get('consensus_group', 'Não disponível')
        group_explanation = recommendation.get('consensus_group_explanation', '')
        
        st.info(f"""
        Com base nas características da DLT {dlt_name} e nos requisitos informados, 
        o grupo de consenso selecionado é: **{consensus_group}**
        
        **Motivo da Seleção:**
        {group_explanation}
        """)
        
        # Get algorithms for the selected group
        group_info = get_consensus_group_algorithms(consensus_group)
        
        # Display available algorithms
        st.write("**Algoritmos disponíveis neste grupo:**")
        for algorithm in group_info.get('algorithms', []):
            characteristics = group_info.get('characteristics', {}).get(algorithm, {})
            st.write(f"- **{algorithm}**")
            cols = st.columns(4)
            cols[0].metric("Segurança", f"{characteristics.get('security', 0.0):.2f}")
            cols[1].metric("Escalabilidade", f"{characteristics.get('scalability', 0.0):.2f}")
            cols[2].metric("Eficiência", f"{characteristics.get('energy_efficiency', 0.0):.2f}")
            cols[3].metric("Governança", f"{characteristics.get('governance', 0.0):.2f}")
        
        # Create comparison table
        try:
            scores_df = pd.DataFrame({
                'Tipo de DLT': [recommendation['evaluation_matrix'][dlt].get('type', 'N/A') 
                               for dlt in recommendation['evaluation_matrix']],
                'DLT': list(recommendation['evaluation_matrix'].keys()),
                'Score Total': [recommendation['weighted_scores'].get(dlt, 0.0) 
                               for dlt in recommendation['evaluation_matrix']],
                'Segurança': [recommendation['evaluation_matrix'][dlt].get('metrics', {}).get('security', 0.0) 
                             for dlt in recommendation['evaluation_matrix']],
                'Escalabilidade': [recommendation['evaluation_matrix'][dlt].get('metrics', {}).get('scalability', 0.0) 
                                  for dlt in recommendation['evaluation_matrix']],
                'Eficiência': [recommendation['evaluation_matrix'][dlt].get('metrics', {}).get('energy_efficiency', 0.0) 
                              for dlt in recommendation['evaluation_matrix']],
                'Governança': [recommendation['evaluation_matrix'][dlt].get('metrics', {}).get('governance', 0.0) 
                              for dlt in recommendation['evaluation_matrix']]
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
            
        except Exception as e:
            st.error(f"Erro ao criar tabela comparativa: {str(e)}")
            
    except Exception as e:
        st.error(f"Erro ao criar matrizes de avaliação: {str(e)}")

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
