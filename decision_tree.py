import streamlit as st
import plotly.graph_objects as go
from decision_logic import get_recommendation, consensus_algorithms
from database import save_recommendation

def create_evaluation_matrices(recommendation):
    if not recommendation or 'evaluation_matrix' not in recommendation:
        return
        
    st.subheader("Matriz de Avaliação Detalhada")
    
    # Create DLT comparison heatmap for raw scores
    st.subheader("Comparação de Métricas Brutas das DLTs")
    metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
    dlts = list(recommendation['evaluation_matrix'].keys())
    
    # Prepare data for raw metrics heatmap
    raw_values = []
    for metric in metrics:
        row = []
        for dlt in dlts:
            raw_score = recommendation['evaluation_matrix'][dlt]['raw_metrics'][metric]
            row.append(raw_score)
        raw_values.append(row)
    
    # Create raw metrics heatmap
    fig_raw = go.Figure(data=go.Heatmap(
        z=raw_values,
        x=dlts,
        y=['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança'],
        colorscale='RdBu',
        hoverongaps=False,
        hovertemplate="<b>DLT:</b> %{x}<br>" +
                     "<b>Métrica:</b> %{y}<br>" +
                     "<b>Valor:</b> %{z:.2f}<br>" +
                     "<extra></extra>"
    ))
    
    fig_raw.update_layout(
        title="Valores Brutos das Métricas",
        xaxis_title="DLTs",
        yaxis_title="Métricas",
        height=400
    )
    
    st.plotly_chart(fig_raw, use_container_width=True)
    
    # Create DLT comparison heatmap for weighted scores
    st.subheader("Comparação de Métricas Ponderadas das DLTs")
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
                     "<b>Tipo:</b> " + "<br>".join(dlt_types) + "<br>" +
                     "<b>Métrica:</b> %{y}<br>" +
                     "<b>Score Ponderado:</b> %{z:.2f}<br>" +
                     "<extra></extra>"
    ))
    
    fig_weighted.update_layout(
        title="Scores Ponderados por Tipo de DLT",
        xaxis_title="DLTs",
        yaxis_title="Métricas",
        height=400
    )
    
    st.plotly_chart(fig_weighted, use_container_width=True)
    
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
    
    # Add explanation of weighting process
    with st.expander("ℹ️ Como os Scores são Calculados"):
        st.markdown("""
        ### Processo de Ponderação Dinâmica
        
        Os scores são calculados usando um sistema de pesos dinâmicos baseados no tipo de DLT:
        
        1. **DLT Permissionada Privada**: 
           - Segurança (35%)
           - Escalabilidade (20%)
           - Eficiência Energética (20%)
           - Governança (25%)
        
        2. **DLT Permissionada Simples**:
           - Segurança (30%)
           - Escalabilidade (25%)
           - Eficiência Energética (25%)
           - Governança (20%)
        
        3. **DLT Híbrida**:
           - Segurança (25%)
           - Escalabilidade (30%)
           - Eficiência Energética (25%)
           - Governança (20%)
        
        4. **DLT com Consenso Delegado**:
           - Segurança (25%)
           - Escalabilidade (35%)
           - Eficiência Energética (25%)
           - Governança (15%)
        
        5. **DLT Pública**:
           - Segurança (40%)
           - Escalabilidade (20%)
           - Eficiência Energética (15%)
           - Governança (25%)
        
        6. **DLT Pública Permissionless**:
           - Segurança (30%)
           - Escalabilidade (30%)
           - Eficiência Energética (20%)
           - Governança (20%)
        """)

def run_decision_tree():
    """Main function to run the decision tree interface."""
    st.title("Framework de Seleção de DLT")
    
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    # Add reset button
    if st.button("🔄 Reiniciar", help="Clique para recomeçar o processo de seleção"):
        st.session_state.answers = {}
        st.experimental_rerun()
    
    # Display current progress
    progress = len(st.session_state.answers) / len(questions)
    st.progress(progress)
    
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
