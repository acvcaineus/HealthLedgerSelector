import streamlit as st
import graphviz as gv
import plotly.graph_objects as go
from database import save_recommendation
from decision_logic import get_recommendation
from dlt_data import consensus_algorithms

def get_questions():
    return {
        'Aplicação': [
            "A aplicação exige alta privacidade e controle centralizado?",
            "A aplicação precisa de alta escalabilidade e eficiência energética?"
        ],
        'Consenso': [
            "A rede exige alta resiliência contra ataques e falhas bizantinas?",
            "A eficiência energética é um fator crucial para a rede?"
        ],
        'Infraestrutura': [
            "A rede precisa integrar-se a sistemas legados de saúde (ex: EHRs, bancos de dados hospitalares)?",
            "A infraestrutura precisa lidar com grandes volumes de dados ou dispositivos IoT?"
        ],
        'Internet': [
            "A rede precisa de governança centralizada?",
            "A validação de consenso deve ser delegada a um subconjunto de validadores (DPoS)?"
        ]
    }

def init_session_state():
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 0
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.recommendation = None

def show_interactive_decision_tree():
    st.header('Framework Proposto para Contextos de Saúde')

    init_session_state()

    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    questions = get_questions()

    if st.session_state.current_phase >= len(phases):
        st.write("Todas as fases foram completadas!")
        show_recommendation(st.session_state.answers)
        return

    current_phase = phases[st.session_state.current_phase]
    current_question = questions[current_phase][st.session_state.current_question]

    st.subheader(f'Fase {st.session_state.current_phase + 1}: {current_phase}')
    answer = st.radio(current_question, ['Sim', 'Não'], key=f'question_{st.session_state.current_phase}_{st.session_state.current_question}')

    if st.button('Próxima Pergunta', key=f'button_{st.session_state.current_phase}_{st.session_state.current_question}'):
        st.session_state.answers[f'{current_phase}_{st.session_state.current_question}'] = answer

        if st.session_state.current_question < len(questions[current_phase]) - 1:
            st.session_state.current_question += 1
        else:
            st.session_state.current_question = 0
            st.session_state.current_phase += 1

        if st.session_state.current_phase >= len(phases):
            st.session_state.recommendation = show_recommendation(st.session_state.answers)
        else:
            st.rerun()

    total_questions = sum(len(q) for q in questions.values())
    current_question_overall = sum(len(questions[p]) for p in phases[:st.session_state.current_phase]) + st.session_state.current_question
    st.progress(current_question_overall / total_questions)

    st.write(f'Fase atual: {st.session_state.current_phase + 1}/{len(phases)}')
    st.write(f'Pergunta atual: {st.session_state.current_question + 1}/{len(questions[current_phase])}')

