import streamlit as st
from user_management import login, register, logout, is_authenticated
from decision_tree import run_decision_tree
from database import get_user_recommendations
from utils import init_session_state
from metrics import calcular_gini, calcular_entropia, calcular_profundidade_decisoria, calcular_pruning
import plotly.graph_objects as go
from decision_logic import compare_algorithms

def show_home_page():
    st.title("Seleção de DLT e Consenso na Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, um sistema de recomendação de tecnologias de ledger distribuído (DLT) para aplicações em saúde.")

    st.write('''
    ## Como a ferramenta funciona:
    1. **Questionário Interativo**: Responda a perguntas sobre requisitos específicos do seu projeto de saúde.
    2. **Análise Baseada em Camadas**: Utilizamos a pilha Shermin para avaliar as necessidades em diferentes níveis (Aplicação, Consenso, Infraestrutura, Internet).
    3. **Recomendação Personalizada**: Com base nas suas respostas, sugerimos a DLT e o algoritmo de consenso mais adequados.

    ## Funcionalidades:
    - Avaliação detalhada de requisitos de projeto
    - Comparação visual de diferentes DLTs e algoritmos
    - Explicações claras sobre as recomendações
    - Perfil de usuário para salvar e revisar recomendações anteriores

    ## Benefícios ao adotar esta ferramenta:
    - Tomada de decisão informada sobre tecnologias blockchain para saúde
    - Economia de tempo na pesquisa e seleção de DLTs
    - Alinhamento das soluções tecnológicas com as necessidades específicas do seu projeto
    - Melhoria contínua das recomendações através do feedback dos usuários
    ''')

    st.write("## Tabela de DLTs, Grupos de Algoritmos e Algoritmos por Grupo")
    with st.expander("Clique para expandir"):
        st.table({
            'Grupo': ['Alta Segurança e Controle', 'Alta Eficiência Operacional', 'Escalabilidade e Governança Flexível', 'Alta Escalabilidade em Redes IoT', 'Alta Segurança e Descentralização de Dados Críticos'],
            'Tipos DLTs': ['DLT Permissionada Privada, DLT Pública Permissionless', 'DLT Permissionada Simples', 'DLT Híbrida, DLT com Consenso Delegado', 'DLT Pública', 'DLT Pública Permissionless'],
            'Algoritmos de Consenso': ['PBFT, PoW', 'RAFT, PoA', 'PoS, DPoS', 'Tangle', 'PoW, PoS'],
            'Cenários de Uso': ['Prontuários eletrônicos, integração de dados sensíveis', 'Sistemas locais de saúde, agendamento de pacientes', 'Monitoramento de saúde pública, redes regionais de saúde', 'Monitoramento de dispositivos IoT em saúde', 'Sistemas de pagamento descentralizados, dados críticos de saúde pública']
        })

    if st.button("Iniciar Questionário"):
        st.session_state.page = "Framework Proposto"
        st.rerun()

def show_metrics():
    st.header("Métricas e Diferenciais do Framework Proposto")

    classes = {"Sim": 70, "Não": 30}
    decisoes = [3, 4, 2, 5]
    total_nos = 20
    nos_podados = 5
    
    gini = calcular_gini(classes)
    entropia = calcular_entropia(classes)
    profundidade = calcular_profundidade_decisoria(decisoes)
    pruning_ratio = calcular_pruning(total_nos, nos_podados)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Impureza de Gini", f"{gini:.2f}")
        st.metric("Entropia", f"{entropia:.2f}")
    with col2:
        st.metric("Profundidade Decisória", f"{profundidade:.2f}")
        st.metric("Pruning Ratio", f"{pruning_ratio:.2f}")

    fig = go.Figure(data=[
        go.Bar(name='Métricas', x=['Gini', 'Entropia', 'Profundidade', 'Pruning'],
               y=[gini, entropia, profundidade, pruning_ratio])
    ])
    st.plotly_chart(fig)

    st.subheader("Explicação das Métricas")
    st.write("""
    - **Impureza de Gini**: Mede a diversidade das classes em cada nó da árvore.
    - **Entropia**: Quantifica a incerteza ou aleatoriedade nas decisões.
    - **Profundidade Decisória**: Indica a complexidade da árvore de decisão.
    - **Pruning Ratio**: Mostra a eficácia da poda na simplificação do modelo.
    """)

    st.subheader("Diferenciais do Framework Proposto")
    st.write("""
    1. **Adaptabilidade ao Contexto de Saúde**: Nosso framework é especialmente projetado para atender às necessidades específicas do setor de saúde.
    2. **Integração de Múltiplos Critérios**: Considera diversos fatores como segurança, escalabilidade e eficiência energética na recomendação de DLTs.
    3. **Visualização Interativa**: Oferece uma interface gráfica intuitiva para melhor compreensão das decisões.
    4. **Feedback Contínuo**: Permite que os usuários forneçam feedback, melhorando continuamente as recomendações.
    5. **Atualização em Tempo Real**: Incorpora as últimas tendências e avanços em DLTs para o setor de saúde.
    """)

