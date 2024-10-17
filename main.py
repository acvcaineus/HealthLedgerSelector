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
    fig.update_layout(title="Decision Tree Visualization")
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
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.success(f"Logged in as {st.session_state.username}")
        st.sidebar.button("Logout", on_click=logout)

        if 'step' not in st.session_state:
            st.session_state.step = 0

        if st.session_state.step == 0:
            st.header("Choose a Healthcare Scenario")
            scenario = st.selectbox("Select a scenario", list(scenarios.keys()))
            if st.button("Start"):
                st.session_state.scenario = scenario
                st.session_state.step = 1
                st.session_state.answers = {}
                st.rerun()

        elif st.session_state.step <= len(questions[st.session_state.scenario]):
            question = questions[st.session_state.scenario][st.session_state.step - 1]
            st.header(f"Question {st.session_state.step}")
            st.write(question['text'])
            answer = st.radio("Select an option:", question['options'])
            
            # Explanation for Interactive Flow Diagram
            st.markdown("""
            ### Interactive Flow Diagram
            This diagram shows your journey through the decision-making process. Each box represents a question, and the highlighted box is your current step. As you progress, you'll see how each answer leads to the next question, ultimately resulting in your personalized recommendation.
            """)
            
            # Display Interactive Flow Diagram
            nodes, edges = create_flow_diagram(st.session_state.scenario, st.session_state.step - 1)
            st.graphviz_chart(f"""
                digraph {{
                    rankdir=LR;
                    node [shape=box];
                    {'; '.join([f'{node["id"]} [label="{node["label"]}", style=filled, fillcolor={node["color"]}]' for node in nodes])}
                    {'; '.join([f'{edge["from"]} -> {edge["to"]}' for edge in edges])}
                }}
            """)
            
            if st.button("Next"):
                st.session_state.answers[question['id']] = answer
                st.session_state.step += 1
                st.rerun()

        else:
            recommendation = get_recommendation(st.session_state.scenario, st.session_state.answers)
            st.header("Recommendation")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("DLT Framework")
                st.info(recommendation['dlt'])
            with col2:
                st.subheader("Consensus Algorithm")
                st.info(recommendation['consensus'])
            
            st.subheader("Detailed Explanation")
            st.markdown(recommendation['explanation'])

            if st.button("Save Recommendation"):
                save_recommendation(st.session_state.username, st.session_state.scenario, recommendation)
                st.success("Recommendation saved successfully!")

            st.header("Visualizations")
            
            # Explanation for Sunburst Chart
            st.markdown("""
            ### Sunburst Chart
            This Sunburst chart shows how different factors influence the choice of DLT and consensus algorithm. The center represents the starting point, and each ring outwards shows a decision point. The final ring shows the recommended DLT and consensus algorithm based on your choices.
            """)
            
            # Sunburst Chart
            sunburst_data = get_sunburst_data()
            fig_sunburst = create_sunburst_chart(sunburst_data)
            st.plotly_chart(fig_sunburst)

            # Response Visualization
            st.subheader("Your Responses")
            df = pd.DataFrame(list(st.session_state.answers.items()), columns=['Question', 'Answer'])
            fig_responses = px.bar(df, x='Question', y='Answer', title="Your Responses")
            st.plotly_chart(fig_responses)

            if st.button("Start Over"):
                st.session_state.step = 0
                st.rerun()

        st.sidebar.header("Previous Recommendations")
        user_recommendations = get_user_recommendations(st.session_state.username)
        for rec in user_recommendations:
            with st.sidebar.expander(f"{rec['scenario']} - {rec['timestamp']}"):
                st.write(f"DLT: {rec['dlt']}")
                st.write(f"Consensus: {rec['consensus']}")

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if __name__ == "__main__":
    main()
