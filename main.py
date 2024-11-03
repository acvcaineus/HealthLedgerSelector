import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from user_management import login, register, is_authenticated, logout
from decision_tree import run_decision_tree
from decision_logic import consensus_algorithms
from database import get_user_recommendations
from metrics import show_metrics
from utils import init_session_state

def reset_application():
    """Reset the entire application state."""
    session_keys = [
        'answers',
        'current_recommendation',
        'metrics_calculated',
        'evaluation_matrices',
        'step',
        'scenario',
        'weights',
        'page'
    ]
    for key in session_keys:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.page = 'Início'

def show_comparisons():
    """Display framework comparisons page."""
    st.title("Comparação de Frameworks")
    
    # Framework comparison data
    frameworks_data = {
        "Framework": [
            "Blockchain-Based Framework for Interoperable EHRs",
            "CREDO-DLT Decision Support Tool",
            "Medshare Data Sharing Framework",
            "TrialChain para Ensaios Clínicos",
            "PharmaChain para Cadeia de Suprimentos",
            "Action-EHR Framework para EHRs",
            "MedRec para Gerenciamento de Registros Médicos",
            "SeletorDLTSaude (Nosso Framework)"
        ],
        "DLTs Possíveis": [
            "DLT permissionada privada",
            "Todas as plataformas DLT relevantes",
            "Blockchain permissionada",
            "DLT permissionada privada/pública",
            "DLT permissionada pública",
            "Hyperledger Fabric, Ethereum",
            "Blockchain permissionada",
            "Múltiplas DLTs (Hyperledger Fabric, Ethereum, IOTA, etc.)"
        ]
    }
    
    st.dataframe(pd.DataFrame(frameworks_data))
    
    # Create radar chart comparing frameworks
    frameworks_metrics = {
        'SeletorDLTSaude': {
            'Segurança': 0.9,
            'Escalabilidade': 0.85,
            'Eficiência': 0.8,
            'Governança': 0.85,
            'Interoperabilidade': 0.9
        },
        'CREDO-DLT': {
            'Segurança': 0.8,
            'Escalabilidade': 0.7,
            'Eficiência': 0.75,
            'Governança': 0.8,
            'Interoperabilidade': 0.85
        }
    }
    
    fig = go.Figure()
    
    for framework, metrics in frameworks_metrics.items():
        fig.add_trace(go.Scatterpolar(
            r=list(metrics.values()),
            theta=list(metrics.keys()),
            fill='toself',
            name=framework
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Comparação de Frameworks"
    )
    
    st.plotly_chart(fig)

def show_home_page():
    st.title("SeletorDLTSaude - Sistema de Seleção de DLT para Saúde")
    st.write("Bem-vindo ao SeletorDLTSaude, uma aplicação para ajudar na escolha de tecnologias de ledger distribuído (DLT) para projetos de saúde.")

    if st.button("Iniciar Questionário", help="Clique aqui para começar o processo de seleção de DLT"):
        st.session_state.page = "Framework Proposto"
        st.experimental_rerun()

def show_user_profile():
    st.header(f"Perfil do Usuário: {st.session_state.username}")
    recommendations = get_user_recommendations(st.session_state.username)
    if recommendations:
        st.subheader("Últimas Recomendações")
        for rec in recommendations:
            st.write(f"DLT: {rec['dlt']}")
            st.write(f"Consenso: {rec['consensus']}")
            st.write(f"Data: {rec['timestamp']}")
            st.markdown("---")

def main():
    st.set_page_config(page_title="SeletorDLTSaude", page_icon="🏥", layout="wide")
    init_session_state()

    if not is_authenticated():
        st.title("SeletorDLTSaude - Login")
        tab1, tab2 = st.tabs(["Login", "Registrar"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.title("Menu")
        menu_options = ['Início', 'Framework Proposto', 'Métricas', 'Comparações', 'Perfil', 'Logout']
        
        # Add reset button to sidebar
        if st.sidebar.button("Reiniciar Aplicação", help="Reiniciar toda a aplicação"):
            reset_application()
            st.experimental_rerun()
        
        menu_option = st.sidebar.selectbox(
            "Escolha uma opção",
            menu_options,
            index=menu_options.index(st.session_state.page) if st.session_state.page in menu_options else 0
        )
        
        st.session_state.page = menu_option
        
        if menu_option == 'Início':
            show_home_page()
        elif menu_option == 'Framework Proposto':
            run_decision_tree()
        elif menu_option == 'Métricas':
            show_metrics()
        elif menu_option == 'Comparações':
            show_comparisons()
        elif menu_option == 'Perfil':
            show_user_profile()
        elif menu_option == 'Logout':
            logout()
            st.session_state.page = 'Início'
            st.experimental_rerun()

if __name__ == "__main__":
    main()
