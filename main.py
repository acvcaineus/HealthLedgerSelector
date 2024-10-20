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

# ... [previous code remains unchanged] ...

def show_scenario_selection(dlt, consensus_algorithm):
    st.header("Cenários de Aplicação Possíveis")
    applicable_scenarios = get_scenario_pros_cons(dlt, consensus_algorithm)
    
    if not applicable_scenarios:
        st.warning("Não há cenários aplicáveis para a combinação de DLT e algoritmo de consenso selecionados.")
        return

    for scenario, data in applicable_scenarios.items():
        with st.expander(f"Cenário: {scenario}"):
            st.write(f"**Descrição do cenário:** {scenarios.get(scenario, 'Descrição não disponível')}")
            
            st.write("**Vantagens:**")
            for adv in data["pros"]:
                st.write(f"- {adv}")
            
            st.write("**Desvantagens:**")
            for disadv in data["cons"]:
                st.write(f"- {disadv}")
            
            st.write("**Aplicabilidade do Algoritmo Recomendado:**")
            st.write(data["algorithm_applicability"])

    selected_scenario = st.selectbox("Selecione um cenário para aplicar", list(applicable_scenarios.keys()))

    if st.button("Finalizar"):
        st.session_state.scenario = selected_scenario
        save_recommendation(st.session_state.username, selected_scenario, st.session_state.recommendation)
        st.success("Recomendação salva com sucesso!")

# ... [rest of the code remains unchanged] ...

if __name__ == "__main__":
    main()
