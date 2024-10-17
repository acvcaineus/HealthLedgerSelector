import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from user_management import login, register, is_authenticated
from database import get_user_recommendations, save_recommendation
from decision_logic import get_recommendation, get_comparison_data, get_sunburst_data
from dlt_data import scenarios, questions, dlt_options, consensus_options, metrics
from utils import init_session_state
from news_updates import fetch_dlt_healthcare_news

def create_sunburst_chart(data):
    df = pd.DataFrame(data)
    fig = px.sunburst(
        df,
        ids='id',
        names='name',
        parents='parent',
        hover_data=['consensus'],
        title="Visualização da Hierarquia de Tecnologias DLT",
        color='id',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        font=dict(size=14),
        margin=dict(t=50, l=25, r=25, b=25),
        height=600
    )
    fig.update_traces(
        textinfo='label',
        insidetextorientation='radial'
    )
    return fig

def plot_dag_dlt_radar():
    dag_dlt_data = {
        'DLT': ['IOTA (DAG)', 'Hashgraph', 'Tangle', 'DLT Recomendado (DAG)'],
        'Escalabilidade': [9, 8, 9, 9],
        'Segurança': [7, 8, 7, 7],
        'Eficiência Energética': [9, 9, 8, 9],
        'Descentralização': [8, 7, 8, 8],
        'Tempo de Confirmação': [8, 7, 7, 8]
    }
    dag_dlt_df = pd.DataFrame(dag_dlt_data)
    
    fig = go.Figure()
    for i in range(len(dag_dlt_df)):
        fig.add_trace(go.Scatterpolar(
            r=[dag_dlt_df['Escalabilidade'][i], dag_dlt_df['Segurança'][i], dag_dlt_df['Eficiência Energética'][i], 
               dag_dlt_df['Descentralização'][i], dag_dlt_df['Tempo de Confirmação'][i]],
            theta=['Escalabilidade', 'Segurança', 'Eficiência Energética', 'Descentralização', 'Tempo de Confirmação'],
            fill='toself',
            name=dag_dlt_df['DLT'][i]
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title="Comparação das DLTs Baseadas em DAG com a Recomendação"
    )
    return fig

def plot_dag_consensus_radar():
    dag_algorithms_data = {
        'Algoritmo': ['IOTA (Tangle)', 'SCP (Stellar)', 'PoA', 'Algoritmo Recomendado (DAG)'],
        'Escalabilidade': [9, 8, 6, 9],
        'Segurança': [7, 8, 7, 7],
        'Eficiência Energética': [9, 8, 7, 9],
        'Descentralização': [8, 6, 5, 8],
        'Tempo de Confirmação': [8, 7, 6, 8]
    }
    dag_algorithms_df = pd.DataFrame(dag_algorithms_data)
    
    fig = go.Figure()
    for i in range(len(dag_algorithms_df)):
        fig.add_trace(go.Scatterpolar(
            r=[dag_algorithms_df['Escalabilidade'][i], dag_algorithms_df['Segurança'][i], dag_algorithms_df['Eficiência Energética'][i], 
               dag_algorithms_df['Descentralização'][i], dag_algorithms_df['Tempo de Confirmação'][i]],
            theta=['Escalabilidade', 'Segurança', 'Eficiência Energética', 'Descentralização', 'Tempo de Confirmação'],
            fill='toself',
            name=dag_algorithms_df['Algoritmo'][i]
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title="Comparação dos Algoritmos de Consenso em DAG com a Recomendação"
    )
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

def show_home_page():
    st.header("Bem-vindo ao SeletorDLTSaude")
    st.write("""
    O SeletorDLTSaude é uma ferramenta interativa projetada para ajudar profissionais e pesquisadores 
    da área de saúde a escolher a melhor solução de Tecnologia de Ledger Distribuído (DLT) e o algoritmo 
    de consenso mais adequado para seus projetos.
    
    ### Como usar a ferramenta:
    1. Escolha um cenário de saúde que melhor se aplica ao seu projeto.
    2. Responda a uma série de perguntas sobre os requisitos do seu projeto.
    3. Receba uma recomendação personalizada de DLT e algoritmo de consenso.
    4. Explore visualizações e comparações detalhadas das soluções recomendadas.
    
    ### Funcionalidades principais:
    - **Questionário Guiado**: Perguntas adaptadas ao seu cenário específico.
    - **Recomendações Personalizadas**: Baseadas nas suas respostas e necessidades.
    - **Visualizações Interativas**: Gráficos e diagramas para melhor compreensão.
    - **Comparação de Soluções**: Compare diferentes opções de DLT lado a lado.
    - **Histórico de Recomendações**: Acesse suas recomendações anteriores.
    
    ### Como interpretar os resultados:
    - **Gráfico Sunburst**: Mostra como suas respostas influenciam a recomendação final.
    - **Diagrama de Fluxo**: Visualize seu progresso através do questionário.
    - **Gráfico de Radar**: Compare diferentes soluções DLT em várias dimensões.
    
    Clique no botão abaixo para começar o processo de seleção e receber sua recomendação personalizada!
    """)
    
    if st.button("Iniciar Questionário"):
        st.session_state.page = "scenario_selection"
        st.rerun()

def show_scenario_selection():
    st.header("Escolha um Cenário de Saúde")
    scenario = st.selectbox("Selecione um cenário", list(scenarios.keys()))
    
    st.write(f"**Descrição do cenário:** {scenarios[scenario]}")
    
    if st.button("Iniciar"):
        st.session_state.scenario = scenario
        st.session_state.step = 1
        st.session_state.answers = {}
        st.session_state.page = "questionnaire"
        st.rerun()

def show_questionnaire():
    if st.session_state.scenario not in questions:
        st.error(f"Cenário '{st.session_state.scenario}' não encontrado.")
        return

    scenario_questions = questions[st.session_state.scenario]
    if st.session_state.step > len(scenario_questions):
        st.error("Todas as perguntas foram respondidas.")
        st.session_state.page = "recommendation"
        st.rerun()
        return

    question = scenario_questions[st.session_state.step - 1]
    st.header(f"Pergunta {st.session_state.step}")
    st.write(question['text'])
    
    with st.expander("Mais informações sobre esta pergunta"):
        st.write(question['explanation'])
    
    answer = st.radio("Selecione uma opção:", question['options'])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Voltar") and st.session_state.step > 1:
            st.session_state.step -= 1
            st.rerun()
    with col2:
        if st.button("Próximo"):
            st.session_state.answers[question['id']] = answer
            if st.session_state.step < len(scenario_questions):
                st.session_state.step += 1
            else:
                st.session_state.page = "recommendation"
            st.rerun()
    
    st.markdown("### Diagrama de Fluxo Interativo")
    nodes, edges = create_flow_diagram(st.session_state.scenario, st.session_state.step - 1)
    st.graphviz_chart(f"""
        digraph {{
            rankdir=LR;
            node [shape=box];
            {'; '.join([f'{node["id"]} [label="{node["label"]}", style=filled, fillcolor={node["color"]}]' for node in nodes])}
            {'; '.join([f'{edge["from"]} -> {edge["to"]}' for edge in edges])}
        }}
    """)

def show_recommendation():
    answers = st.session_state.answers
    recommendation = get_recommendation(answers)
    st.header("Recomendação")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Framework DLT")
        if recommendation['dlt'] == "Distributed Ledger" and recommendation['consensus'] == "Directed Acyclic Graph (DAG)":
            st.info("Distributed Ledger (DAG)")
        else:
            st.info(recommendation['dlt'])
    with col2:
        st.subheader("Algoritmo de Consenso")
        st.info(recommendation['consensus'])
    
    with st.expander("Explicação Detalhada"):
        if recommendation['dlt'] == "Distributed Ledger" and recommendation['consensus'] == "Directed Acyclic Graph (DAG)":
            st.markdown('''
            **DLT Recomendada: Distributed Ledger (DAG)**
            Não utiliza necessariamente a tecnologia de blockchain. Indica-se a adoção de **Directed Acyclic Graph (DAG)**.
            
            **Algoritmo de Consenso Recomendado: IOTA**
            Adotado para IoT e alta escalabilidade. O IOTA é uma implementação específica de DAG otimizada para dispositivos IoT e casos de uso que requerem alta escalabilidade.
            ''')
        else:
            st.markdown(f'''
            **DLT Recomendada:** {recommendation['dlt']}
            {recommendation['dlt_explanation']}

            **Algoritmo de Consenso Recomendado:** {recommendation['consensus']}
            {recommendation['consensus_explanation']}
            ''')

    if st.button("Salvar Recomendação"):
        save_recommendation(st.session_state.username, st.session_state.scenario, recommendation)
        st.success("Recomendação salva com sucesso!")

    st.header("Comparação de Soluções DLT")
    
    comparison_data = get_comparison_data(recommendation['dlt'], recommendation['consensus'])
    
    st.subheader("Tabela Comparativa")
    df_comparison = pd.DataFrame(comparison_data)
    st.table(df_comparison)

    st.subheader("Comparação Visual (Gráfico de Radar)")
    
    metrics_to_plot = [
        "Tempo de confirmação de transação (segundos)",
        "Throughput (transações por segundo)",
        "Nível de descentralização (1-10)",
        "Flexibilidade de programação (1-10)",
        "Interoperabilidade (1-10)",
        "Resistência a ataques quânticos (1-10)"
    ]

    fig = go.Figure()

    for system in df_comparison.index:
        values = df_comparison.loc[system, metrics_to_plot].values.tolist()
        values += values[:1]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics_to_plot + [metrics_to_plot[0]],
            fill='toself',
            name=system
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max([max(df_comparison[metric]) for metric in metrics_to_plot])]
            )),
        showlegend=True
    )

    st.plotly_chart(fig)

    st.markdown("""
    **Como interpretar o gráfico de radar:**
    - Cada eixo representa uma métrica diferente.
    - Quanto mais distante do centro, melhor o desempenho naquela métrica.
    - Compare as áreas formadas por cada solução para uma visão geral do desempenho.
    - Observe que algumas métricas podem ser mais importantes que outras dependendo do seu caso de uso.
    """)

    if recommendation['dlt'] == "Distributed Ledger" and recommendation['consensus'] == "Directed Acyclic Graph (DAG)":
        st.subheader("Comparação de DLTs baseadas em DAG")
        fig_dag_dlt = plot_dag_dlt_radar()
        st.plotly_chart(fig_dag_dlt)
        
        st.subheader("Comparação de Algoritmos de Consenso em DAG")
        fig_dag_consensus = plot_dag_consensus_radar()
        st.plotly_chart(fig_dag_consensus)
        
        st.markdown('''
        **Como interpretar os gráficos de radar para DLTs e Algoritmos baseados em DAG:**
        - Cada eixo representa uma característica diferente (Escalabilidade, Segurança, etc.).
        - Quanto mais distante do centro, melhor o desempenho naquela característica.
        - Compare as áreas formadas por cada solução para uma visão geral do desempenho.
        - O "DLT Recomendado (DAG)" e "Algoritmo Recomendado (DAG)" representam a solução sugerida com base nas suas respostas.
        ''')

    st.header("Visualizações")
    
    with st.expander("Como interpretar o Gráfico Sunburst"):
        st.markdown("""
        O gráfico Sunburst mostra como diferentes fatores influenciam a escolha da tecnologia DLT e do algoritmo de consenso. 
        
        - O centro representa o ponto de partida da decisão.
        - Cada anel em direção ao exterior representa um ponto de decisão (uma pergunta que você respondeu).
        - O anel mais externo mostra a DLT e o algoritmo de consenso recomendados com base em suas escolhas.
        - As cores representam diferentes caminhos de decisão.
        - Ao passar o mouse sobre cada seção, você verá informações detalhadas sobre aquele ponto de decisão.
        
        Este gráfico ajuda a visualizar como cada resposta afeta a recomendação final, permitindo uma compreensão mais profunda do processo de seleção de tecnologia para seu cenário de saúde.
        """)
    
    sunburst_data = get_sunburst_data()
    fig_sunburst = create_sunburst_chart(sunburst_data)
    st.plotly_chart(fig_sunburst)

    st.subheader("Suas Respostas")
    df = pd.DataFrame(list(st.session_state.answers.items()), columns=['Pergunta', 'Resposta'])
    fig_responses = px.bar(df, x='Pergunta', y='Resposta', title="Suas Respostas")
    st.plotly_chart(fig_responses)

    if st.button("Voltar para a Página Inicial"):
        st.session_state.page = "home"
        st.rerun()

def show_news_updates():
    st.header("Atualizações em Tempo Real sobre DLT na Saúde")
    news_articles = fetch_dlt_healthcare_news()
    
    if news_articles:
        for article in news_articles:
            with st.expander(article['title']):
                st.write(article['description'])
                st.write(f"Publicado em: {article['publishedAt']}")
                st.markdown(f"[Leia mais]({article['url']})")
    else:
        st.info("Nenhuma notícia recente disponível. Por favor, tente novamente mais tarde.")

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
            show_news_updates()
        elif st.session_state.page == "scenario_selection":
            show_scenario_selection()
        elif st.session_state.page == "questionnaire":
            show_questionnaire()
        elif st.session_state.page == "recommendation":
            show_recommendation()
            show_news_updates()

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