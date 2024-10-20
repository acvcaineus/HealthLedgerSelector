import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from user_management import login, register, is_authenticated, logout
from database import get_user_recommendations, save_recommendation, save_feedback
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm, get_scenario_pros_cons
from dlt_data import scenarios, questions, dlt_classes, consensus_algorithms
from utils import init_session_state

def generate_decision_tree():
    G = nx.DiGraph()
    
    shermin_layers = ['Aplicação', 'Consenso', 'Infraestrutura', 'Internet']
    layer_positions = {layer: i for i, layer in enumerate(shermin_layers)}
    
    for question in st.session_state.answers:
        question_data = next(q for q in questions[st.session_state.scenario] if q['id'] == question)
        answer = st.session_state.answers[question]
        
        G.add_node(question, label=question_data['text'], color='lightblue', 
                   pos=(layer_positions[question_data['shermin_layer']], 0),
                   shermin_layer=question_data['shermin_layer'], 
                   main_characteristic=question_data['main_characteristic'])
        
        answer_node = f"{question}_{answer}"
        G.add_node(answer_node, label=answer, color='green' if answer == 'Sim' else 'red',
                   pos=(layer_positions[question_data['shermin_layer']], 1),
                   shape='box')
        
        G.add_edge(question, answer_node)
        
        next_layer = question_data['next_layer'][answer]
        next_questions = [q for q in questions[st.session_state.scenario] if q['shermin_layer'] == next_layer]
        if next_questions:
            next_question = next_questions[0]['id']
            G.add_edge(answer_node, next_question, color='gray', style='dashed')
    
    return G

def show_decision_tree():
    st.subheader("Árvore de Decisão")
    
    G = generate_decision_tree()
    
    net = Network(height="500px", width="100%", directed=True)
    net.from_nx(G)
    
    for node in net.nodes:
        if 'shape' in node:
            node['shape'] = node['shape']
        if 'pos' in node:
            node['x'], node['y'] = node['pos']
        if 'shermin_layer' in node:
            node['title'] = f"Camada Shermin: {node['shermin_layer']}<br>Característica Principal: {node['main_characteristic']}"
    
    html = net.generate_html()
    components.html(html, height=600)
    
    st.write("**Legenda:**")
    st.write("- Círculos azuis: Perguntas (Passe o mouse para ver a camada Shermin e característica principal)")
    st.write("- Quadrados verdes: Respostas 'Sim'")
    st.write("- Quadrados vermelhos: Respostas 'Não'")
    st.write("- Setas pontilhadas: Fluxo para a próxima pergunta")

def show_feedback_form():
    st.header("Feedback")
    st.write("Por favor, forneça seu feedback sobre a recomendação:")

    col1, col2 = st.columns(2)
    with col1:
        rating = st.slider("Avalie a qualidade da recomendação:", 1, 5, 3)
    with col2:
        usefulness = st.selectbox("Quão útil foi esta recomendação?", 
                                  ["Muito útil", "Útil", "Neutro", "Pouco útil", "Nada útil"])

    feedback_text = st.text_area("Seus comentários:", max_chars=500, 
                                 help="Por favor, forneça detalhes sobre o que você achou da recomendação.")
    
    specific_feedback = st.multiselect("Selecione os aspectos que você gostaria de comentar:",
                                       ["Clareza da explicação", "Relevância para o cenário", 
                                        "Comparação com outras soluções", "Facilidade de implementação"])

    if st.button("Enviar Feedback"):
        if feedback_text.strip() == "":
            st.warning("Por favor, escreva um comentário antes de enviar o feedback.")
        else:
            feedback_data = {
                "rating": rating,
                "usefulness": usefulness,
                "comment": feedback_text,
                "specific_aspects": specific_feedback
            }
            save_feedback(st.session_state.username, st.session_state.scenario, st.session_state.recommendation['dlt'], st.session_state.recommendation['consensus_group'], feedback_data)
            st.success("Obrigado pelo seu feedback! Sua opinião é muito importante para nós.")
            st.balloons()

