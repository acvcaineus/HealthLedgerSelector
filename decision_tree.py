import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dlt_data import questions, dlt_metrics, dlt_type_weights, dlt_classes, consensus_algorithms
from decision_logic import get_consensus_group_algorithms, get_recommendation
from database import save_recommendation

def create_progress_animation(current_phase, answers, questions):
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
        
        st.subheader("Classificação e Recomendação de DLTs")
        
        # Display classification levels
        with st.expander("ℹ️ Estrutura de Classificação"):
            st.write("1. Tipo de DLT:", recommendation.get('dlt_type', 'N/A'))
            st.write("2. Grupo de Algoritmo:", recommendation.get('consensus_group', 'N/A'))
            st.write("3. Algoritmo de Consenso:", recommendation.get('consensus', 'N/A'))

        # Show recommendation with justification
        st.subheader("Recomendação Principal")
        st.write(f"DLT Recomendada: {recommendation['dlt']}")
        
        # Get detailed information from the reference table
        dlt_info = recommendation.get('dlt_details', {})
        
        with st.expander("📊 Características Técnicas"):
            if 'technical_characteristics' in dlt_info:
                st.write(dlt_info['technical_characteristics'])
            else:
                metrics = recommendation['evaluation_matrix'].get(recommendation['dlt'], {}).get('metrics', {})
                for metric, value in metrics.items():
                    st.metric(metric.replace('_', ' ').title(), f"{value:.2f}")
        
        with st.expander("🎯 Casos de Uso"):
            if 'use_cases' in dlt_info:
                st.write(dlt_info['use_cases'])
            else:
                st.write("Informação não disponível")
        
        with st.expander("⚠️ Desafios e Limitações"):
            if 'challenges' in dlt_info:
                st.write(dlt_info['challenges'])
            else:
                st.write("Informação não disponível")
        
        with st.expander("📚 Referências Bibliográficas"):
            if 'references' in dlt_info:
                st.write(dlt_info['references'])
            else:
                st.write("Informação não disponível")

        # Weight information display
        if 'adjusted_weights' in recommendation and 'weight_explanations' in recommendation:
            with st.expander("⚖️ Pesos e Justificativas"):
                weights = recommendation['adjusted_weights']
                explanations = recommendation['weight_explanations']
                
                for metric, weight in weights.items():
                    st.write(f"**{metric.replace('_', ' ').title()}:** {weight:.2%}")
                    if explanations.get(metric):
                        st.write("*Justificativa:* " + ", ".join(explanations[metric]))
                    st.write("---")

        # Create comparison table with enhanced styling
        st.subheader("Comparação de DLTs")
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
                is_recommended = row['DLT'] == recommendation['dlt']
                return ['background-color: #e6f3ff; font-weight: bold' if is_recommended else '' for _ in row]
            
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
        progress_fig = create_progress_animation(current_phase, st.session_state.answers, questions)
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
        
        create_evaluation_matrices(recommendation)
        
        if st.session_state.get('authenticated', False):
            if st.button("💾 Salvar Recomendação"):
                save_recommendation(
                    st.session_state.username,
                    "Healthcare",
                    recommendation
                )
                st.success("Recomendação salva com sucesso!")
