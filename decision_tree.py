import streamlit as st
import graphviz as gv

# Função para retornar as perguntas por fase
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

# Função para inicializar o estado da sessão
def init_session_state():
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 0
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.recommendation = None  # Armazena a recomendação final

# Função para visualizar as métricas de Decision Tree
def show_decision_tree_metrics():
    st.subheader("Métricas da Árvore de Decisão")
    st.write("""
    **Impureza de Gini**: Mede a impureza ou diversidade dos nós da árvore.
    - Fórmula: Gini(t) = 1 - Σ(pi^2)
    - 0.0: Puro, 1.0: Máxima impureza.

    **Entropia**: Quantifica a desordem ou incerteza.
    - Fórmula: Entropia(t) = -Σ(pi * log2(pi))

    **Profundidade Decisória**: Mede o número de divisões feitas para chegar à decisão final.
    - Baixa: Menor que 3, Média: 3-6, Alta: Mais de 6.

    **Pruning (Poda)**: Processo de simplificação da árvore para evitar overfitting.
    - Redução de nós sem perda de precisão.
    """)

# Função para exibir a árvore de decisão interativa
def show_interactive_decision_tree():
    st.header('Árvore de Decisão Interativa para Contextos de Saúde')

    # Inicializa o estado de sessão, se necessário
    init_session_state()

    # Definir fases e perguntas
    phases = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    questions = get_questions()

    # Garante que o current_phase não ultrapasse o limite das fases
    if st.session_state.current_phase >= len(phases):
        st.write("Todas as fases foram completadas!")
        show_recommendation(st.session_state.answers)  # Mostra a recomendação final
        return  # Sai da função para não tentar acessar um índice fora da lista

    # Pega a fase e pergunta atuais
    current_phase = phases[st.session_state.current_phase]
    current_question = questions[current_phase][st.session_state.current_question]

    # Exibe a pergunta atual
    st.subheader(f'Fase {st.session_state.current_phase + 1}: {current_phase}')
    answer = st.radio(current_question, ['Sim', 'Não'], key=f'question_{st.session_state.current_phase}_{st.session_state.current_question}')

    # Botão para avançar para a próxima pergunta
    if st.button('Próxima Pergunta', key=f'button_{st.session_state.current_phase}_{st.session_state.current_question}'):
        # Armazena a resposta
        st.session_state.answers[f'{current_phase}_{st.session_state.current_question}'] = answer

        # Verifica se ainda há perguntas na fase atual
        if st.session_state.current_question < len(questions[current_phase]) - 1:
            st.session_state.current_question += 1  # Avança para a próxima pergunta
        else:
            # Se todas as perguntas da fase atual foram respondidas, avança para a próxima fase
            st.session_state.current_question = 0
            st.session_state.current_phase += 1

        # Verifica se todas as fases foram completadas
        if st.session_state.current_phase >= len(phases):
            st.session_state.recommendation = show_recommendation(st.session_state.answers)  # Mostra a recomendação final
        else:
            st.experimental_rerun()  # Recarrega a página para mostrar a próxima pergunta

    # Progresso geral
    total_questions = sum(len(q) for q in questions.values())
    current_question_overall = sum(len(questions[p]) for p in phases[:st.session_state.current_phase]) + st.session_state.current_question
    st.progress(current_question_overall / total_questions)

    # Exibe progresso e debug
    st.write(f'Fase atual: {st.session_state.current_phase + 1}/{len(phases)}')
    st.write(f'Pergunta atual: {st.session_state.current_question + 1}/{len(questions[current_phase])}')
    st.write('Debug - Respostas atuais:', st.session_state.answers)

    # Visualização do fluxo de decisão
    st.subheader("Fluxo de Decisão")
    decision_flow = gv.Digraph(format="png")
    decision_flow.node("Início", "Início")
    for phase_key, question_key in st.session_state.answers.items():
        decision_flow.node(f"{phase_key}", f"{phase_key} - {question_key}")
        decision_flow.edge("Início", f"{phase_key}")
    st.graphviz_chart(decision_flow)

# Função para exibir a recomendação final baseada em todas as respostas
def show_recommendation(answers):
    st.subheader('Recomendação Final:')

    # Inicializando valores padrão
    dlt = "DLT Pública"
    consensus = "DPoS"
    explanation = "Com base nas respostas, a DLT pública com Delegated Proof of Stake é a recomendação mais adequada."

    # Analisando respostas da fase "Aplicação"
    if answers.get("Aplicação_0") == "Sim":
        dlt = "DLT Permissionada Privada"
        consensus = "PBFT"
        explanation = "A aplicação exige alta privacidade e controle centralizado. A DLT Permissionada Privada com PBFT é adequada para garantir segurança e controle."
    elif answers.get("Aplicação_1") == "Sim":
        dlt = "DLT Pública ou Híbrida"
        consensus = "PoS"
        explanation = "A aplicação precisa de alta escalabilidade e eficiência energética. A DLT Pública ou Híbrida com PoS é adequada para esses requisitos."

    # Outras fases seguem o mesmo padrão...

    # Exibe a recomendação com base nas respostas
    st.write(f"**DLT Recomendada**: {dlt}")
    st.write(f"**Algoritmo de Consenso Recomendado**: {consensus}")
    st.write(f"**Explicação**: {explanation}")

    # Exibir todas as respostas acumuladas para transparência
    st.write("**Respostas acumuladas**:")
    st.json(answers)

    # Botão para salvar a recomendação
    if st.button("Salvar Recomendação"):
        with open("recomendacao.txt", "w") as f:
            f.write(f"DLT Recomendada: {dlt}\n")
            f.write(f"Algoritmo de Consenso Recomendado: {consensus}\n")
            f.write(f"Explicação: {explanation}\n")
        st.success("Recomendação salva com sucesso!")

# Função para reiniciar a árvore de decisão
def restart_decision_tree():
    if st.button("Reiniciar"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()

# Função principal para rodar a árvore de decisão
def run_decision_tree():
    show_interactive_decision_tree()
    st.markdown("---")
    show_decision_tree_metrics()  # Botão para visualizar métricas
    restart_decision_tree()  # Botão para reiniciar