def show_scenario_selection(dlt, consensus_algorithm):
    st.header("Escolha um Cenário de Aplicação")
    scenario = st.selectbox("Selecione um cenário", list(scenarios.keys()))

    st.write(f"**Descrição do cenário:** {scenarios[scenario]}")

    st.subheader("Vantagens e Desvantagens da Implementação")
    advantages, disadvantages, algorithm_applicability = get_scenario_pros_cons(scenario, dlt, consensus_algorithm)
    
    st.write("**Vantagens:**")
    for adv in advantages:
        st.write(f"- {adv}")
    
    st.write("**Desvantagens:**")
    for disadv in disadvantages:
        st.write(f"- {disadv}")
    
    st.write("**Aplicabilidade do Algoritmo Recomendado:**")
    st.write(algorithm_applicability)

    if st.button("Finalizar"):
        st.session_state.scenario = scenario
        save_recommendation(st.session_state.username, scenario, st.session_state.recommendation)
        st.success("Recomendação salva com sucesso!")

def show_correlation_table():
    st.subheader("Correlação entre DLT, Grupos de Algoritmos e Algoritmos Específicos")
    data = {
        'DLT': ['Public Blockchain', 'Permissioned Blockchain', 'Private Blockchain', 'Hybrid Blockchain', 'Distributed Ledger'],
        'Grupo de Algoritmos': ['Públicos', 'Permissionados', 'Permissionados', 'Híbridos', 'Distribuídos'],
        'Algoritmos Específicos': ['PoW, PoS, DPoS', 'PBFT, PoA, Raft', 'PBFT, PoA, Raft', 'PoS, PBFT', 'DAG, Tangle']
    }
    df = pd.DataFrame(data)
    st.table(df)

def show_questionnaire():
    st.header("Questionário")
    scenario = "Registros Médicos Eletrônicos (EMR)"
    scenario_questions = questions[scenario]
    question_order = ['privacy', 'integration', 'data_volume', 'energy_efficiency', 'network_security', 'scalability', 'governance_flexibility', 'interoperability']

    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0

    if st.session_state.question_index < len(question_order):
        current_question = next(q for q in scenario_questions if q['id'] == question_order[st.session_state.question_index])

        st.subheader(f"Pergunta {st.session_state.question_index + 1} - Camada {current_question['shermin_layer']}")
        st.write(current_question['text'])

        st.info(f"Camada Shermin: {current_question['shermin_layer']}")
        st.write(f"Características consideradas: {', '.join(current_question['characteristics'])}")

        answer = st.radio("Selecione uma opção:", current_question['options'])

        if st.button("Próximo"):
            st.session_state.answers[current_question['id']] = answer
            st.session_state.question_index += 1

            if st.session_state.question_index == len(question_order):
                st.session_state.page = "prioritize_characteristics"
            st.rerun()

        progress = (st.session_state.question_index + 1) / len(question_order)
        st.progress(progress)
        st.write(f"Progresso: Pergunta {st.session_state.question_index + 1} de {len(question_order)}")
    else:
        st.session_state.page = "prioritize_characteristics"
        st.rerun()

def show_prioritize_characteristics():
    st.header('Priorize as Características')
    st.write('Distribua 100 pontos entre as seguintes características de acordo com sua importância para o seu projeto:')

    total_points = 100
    remaining_points = total_points

    characteristics = ['Segurança', 'Escalabilidade', 'Eficiência Energética', 'Governança']
    weights = {}

    col1, col2 = st.columns(2)

    for i, char in enumerate(characteristics):
        with col1 if i % 2 == 0 else col2:
            if remaining_points > 0:
                weights[char.lower()] = st.slider(f'{char} ({remaining_points} pontos restantes)', 
                                                  min_value=0, 
                                                  max_value=remaining_points, 
                                                  value=min(25, remaining_points),
                                                  key=f'weight_{char.lower()}')
                remaining_points -= weights[char.lower()]
            else:
                st.write(f'{char}: 0 pontos')
                weights[char.lower()] = 0

    if remaining_points == 0:
        if st.button('Finalizar e Obter Recomendação'):
            st.session_state.weights = {
                'segurança': weights['segurança'],
                'escalabilidade': weights['escalabilidade'],
                'eficiência energética': weights['eficiência energética'],
                'governança': weights['governança']
            }
            recommendation = get_recommendation(st.session_state.answers, st.session_state.weights)
            st.session_state.recommendation = recommendation
            st.session_state.page = 'recommendation'
            st.rerun()
    else:
        st.warning(f'Por favor, distribua todos os {remaining_points} pontos restantes antes de prosseguir.')

