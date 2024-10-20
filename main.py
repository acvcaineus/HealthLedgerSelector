import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from user_management import login, register, is_authenticated, logout
from database import get_user_recommendations, save_recommendation, save_feedback
from decision_logic import get_recommendation, compare_algorithms, select_final_algorithm
from dlt_data import scenarios, questions, dlt_classes, consensus_algorithms
from utils import init_session_state

def define_consensus_weights():
    st.subheader("Defina os Pesos para as Características do Algoritmo de Consenso")
    st.write("Atribua um valor de 0 a 10 para cada característica com base na sua importância.")
    
    weights = {
        "security": st.slider("Peso de Segurança", 0, 10, 5),
        "scalability": st.slider("Peso de Escalabilidade", 0, 10, 5),
        "energy_efficiency": st.slider("Peso de Eficiência Energética", 0, 10, 5),
        "governance": st.slider("Peso de Governança", 0, 10, 5)
    }
    
    return weights

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
                   characteristics=', '.join(question_data['characteristics']))
        
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
            node['title'] = f"Camada Shermin: {node['shermin_layer']}<br>Características: {node['characteristics']}"
    
    html = net.generate_html()
    components.html(html, height=600)
    
    st.write("**Legenda:**")
    st.write("- Círculos azuis: Perguntas (Passe o mouse para ver a camada Shermin e características)")
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
            save_feedback(st.session_state.username, st.session_state.scenario, st.session_state.recommendation, feedback_data)
            st.success("Obrigado pelo seu feedback! Sua opinião é muito importante para nós.")
            st.balloons()

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

    st.subheader("Defina as Porcentagens para cada Característica")
    characteristics = ["Segurança", "Escalabilidade", "Eficiência Energética", "Governança"]
    percentages = {}
    total = 0
    for char in characteristics:
        percentages[char] = st.slider(f"Porcentagem para {char}", 0, 100, 25, 5)
        total += percentages[char]
    
    if total != 100:
        st.warning(f"A soma das porcentagens deve ser 100%. Atualmente é {total}%.")
    else:
        final_algorithm = select_final_algorithm(recommendation['consensus_group'], percentages)
        st.success(f"O algoritmo final recomendado é: {final_algorithm}")

    st.subheader("Influência das Características na Decisão")
    fig = px.bar(df, x=df.index, y=df.columns, title="Comparação de Características")
    st.plotly_chart(fig)

    show_feedback_form()

def show_questionnaire():
    st.header("Questionário")
    if st.session_state.scenario not in questions:
        st.error(f"Cenário '{st.session_state.scenario}' não encontrado.")
        return

    scenario_questions = questions[st.session_state.scenario]
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
                st.session_state.page = "recommendation"
                recommendation = get_recommendation(st.session_state.answers, st.session_state.weights)
                st.session_state.recommendation = recommendation
            st.rerun()

        progress = (st.session_state.question_index + 1) / len(question_order)
        st.progress(progress)
        st.write(f"Progresso: Pergunta {st.session_state.question_index + 1} de {len(question_order)}")
    else:
        st.session_state.page = "recommendation"
        recommendation = get_recommendation(st.session_state.answers, st.session_state.weights)
        st.session_state.recommendation = recommendation
        st.rerun()

def show_scenario_selection():
    st.header("Escolha um Cenário de Saúde")
    scenario = st.selectbox("Selecione um cenário", list(scenarios.keys()))

    st.write(f"**Descrição do cenário:** {scenarios[scenario]}")

    if st.button("Iniciar"):
        st.session_state.scenario = scenario
        st.session_state.answers = {}
        st.session_state.page = "weight_definition"
        st.rerun()

def show_home_page():
    st.header("Bem-vindo ao SeletorDLTSaude")
    st.write("""
    O SeletorDLTSaude é uma ferramenta interativa projetada para ajudar profissionais e pesquisadores 
    da área de saúde a escolher a melhor solução de Tecnologia de Ledger Distribuído (DLT) e o algoritmo 
    de consenso mais adequado para seus projetos.
    """)

    if st.button("Iniciar Questionário"):
        st.session_state.page = "scenario_selection"
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
        elif st.session_state.page == "scenario_selection":
            show_scenario_selection()
        elif st.session_state.page == "weight_definition":
            st.session_state.weights = define_consensus_weights()
            if st.button("Iniciar Questionário"):
                st.session_state.page = "questionnaire"
                st.rerun()
        elif st.session_state.page == "questionnaire":
            show_questionnaire()
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