import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from user_management import login, register, is_authenticated
from database import get_user_recommendations, save_recommendation
from decision_logic import get_recommendation, get_sunburst_data
from dlt_data import scenarios, questions
from utils import init_session_state

def create_sunburst_chart(data):
    df = pd.DataFrame(data)
    fig = px.sunburst(df, ids='id', names='name', parents='parent', hover_data=['consensus'])
    fig.update_layout(title="Visualização da Árvore de Decisão")
    return fig

def create_flow_diagram(scenario, current_step):
    steps = [q['id'] for q in questions[scenario]]
    edges = [(steps[i], steps[i+1]) for i in range(len(steps)-1)]
    
    nodes = [
        {
            'id': step,
            'label': step.replace('_', ' ').title(),
            'color': 'lightblue' if i < current_step else ('yellow' if i == current_step else 'white')
        }
        for i, step in enumerate(steps)
    ]
    
    edges = [
        {'from': edge[0], 'to': edge[1], 'arrows': 'to'}
        for edge in edges
    ]
    
    return nodes, edges

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

        if 'step' not in st.session_state:
            st.session_state.step = 0

        if st.session_state.step == 0:
            st.header("Escolha um Cenário de Saúde")
            scenario = st.selectbox("Selecione um cenário", list(scenarios.keys()))
            if st.button("Iniciar"):
                st.session_state.scenario = scenario
                st.session_state.step = 1
                st.session_state.answers = {}
                st.rerun()

        elif st.session_state.step <= len(questions[st.session_state.scenario]):
            question = questions[st.session_state.scenario][st.session_state.step - 1]
            st.header(f"Pergunta {st.session_state.step}")
            st.write(question['text'])
            st.write(question['explanation'])
            answer = st.radio("Selecione uma opção:", question['options'])
            
            st.markdown("""
            ### Diagrama de Fluxo Interativo
            Este diagrama mostra sua jornada através do processo de tomada de decisão. Cada caixa representa uma pergunta, e a caixa destacada é sua etapa atual. À medida que você avança, verá como cada resposta leva à próxima pergunta, resultando em uma recomendação personalizada.

            O diagrama ajuda a visualizar:
            1. As perguntas já respondidas (azul claro)
            2. A pergunta atual (amarelo)
            3. As perguntas futuras (branco)
            4. A sequência lógica das decisões

            Isso permite que você entenda melhor como suas escolhas influenciam a recomendação final de tecnologia DLT e algoritmo de consenso para seu cenário de saúde.
            """)
            
            nodes, edges = create_flow_diagram(st.session_state.scenario, st.session_state.step - 1)
            st.graphviz_chart(f"""
                digraph {{
                    rankdir=LR;
                    node [shape=box];
                    {'; '.join([f'{node["id"]} [label="{node["label"]}", style=filled, fillcolor={node["color"]}]' for node in nodes])}
                    {'; '.join([f'{edge["from"]} -> {edge["to"]}' for edge in edges])}
                }}
            """)
            
            if st.button("Próximo"):
                st.session_state.answers[question['id']] = answer
                st.session_state.step += 1
                st.rerun()

        else:
            recommendation = get_recommendation(st.session_state.scenario, st.session_state.answers)
            st.header("Recomendação")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Framework DLT")
                st.info(recommendation['dlt'])
            with col2:
                st.subheader("Algoritmo de Consenso")
                st.info(recommendation['consensus'])
            
            st.subheader("Explicação Detalhada")
            st.markdown(recommendation['explanation'])

            if st.button("Salvar Recomendação"):
                save_recommendation(st.session_state.username, st.session_state.scenario, recommendation)
                st.success("Recomendação salva com sucesso!")

            st.header("Visualizações")
            
            st.markdown("""
            ### Gráfico Sunburst
            Este gráfico Sunburst mostra como diferentes fatores influenciam a escolha da tecnologia DLT e do algoritmo de consenso. 

            Como interpretar:
            1. O centro representa o ponto de partida da decisão.
            2. Cada anel em direção ao exterior representa um ponto de decisão (uma pergunta que você respondeu).
            3. O anel mais externo mostra a DLT e o algoritmo de consenso recomendados com base em suas escolhas.
            4. As cores representam diferentes caminhos de decisão.
            5. Ao passar o mouse sobre cada seção, você verá informações detalhadas sobre aquele ponto de decisão.

            Este gráfico ajuda a visualizar como cada resposta afeta a recomendação final, permitindo uma compreensão mais profunda do processo de seleção de tecnologia para seu cenário de saúde.
            """)
            
            sunburst_data = get_sunburst_data()
            fig_sunburst = create_sunburst_chart(sunburst_data)
            st.plotly_chart(fig_sunburst)

            st.subheader("Suas Respostas")
            df = pd.DataFrame(list(st.session_state.answers.items()), columns=['Pergunta', 'Resposta'])
            fig_responses = px.bar(df, x='Pergunta', y='Resposta', title="Suas Respostas")
            st.plotly_chart(fig_responses)

            if st.button("Recomeçar"):
                st.session_state.step = 0
                st.rerun()

        st.sidebar.header("Recomendações Anteriores")
        user_recommendations = get_user_recommendations(st.session_state.username)
        for rec in user_recommendations:
            with st.sidebar.expander(f"{rec['scenario']} - {rec['timestamp']}"):
                st.write(f"DLT: {rec['dlt']}")
                st.write(f"Consenso: {rec['consensus']}")

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if __name__ == "__main__":
    main()