def show_user_profile():
    st.header("Perfil do Usuário")
    st.write(f"Bem-vindo, {st.session_state.username}!")

    recommendations = get_user_recommendations(st.session_state.username)
    
    if recommendations:
        st.subheader("Suas Recomendações Salvas:")
        for rec in recommendations:
            st.write(f"Cenário: {rec['scenario']}")
            st.write(f"DLT Recomendada: {rec['dlt']}")
            st.write(f"Algoritmo de Consenso: {rec['consensus']}")
            st.write(f"Data: {rec['timestamp']}")
            st.write("---")
    else:
        st.write("Você ainda não tem recomendações salvas.")

def show_recommendation_comparison():
    st.header("Comparação de Recomendações")
    if 'recommendation' in st.session_state and st.session_state.recommendation:
        rec = st.session_state.recommendation
        st.write(f"DLT Recomendada: {rec.get('dlt', 'Não disponível')}")
        st.write(f"Grupo de Consenso: {rec.get('consensus_group', 'Não disponível')}")
        st.write(f"Algoritmo de Consenso Recomendado: {rec.get('consensus', 'Não disponível')}")
        
        if 'consensus_group' in rec:
            st.subheader("Comparação Visual dos Algoritmos")
            comparison_data = compare_algorithms(rec['consensus_group'])
            
            new_metrics = {
                'Latência': {alg: round(5 - score, 2) for alg, score in comparison_data['Escalabilidade'].items()},
                'Throughput': comparison_data['Escalabilidade'],
                'Tolerância a Falhas': comparison_data['Segurança'],
                'Nível de Descentralização': {alg: round((score + comparison_data['Governança'][alg]) / 2, 2) for alg, score in comparison_data['Segurança'].items()}
            }
            comparison_data.update(new_metrics)

            available_metrics = list(comparison_data.keys())
            selected_metrics = st.multiselect("Selecione as métricas para comparar", available_metrics, default=available_metrics[:4])

            if selected_metrics:
                fig = go.Figure()

                for alg in comparison_data['Segurança'].keys():
                    fig.add_trace(go.Scatterpolar(
                        r=[comparison_data[metric][alg] for metric in selected_metrics],
                        theta=selected_metrics,
                        fill='toself',
                        name=alg
                    ))

                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 5]
                        )),
                    showlegend=True
                )
                
                st.plotly_chart(fig)

            st.subheader("Comparação Detalhada")
            st.table({metric: comparison_data[metric] for metric in selected_metrics})

            st.subheader("Justificativa da Recomendação")
            st.write(f"O algoritmo {rec['consensus']} foi selecionado porque:")
            for metric in selected_metrics:
                if rec['consensus'] in comparison_data[metric]:
                    score = comparison_data[metric][rec['consensus']]
                    st.write(f"- {metric}: pontuação {score}/5")

            st.subheader("Cenários de Aplicação")
            scenarios = {
                "PBFT": "Ideal para prontuários eletrônicos e sistemas que requerem alta segurança e controle centralizado.",
                "PoW": "Adequado para sistemas de pagamento descentralizados e proteção de dados críticos de saúde pública.",
                "PoS": "Ótimo para redes de saúde que necessitam de alta escalabilidade e eficiência energética.",
                "DPoS": "Perfeito para sistemas de monitoramento de saúde pública e redes regionais de saúde.",
                "PoA": "Ideal para sistemas locais de saúde e agendamento de pacientes.",
                "Tangle": "Excelente para monitoramento de dispositivos IoT em saúde e processamento de dados em tempo real."
            }
            for alg, scenario in scenarios.items():
                if alg in comparison_data['Segurança']:
                    st.write(f"**{alg}**: {scenario}")

        else:
            st.write("Dados de comparação não disponíveis.")
        
        st.subheader("Pesos Atribuídos")
        st.write("Os seguintes pesos foram considerados na escolha do algoritmo:")
        st.write("- Segurança: 40%")
        st.write("- Escalabilidade: 30%")
        st.write("- Eficiência Energética: 20%")
        st.write("- Governança: 10%")
    else:
        st.write("Nenhuma recomendação disponível para comparação. Por favor, complete o questionário primeiro.")

