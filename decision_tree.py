import streamlit as st
import plotly.graph_objects as go
import math
from decision_logic import get_recommendation, consensus_algorithms, consensus_groups, compare_algorithms
from database import save_recommendation
import networkx as nx
from metrics import (calcular_gini, calcular_entropia, calcular_profundidade_decisoria, 
                    calcular_pruning, calcular_confiabilidade_recomendacao)

def create_progress_animation(current_phase, answers, questions):
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

def show_recommendation(answers, weights, questions):
    recommendation = get_recommendation(answers, weights)
    
    st.header("Recomendação de DLT")
    st.write(f"DLT Recomendada: **{recommendation['dlt']}**")
    
    # Save button in a container with custom styling
    save_container = st.container()
    with save_container:
        if st.session_state.get('authenticated', False):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(
                    "💾 Salvar Recomendação",
                    help="Clique para salvar esta recomendação no seu perfil",
                    key="save_recommendation",
                    type="primary",  # Makes the button more prominent
                    use_container_width=True  # Makes the button wider
                ):
                    save_recommendation(
                        st.session_state.username,
                        "Healthcare",
                        recommendation
                    )
                    st.success("✅ Recomendação salva com sucesso! Você pode acessá-la no seu perfil.")
        else:
            st.warning("⚠️ Faça login para salvar recomendações e acessá-las posteriormente.")
    
    st.markdown("---")  # Visual separator
    
    st.subheader("Algoritmo de Consenso")
    st.write(f"Grupo de Consenso: {recommendation.get('consensus_group', 'Não disponível')}")
    st.write(f"Algoritmo: {recommendation.get('consensus', 'Não disponível')}")
    st.write(f"Descrição: {recommendation.get('group_description', '')}")
    
    st.subheader("Matriz de Avaliação de DLTs")
    with st.expander("Ver Matriz de Avaliação de DLTs"):
        evaluation_matrix = recommendation.get('evaluation_matrix', {})
        dlt_scores = {
            metric: [float(data['metrics'][metric]) for data in evaluation_matrix.values()]
            for metric in ['security', 'scalability', 'energy_efficiency', 'governance']
        }
        
        fig_dlt = go.Figure(data=go.Heatmap(
            z=list(dlt_scores.values()),
            x=list(evaluation_matrix.keys()),
            y=list(dlt_scores.keys()),
            colorscale='Viridis',
            hoverongaps=False,
            hovertemplate="<b>DLT:</b> %{x}<br>" +
                         "<b>Métrica:</b> %{y}<br>" +
                         "<b>Score:</b> %{z:.2f}<br>" +
                         "<extra></extra>"
        ))
        st.plotly_chart(fig_dlt, use_container_width=True)
        st.markdown('''
        ### Como interpretar a Matriz de DLTs:
        - Cores mais escuras indicam scores mais altos
        - Cada linha representa uma métrica diferente
        - Cada coluna representa uma DLT
        - Passe o mouse sobre os quadrados para ver os valores exatos
        ''')

    st.subheader("Matriz de Avaliação dos Grupos de Algoritmos")
    with st.expander("Ver Matriz de Avaliação dos Grupos"):
        group_data = {
            group: data['characteristics']
            for group, data in consensus_groups.items()
        }
        
        fig_groups = go.Figure(data=go.Heatmap(
            z=[[float(v) for v in group.values()] for group in group_data.values()],
            x=list(next(iter(group_data.values())).keys()),
            y=list(group_data.keys()),
            colorscale='Viridis',
            hovertemplate="<b>Grupo:</b> %{y}<br>" +
                         "<b>Métrica:</b> %{x}<br>" +
                         "<b>Score:</b> %{z:.2f}<br>" +
                         "<extra></extra>"
        ))
        st.plotly_chart(fig_groups, use_container_width=True)
        st.markdown('''
        ### Como interpretar a Matriz de Grupos:
        - Cada linha representa um grupo de algoritmos
        - Cada coluna representa uma característica
        - A intensidade da cor indica o score
        - Os valores são baseados em pesquisas acadêmicas
        ''')

    if 'consensus_group' in recommendation:
        st.subheader("Matriz de Avaliação dos Algoritmos de Consenso")
        with st.expander("Ver Matriz de Avaliação dos Algoritmos"):
            recommended_group = recommendation['consensus_group']
            algorithms = consensus_groups[recommended_group]['algorithms']
            
            algo_data = {
                algo: consensus_algorithms[algo]
                for algo in algorithms if algo in consensus_algorithms
            }
            
            fig_algo = go.Figure(data=go.Heatmap(
                z=[[float(v) for v in algo.values()] for algo in algo_data.values()],
                x=list(next(iter(algo_data.values())).keys()),
                y=list(algo_data.keys()),
                colorscale='Viridis',
                hovertemplate="<b>Algoritmo:</b> %{y}<br>" +
                             "<b>Métrica:</b> %{x}<br>" +
                             "<b>Score:</b> %{z:.2f}<br>" +
                             "<extra></extra>"
            ))
            st.plotly_chart(fig_algo, use_container_width=True)
            st.markdown(f'''
            ### Como interpretar a Matriz de Algoritmos:
            - Mostra os algoritmos do grupo {recommended_group}
            - Cada linha é um algoritmo específico
            - Cada coluna é uma característica
            - Os scores são baseados em validação acadêmica
            ''')

    if 'confidence_value' in recommendation:
        st.subheader("Métricas de Confiança")
        with st.expander("Ver Métricas de Confiança"):
            conf_val = float(recommendation['confidence_value'])
            st.metric(
                "Índice de Confiança",
                f"{conf_val:.2%}",
                help="Quanto maior, mais confiável é a recomendação"
            )
            st.progress(conf_val)
            
            st.markdown(f'''
            ### Interpretação do Índice de Confiança:
            - Abaixo de 60%: Baixa confiança
            - Entre 60% e 80%: Confiança moderada
            - Acima de 80%: Alta confiança
            
            Valor atual: {conf_val:.2%} - {'Alta' if conf_val > 0.8 else 'Moderada' if conf_val > 0.6 else 'Baixa'} confiança
            ''')
            
            st.markdown('''
            ### Como melhorar a confiança da recomendação:
            
            1. **Consistência nas Respostas**
            - Verifique se suas respostas são consistentes com o caso de uso
            - Revise respostas que parecem contraditórias
            
            2. **Características Priorizadas**
            - Certifique-se de que as características mais importantes têm peso adequado
            - Ajuste os pesos se necessário
            
            3. **Alinhamento com Requisitos**
            - Verifique se a DLT recomendada atende todos os requisitos críticos
            - Considere requisitos não funcionais
            
            4. **Validação Acadêmica**
            - Considere a pontuação de validação acadêmica
            - Verifique casos de uso similares
            ''')
            
            if 'confidence_components' in recommendation:
                components = recommendation['confidence_components']
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(components.keys()),
                        y=list(components.values()),
                        text=[f'{v:.1%}' for v in components.values()],
                        textposition='auto',
                    )
                ])
                fig.update_layout(
                    title="Componentes do Índice de Confiança",
                    xaxis_title="Componente",
                    yaxis_title="Contribuição",
                    yaxis=dict(range=[0, 1])
                )
                st.plotly_chart(fig, use_container_width=True)

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
        st.session_state.recommendation = show_recommendation(st.session_state.answers, weights, questions)
