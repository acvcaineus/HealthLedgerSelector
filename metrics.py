import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from decision_logic import get_recommendation

def reset_metrics():
    """Reset all stored metrics calculations."""
    metrics_keys = [
        'gini_index',
        'entropy_value',
        'pruning_metrics',
        'precision_metrics',
        'depth_metrics',
        'consistency_score'
    ]
    for key in metrics_keys:
        if key in st.session_state:
            del st.session_state[key]

def calculate_metrics(recommendation):
    """Calculate metrics based on the current recommendation."""
    if not recommendation or 'metrics' not in recommendation:
        return None
    
    metrics = recommendation['metrics']
    
    # Calculate overall score
    weights = {'security': 0.25, 'scalability': 0.25, 'energy_efficiency': 0.25, 'governance': 0.25}
    total_score = sum(metrics[key] * weight for key, weight in weights.items())
    
    return {
        'total_score': total_score,
        'security_score': metrics['security'],
        'scalability_score': metrics['scalability'],
        'energy_efficiency_score': metrics['energy_efficiency'],
        'governance_score': metrics['governance']
    }

def show_metrics():
    """Display metrics and analysis with enhanced visualization and state synchronization."""
    st.header("Métricas Técnicas e Análise")
    
    # Add reset button in metrics page
    if st.button("Reiniciar Métricas", help="Limpar todos os cálculos de métricas"):
        reset_metrics()
        st.experimental_rerun()
    
    if 'current_recommendation' in st.session_state:
        recommendation = st.session_state.current_recommendation
        if recommendation and recommendation['dlt'] != "Não disponível":
            metrics = calculate_metrics(recommendation)
            
            if metrics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Pontuações por Característica")
                    metrics_df = pd.DataFrame({
                        'Característica': ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
                        'Pontuação': [
                            metrics['security_score'],
                            metrics['scalability_score'],
                            metrics['energy_efficiency_score'],
                            metrics['governance_score']
                        ]
                    })
                    
                    fig = px.bar(metrics_df, x='Característica', y='Pontuação',
                               title="Análise de Características",
                               color='Pontuação',
                               color_continuous_scale='RdYlBu')
                    st.plotly_chart(fig)
                
                with col2:
                    st.subheader("Avaliação Global")
                    st.metric("Pontuação Total", f"{metrics['total_score']:.2f}")
                    
                    # Create radar chart
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=[metrics['security_score'], 
                           metrics['scalability_score'],
                           metrics['energy_efficiency_score'], 
                           metrics['governance_score']],
                        theta=['Segurança', 'Escalabilidade', 
                               'Eficiência Energética', 'Governança'],
                        fill='toself'
                    ))
                    
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                        showlegend=False,
                        title="Radar de Características"
                    )
                    
                    st.plotly_chart(fig)
                
                # Display evaluation matrix if available
                if 'evaluation_matrix' in recommendation:
                    st.subheader("Matriz de Avaliação")
                    matrix_data = []
                    for dlt, info in recommendation['evaluation_matrix'].items():
                        matrix_data.append({
                            'DLT': dlt,
                            'Tipo': info['type'],
                            'Estrutura': info['data_structure'],
                            'Grupo': info['group'],
                            'Score': info['score']
                        })
                    
                    matrix_df = pd.DataFrame(matrix_data)
                    st.dataframe(matrix_df)
    else:
        st.info("Complete o questionário para visualizar as métricas detalhadas.")