def show_recommendation(answers):
    st.subheader('Recomendação Final:')

    weights = {
        "security": 0.4,
        "scalability": 0.3,
        "energy_efficiency": 0.2,
        "governance": 0.1
    }

    recommendation = get_recommendation(answers, weights)
    st.session_state.recommendation = recommendation
    
    st.write(f"**DLT Recomendada**: {recommendation['dlt']}")
    st.write(f"**Grupo de Consenso**: {recommendation['consensus_group']}")
    st.write(f"**Algoritmo de Consenso Recomendado**: {recommendation['consensus']}")

    # New section for application scenarios
    st.subheader("Cenários de Aplicação Recomendados")
    st.write("Para o seu caso de uso, considerando as respostas fornecidas, recomendamos:")

    # Mapping DLT types to scenarios and use cases
    dlt_scenarios = {
        "DLT Permissionada Privada": {
            "descricao": "Alta segurança e resiliência contra falhas bizantinas. Máxima proteção de dados sensíveis em redes permissionadas e descentralizadas.",
            "casos_uso": ["Prontuários eletrônicos", "Integração de dados sensíveis", "Sistemas de pagamento descentralizados"],
            "exemplos": "Hyperledger Fabric implementado em sistemas hospitalares para gerenciamento de registros médicos.",
            "referencia": "Mehmood et al. (2025) - BLPCA-ledger"
        },
        "DLT Pública Permissionless": {
            "descricao": "Máxima segurança e descentralização para redes públicas, garantindo proteção de dados críticos de saúde pública.",
            "casos_uso": ["Sistemas de pagamento descentralizados", "Dados críticos de saúde pública"],
            "exemplos": "Bitcoin e Ethereum para armazenamento seguro de dados médicos críticos.",
            "referencia": "Liu et al. (2024) - Blockchain in healthcare for EHR management"
        },
        "DLT Permissionada Simples": {
            "descricao": "Simplicidade e eficiência em redes permissionadas menores. Validação rápida e leve, ideal para redes locais.",
            "casos_uso": ["Sistemas locais de saúde", "Agendamento de pacientes", "Redes locais de hospitais"],
            "exemplos": "Quorum e VeChain para rastreamento de suprimentos médicos.",
            "referencia": "Popoola et al. (2024) - Security and privacy in smart home healthcare"
        },
        "DLT Híbrida": {
            "descricao": "Alta escalabilidade e eficiência energética com governança descentralizada ou semi-descentralizada.",
            "casos_uso": ["Monitoramento de saúde pública", "Redes regionais de saúde", "Integração de EHRs"],
            "exemplos": "Ethereum 2.0 para aceleração de ensaios clínicos e compartilhamento de dados.",
            "referencia": "Nawaz et al. (2024) - Supply chain traceability system"
        },
        "DLT com Consenso Delegado": {
            "descricao": "Alta escalabilidade e eficiência energética com governança descentralizada ou semi-descentralizada.",
            "casos_uso": ["Monitoramento de saúde pública", "Redes regionais de saúde", "Integração de EHRs"],
            "exemplos": "EOS para monitoramento de saúde pública e integração de dados.",
            "referencia": "Javed et al. (2024) - Trust model for healthcare systems"
        },
        "DLT Pública": {
            "descricao": "Alta escalabilidade e eficiência para o monitoramento de dispositivos IoT em tempo real.",
            "casos_uso": ["Monitoramento de dispositivos IoT em saúde", "Dados em tempo real"],
            "exemplos": "IOTA para compartilhamento seguro de dados de pacientes via IoT.",
            "referencia": "Salim et al. (2024) - Privacy-preserving blockchain for healthcare"
        }
    }

    recommended_scenario = dlt_scenarios.get(recommendation['dlt'], {})
    with st.expander("Ver Detalhes do Cenário Recomendado"):
        st.write("### Descrição do Cenário")
        st.write(recommended_scenario.get("descricao", "Descrição não disponível"))
        
        st.write("### Casos de Uso Típicos")
        for caso in recommended_scenario.get("casos_uso", []):
            st.write(f"- {caso}")
        
        st.write("### Exemplos de Implementação")
        st.write(recommended_scenario.get("exemplos", "Exemplos não disponíveis"))
        
        st.write("### Justificativa da Escolha")
        st.write("Com base nas suas respostas e nos pesos atribuídos:")
        st.write(f"- Segurança ({weights['security']*100}%)")
        st.write(f"- Escalabilidade ({weights['scalability']*100}%)")
        st.write(f"- Eficiência Energética ({weights['energy_efficiency']*100}%)")
        st.write(f"- Governança ({weights['governance']*100}%)")
        st.write(f"\nReferência: {recommended_scenario.get('referencia', 'Não disponível')}")

    with st.expander("Ver Outros Cenários para Comparação"):
        for dlt_type, scenario in dlt_scenarios.items():
            if dlt_type != recommendation['dlt']:
                st.write(f"### {dlt_type}")
                st.write(scenario['descricao'])
                st.write("**Casos de Uso:**")
                for caso in scenario['casos_uso']:
                    st.write(f"- {caso}")

    st.subheader("Matriz de Avaliação")
    evaluation_matrix = recommendation['evaluation_matrix']
    scores = {dlt: data["score"] for dlt, data in evaluation_matrix.items()}
    fig = go.Figure(data=[go.Bar(x=list(scores.keys()), y=list(scores.values()))])
    fig.update_layout(title="Pontuação das DLTs", xaxis_title="DLTs", yaxis_title="Pontuação")
    st.plotly_chart(fig)

    if 'academic_validation' in recommendation:
        st.subheader("Validação Acadêmica")
        academic_data = recommendation['academic_validation']
        if academic_data:
            st.write(f"**Score Acadêmico**: {academic_data.get('score', 'N/A')}/5")
            st.write(f"**Citações**: {academic_data.get('citations', 'N/A')}")
            st.write(f"**Referência**: {academic_data.get('reference', 'N/A')}")
            st.write(f"**Validação**: {academic_data.get('validation', 'N/A')}")

    st.subheader("Pontuações dos Algoritmos de Consenso")
    if 'algorithms' in recommendation:
        consensus_scores = {alg: sum(float(value) for value in consensus_algorithms[alg].values()) for alg in recommendation['algorithms']}
        fig = go.Figure(data=[go.Bar(x=list(consensus_scores.keys()), y=list(consensus_scores.values()))])
        fig.update_layout(title="Pontuação dos Algoritmos de Consenso", xaxis_title="Algoritmos", yaxis_title="Pontuação")
        st.plotly_chart(fig)

    with st.expander("Ver Respostas Acumuladas"):
        st.json(answers)

    if st.button("Salvar Recomendação"):
        scenario = "Cenário Geral"
        save_recommendation(st.session_state.username, scenario, recommendation)
        st.success("Recomendação salva com sucesso no seu perfil!")

    st.button("Comparar Algoritmos", on_click=lambda: setattr(st.session_state, 'page', 'Comparação de Recomendações'))

    return recommendation

def restart_decision_tree():
    if st.button("Reiniciar"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def run_decision_tree():
    show_interactive_decision_tree()
    st.markdown("---")
    restart_decision_tree()
