import streamlit as st
import plotly.express as px
import pandas as pd
from user_management import login, register, is_authenticated
from database import get_user_recommendations, save_recommendation
from decision_logic import get_recommendation
from dlt_data import scenarios, questions
from utils import init_session_state

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
            
            if st.button("Next"):
                st.session_state.answers[question['id']] = answer
                st.session_state.step += 1
                st.rerun()

        else:
            recommendation = get_recommendation(st.session_state.scenario, st.session_state.answers)
            st.header("Recommendation")
            st.write(f"Based on your responses, we recommend:")
            st.write(f"**DLT Framework:** {recommendation['dlt']}")
            st.write(f"**Consensus Algorithm:** {recommendation['consensus']}")
            st.write(f"**Explanation:** {recommendation['explanation']}")

            if st.button("Save Recommendation"):
                save_recommendation(st.session_state.username, st.session_state.scenario, recommendation)
                st.success("Recommendation saved successfully!")

            st.header("Response Visualization")
            df = pd.DataFrame(list(st.session_state.answers.items()), columns=['Question', 'Answer'])
            fig = px.bar(df, x='Question', y='Answer', title="Your Responses")
            st.plotly_chart(fig)

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