def show_framework_info():
    st.header("Sobre o Framework Proposto")
    
    st.subheader("Embasamento Teórico")
    st.write("""
    O framework proposto é baseado na Pilha Shermin, que divide a análise de DLTs em quatro camadas:
    1. Aplicação
    2. Consenso
    3. Infraestrutura
    4. Internet
    
    Esta abordagem permite uma avaliação holística das necessidades do projeto de saúde e das capacidades das diferentes DLTs.
    """)
    
    st.subheader("Métricas e Ponderações")
    st.write("""
    O framework utiliza as seguintes métricas principais:
    - Segurança (40%)
    - Escalabilidade (30%)
    - Eficiência Energética (20%)
    - Governança (10%)
    
    Estas ponderações foram definidas com base na importância relativa de cada aspecto para projetos de saúde típicos.
    """)
    
    st.subheader("Fundamentação da Aplicação")
    st.write("""
    A aplicação utiliza um sistema de pontuação ponderada para recomendar a DLT e o algoritmo de consenso mais adequados.
    As respostas do usuário são mapeadas para características específicas, que por sua vez influenciam a pontuação final de cada opção.
    """)
    
    st.subheader("Limitações")
    st.write("""
    1. Generalização: O framework pode não capturar todas as nuances de projetos de saúde altamente especializados.
    2. Dependência de dados atualizados: A eficácia das recomendações depende da atualização constante das informações sobre DLTs e algoritmos.
    3. Simplificação: Algumas complexidades técnicas são simplificadas para tornar o processo de decisão mais acessível.
    4. Foco limitado: O framework se concentra principalmente em DLTs e pode não abordar todos os aspectos de implementação de blockchain em saúde.
    """)

def main():
    init_session_state()

    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")

    if not is_authenticated():
        st.title("SeletorDLTSaude - Login")

        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.title("Menu")
        menu_options = ['Início', 'Framework Proposto', 'Comparação de Recomendações', 'Métricas', 'Sobre o Framework', 'Perfil', 'Logout']

        menu_option = st.sidebar.selectbox(
            "Escolha uma opção",
            menu_options,
            index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
        )

        st.session_state.page = menu_option

        if st.session_state.page == 'Início':
            show_home_page()
        elif st.session_state.page == 'Framework Proposto':
            run_decision_tree()
        elif st.session_state.page == 'Comparação de Recomendações':
            show_recommendation_comparison()
        elif st.session_state.page == 'Métricas':
            show_metrics()
        elif st.session_state.page == 'Sobre o Framework':
            show_framework_info()
        elif st.session_state.page == 'Perfil':
            show_user_profile()
        elif st.session_state.page == 'Logout':
            logout()
            st.session_state.page = 'Início'

if __name__ == "__main__":
    main()