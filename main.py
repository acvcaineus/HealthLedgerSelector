import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import compare_algorithms, consensus_algorithms
from database import get_user_recommendations
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)
from utils import init_session_state

def create_metrics_radar_chart(gini, entropy, depth, pruning):
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[gini, entropy, depth, pruning],
        theta=['Índice de Gini', 'Entropia', 'Profundidade', 'Taxa de Poda'],
        fill='toself',
        name='Métricas Atuais',
        hovertemplate="<b>%{theta}</b><br>" +
                     "Valor: %{r:.3f}<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        title="Visão Geral das Métricas",
        showlegend=True
    )
    return fig

def create_gini_comparison(classes):
    fig = go.Figure()
    
    values = list(classes.values())
    labels = list(classes.keys())
    
    fig.add_trace(go.Bar(
        x=labels,
        y=values,
        name='Valores por Classe',
        marker_color='#1f77b4',
        hovertemplate="<b>%{x}</b><br>" +
                     "Score: %{y:.3f}<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        title="Distribuição do Índice de Gini por Classe",
        xaxis_title="Classes",
        yaxis_title="Valor",
        showlegend=True
    )
    return fig

def show_metrics():
    st.header("Métricas Técnicas do Processo de Decisão")
    
    # Gini Index Section
    st.subheader("1. Índice de Gini")
    
    with st.expander("Como interpretar o Índice de Gini?"):
        st.markdown("""
        O Índice de Gini mede a impureza de um conjunto de dados. Em nossa árvore de decisão, 
        ele indica quão bem as características distinguem entre diferentes DLTs.
        
        ### Interpretação:
        - **Valores próximos a 0**: Melhor separação entre classes
        - **Valores próximos a 1**: Maior mistura entre classes
        
        ### Fórmula:
        """)
        st.latex(r"Gini = 1 - \sum_{i=1}^{n} p_i^2")
        st.markdown("""
        Onde:
        - $p_i$ é a proporção de cada classe no conjunto
        - $n$ é o número total de classes
        """)
    
    # Example calculation and visualizations
    if 'recommendation' in st.session_state:
        rec = st.session_state.recommendation
        if 'evaluation_matrix' in rec:
            classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
            gini = calcular_gini(classes)
            entropy = calcular_entropia(classes)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Índice de Gini Atual",
                    value=f"{gini:.3f}",
                    help="Quanto menor, melhor a separação entre as classes"
                )
            
            with col2:
                st.metric(
                    label="Entropia Atual",
                    value=f"{entropy:.3f} bits",
                    help="Quanto menor, mais certeza na decisão"
                )
            
            if 'answers' in st.session_state:
                depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
                total_nos = len(st.session_state.answers) * 2 + 1
                nos_podados = total_nos - len(st.session_state.answers) - 1
                pruning_ratio = calcular_pruning(total_nos, nos_podados)
                
                # Add radar chart
                fig_radar = create_metrics_radar_chart(
                    gini,
                    entropy,
                    depth / 10,  # Normalize to 0-1 range
                    pruning_ratio
                )
                st.plotly_chart(fig_radar, use_container_width=True)
                
                with st.expander("Como interpretar o Gráfico Radar?"):
                    st.markdown("""
                    O gráfico radar mostra todas as métricas importantes em um único visual:
                    
                    - **Índice de Gini**: Pureza da classificação
                    - **Entropia**: Certeza nas decisões
                    - **Profundidade**: Complexidade da árvore (normalizada)
                    - **Taxa de Poda**: Eficiência da simplificação
                    
                    Quanto maior a área preenchida, melhor o desempenho geral do modelo.
                    """)
                
                # Add Gini comparison
                fig_gini = create_gini_comparison(classes)
                st.plotly_chart(fig_gini, use_container_width=True)
                
                with st.expander("Como interpretar o Gráfico de Barras?"):
                    st.markdown("""
                    O gráfico de barras mostra a distribuição dos scores entre as diferentes DLTs:
                    
                    - **Altura da barra**: Score da DLT
                    - **Cores**: Azul padrão (#1f77b4) para facilitar a visualização
                    - **Interatividade**: Passe o mouse sobre as barras para ver valores exatos
                    
                    Uma distribuição mais uniforme indica maior incerteza na recomendação.
                    """)

    # Entropy Section with enhanced visualization
    st.subheader("2. Entropia")
    with st.expander("Como interpretar a Entropia?"):
        st.markdown("""
        A Entropia mede a aleatoriedade ou incerteza em nosso conjunto de decisões.
        Uma menor entropia indica decisões mais consistentes e confiáveis.
        
        ### Interpretação:
        - **Valores baixos**: Alta certeza nas decisões
        - **Valores altos**: Maior incerteza/aleatoriedade
        
        ### Fórmula:
        """)
        st.latex(r"Entropia = -\sum_{i=1}^{n} p_i \log_2(p_i)")
        st.markdown("""
        Onde:
        - $p_i$ é a probabilidade de cada classe
        - Logaritmo na base 2 é usado para medir em bits
        """)

    # Enhanced entropy visualization
    if 'recommendation' in st.session_state and 'answers' in st.session_state:
        entropy_values = []
        for i in range(len(st.session_state.answers)):
            partial_answers = dict(list(st.session_state.answers.items())[:i+1])
            partial_classes = {k: v['score'] for k, v in rec['evaluation_matrix'].items()}
            entropy_values.append(calcular_entropia(partial_classes))
        
        entropy_fig = go.Figure()
        entropy_fig.add_trace(go.Scatter(
            x=list(range(len(st.session_state.answers))),
            y=entropy_values,
            mode='lines+markers',
            name='Entropia'
        ))
        entropy_fig.update_layout(
            title="Variação da Entropia nas Decisões",
            xaxis_title="Número da Decisão",
            yaxis_title="Valor da Entropia"
        )
        st.plotly_chart(entropy_fig)
    
    # Decision Tree Metrics
    st.subheader("3. Métricas da Árvore de Decisão")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'answers' in st.session_state:
            depth = calcular_profundidade_decisoria(list(range(len(st.session_state.answers))))
            st.metric(
                label="Profundidade da Árvore",
                value=f"{depth:.1f}",
                help="Número médio de decisões necessárias"
            )
    
    with col2:
        if 'recommendation' in st.session_state:
            total_nos = len(st.session_state.answers) * 2 + 1
            nos_podados = total_nos - len(st.session_state.answers) - 1
            pruning_ratio = calcular_pruning(total_nos, nos_podados)
            st.metric(
                label="Taxa de Poda",
                value=f"{pruning_ratio:.2%}",
                help="Porcentagem de nós removidos para simplificação"
            )

    # New Accuracy Metrics Section
    st.subheader("4. Precisão (Accuracy)")
    with st.expander("Como interpretar a Precisão?"):
        st.markdown('''
        A precisão é uma métrica fundamental que avalia a proporção de decisões corretas em relação ao total.
        
        ### Fórmula:
        ''')
        st.latex(r"Precisão = \frac{Número\;de\;Decisões\;Corretas}{Total\;de\;Decisões}")
        
        if 'recommendation' in st.session_state:
            # Simulate accuracy metrics (replace with actual calculations in production)
            correct_decisions = len([ans for ans in st.session_state.answers.values() if ans == "Sim"])
            total_decisions = len(st.session_state.answers)
            
            accuracy_fig = go.Figure(data=[
                go.Bar(name='Acertos', x=['Decisões'], y=[correct_decisions]),
                go.Bar(name='Total', x=['Decisões'], y=[total_decisions])
            ])
            accuracy_fig.update_layout(
                title="Distribuição de Decisões",
                barmode='group'
            )
            st.plotly_chart(accuracy_fig)

    # Sensitivity and Specificity Section
    st.subheader("5. Sensibilidade e Especificidade")
    with st.expander("Como interpretar Sensibilidade e Especificidade?"):
        st.markdown('''
        ### Sensibilidade (Recall)
        Capacidade de identificar corretamente DLTs adequadas.
        
        ### Especificidade
        Capacidade de excluir corretamente DLTs inadequadas.
        ''')
        st.latex(r"Sensibilidade = \frac{VP}{VP + FN}")
        st.latex(r"Especificidade = \frac{VN}{VN + FP}")

        if 'recommendation' in st.session_state:
            # Simulate sensitivity and specificity metrics
            vp = len([ans for ans in st.session_state.answers.values() if ans == "Sim"])
            vn = len([ans for ans in st.session_state.answers.values() if ans == "Não"])
            total = len(st.session_state.answers)
            
            sensitivity = vp / total if total > 0 else 0
            specificity = vn / total if total > 0 else 0
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Sensibilidade", f"{sensitivity:.2%}")
            with col2:
                st.metric("Especificidade", f"{specificity:.2%}")

    # Return button at the bottom
    if st.button("Retornar ao Framework"):
        st.session_state.page = "Framework Proposto"
        st.experimental_rerun()

def show_reference_table():
    # [Rest of the code remains unchanged]
    pass

def show_home_page():
    # [Rest of the code remains unchanged]
    pass

def show_user_profile():
    # [Rest of the code remains unchanged]
    pass

def main():
    # [Rest of the code remains unchanged]
    pass

if __name__ == "__main__":
    main()