def show_recommendation():
    if 'recommendation' not in st.session_state:
        st.error("Por favor, complete o questionário primeiro para receber uma recomendação.")
        return

    recommendation = st.session_state.recommendation
    st.header("Recomendação")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Framework DLT")
        st.info(recommendation['dlt'])
    with col2:
        st.subheader("Grupo de Algoritmos de Consenso")
        st.info(recommendation['consensus_group'])

    with st.expander("Explicação Detalhada"):
        st.markdown(f'''
        **DLT Recomendada:** {recommendation['dlt']}
        {dlt_classes[recommendation['dlt']]}

        **Grupo de Algoritmos de Consenso Recomendado:** {recommendation['consensus_group']}
        ''')

    show_decision_tree()

    st.subheader("Comparação de Algoritmos de Consenso no Grupo")
    comparison_data = compare_algorithms(recommendation['consensus_group'])
    
    df = pd.DataFrame(comparison_data)
    st.table(df)

    st.subheader("Ajuste Fino das Prioridades")
    characteristics = ["Segurança", "Escalabilidade", "Eficiência Energética", "Governança"]
    priorities = {}
    for char in characteristics:
        priorities[char] = st.slider(f"Prioridade para {char}", 1, 10, 5)

    final_algorithm = select_final_algorithm(recommendation['consensus_group'], priorities)
    st.success(f"O algoritmo final recomendado é: {final_algorithm}")

    show_scenario_selection(recommendation['dlt'], final_algorithm)

    st.subheader("Influência das Características na Decisão")
    fig = px.bar(df, x=df.index, y=df.columns, title="Comparação de Características")
    st.plotly_chart(fig)

    show_feedback_form()

def show_home_page():
    st.header("Bem-vindo ao SeletorDLTSaude")
    st.write("""
    O SeletorDLTSaude é uma ferramenta interativa projetada para ajudar profissionais e pesquisadores 
    da área de saúde a escolher a melhor solução de Tecnologia de Ledger Distribuído (DLT) e o algoritmo 
    de consenso mais adequado para seus projetos.
    """)
    show_correlation_table()
    if st.button("Iniciar Questionário"):
        st.session_state.page = "questionnaire"
        st.rerun()

def main():
    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
    init_session_state()

    st.title("SeletorDLTSaude")
    st.sidebar.image("assets/logo.svg", use_column_width=True)

    if not is_authenticated():
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.success(f"Logado como {st.session_state.username}")
        st.sidebar.button("Sair", on_click=logout)

        if 'page' not in st.session_state:
            st.session_state.page = "home"

        if st.session_state.page == "home":
            show_home_page()
        elif st.session_state.page == "questionnaire":
            show_questionnaire()
        elif st.session_state.page == "prioritize_characteristics":
            show_prioritize_characteristics()
        elif st.session_state.page == "recommendation":
            show_recommendation()

        st.sidebar.header("Recomendações Anteriores")
        user_recommendations = get_user_recommendations(st.session_state.username)
        for rec in user_recommendations:
            with st.sidebar.expander(f"{rec['scenario']} - {rec['timestamp']}"):
                st.write(f"DLT: {rec['dlt']}")
                st.write(f"Consenso: {rec['consensus']}")

if __name__ == "__main__":
    main()