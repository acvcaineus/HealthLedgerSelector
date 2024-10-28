import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from decision_logic import get_recommendation, compare_algorithms, consensus_algorithms, reference_data

def show_evaluation_matrices():
    """Display evaluation matrices with explanations"""
    
    # Security Metrics Matrix
    with st.expander("🔒 Matriz de Segurança", expanded=False):
        st.markdown("""
            ### Métricas de Segurança
            Esta matriz avalia os aspectos de segurança da DLT selecionada:
            
            | Métrica | Descrição | Peso |
            |---------|-----------|------|
            | Privacidade | Proteção de dados sensíveis | 40% |
            | Autenticação | Controle de acesso | 30% |
            | Criptografia | Força dos algoritmos | 30% |
        """)
        
        security_data = {
            'DLT': ['Hyperledger Fabric', 'Ethereum', 'IOTA'],
            'Privacidade': [5, 4, 3],
            'Autenticação': [5, 4, 4],
            'Criptografia': [5, 5, 4]
        }
        st.table(pd.DataFrame(security_data))
    
    # Scalability Matrix
    with st.expander("📈 Matriz de Escalabilidade", expanded=False):
        st.markdown("""
            ### Métricas de Escalabilidade
            Avaliação da capacidade de crescimento e adaptação:
            
            | Métrica | Descrição | Peso |
            |---------|-----------|------|
            | TPS | Transações por segundo | 40% |
            | Latência | Tempo de resposta | 30% |
            | Throughput | Volume de dados | 30% |
        """)
        
        scalability_data = {
            'DLT': ['Hyperledger Fabric', 'Ethereum', 'IOTA'],
            'TPS': [3000, 15, 1000],
            'Latência': ['1s', '15s', '60s'],
            'Throughput': ['Alto', 'Médio', 'Alto']
        }
        st.table(pd.DataFrame(scalability_data))
    
    # Energy Efficiency Matrix
    with st.expander("⚡ Matriz de Eficiência Energética", expanded=False):
        st.markdown("""
            ### Métricas de Eficiência Energética
            Análise do consumo e otimização de recursos:
            
            | Métrica | Descrição | Peso |
            |---------|-----------|------|
            | Consumo | kWh por transação | 40% |
            | Sustentabilidade | Impacto ambiental | 30% |
            | Otimização | Uso de recursos | 30% |
        """)
        
        energy_data = {
            'DLT': ['Hyperledger Fabric', 'Ethereum', 'IOTA'],
            'Consumo (kWh)': [0.001, 62, 0.0001],
            'Sustentabilidade': ['Alta', 'Baixa', 'Alta'],
            'Otimização': ['Alta', 'Média', 'Alta']
        }
        st.table(pd.DataFrame(energy_data))
    
    # Governance Matrix
    with st.expander("🏛️ Matriz de Governança", expanded=False):
        st.markdown("""
            ### Métricas de Governança
            Avaliação dos aspectos de controle e administração:
            
            | Métrica | Descrição | Peso |
            |---------|-----------|------|
            | Controle | Nível de permissionamento | 40% |
            | Auditoria | Rastreabilidade | 30% |
            | Flexibilidade | Adaptabilidade | 30% |
        """)
        
        governance_data = {
            'DLT': ['Hyperledger Fabric', 'Ethereum', 'IOTA'],
            'Controle': ['Alto', 'Baixo', 'Médio'],
            'Auditoria': ['Alta', 'Alta', 'Média'],
            'Flexibilidade': ['Alta', 'Alta', 'Média']
        }
        st.table(pd.DataFrame(governance_data))

def run_decision_tree():
    """Main function for the decision tree"""
    st.title("Framework de Seleção de DLT")
    
    # Show evaluation matrices
    show_evaluation_matrices()
    
    # Rest of the existing decision tree code...
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 1
    
    # Show questions and collect answers
    questions = get_phase_questions(st.session_state.current_phase)
    for question in questions:
        response = st.radio(question['text'], ['Sim', 'Não'])
        st.session_state.answers[question['id']] = response
    
    if st.button("Próxima Fase"):
        st.session_state.current_phase += 1
        st.experimental_rerun()

def get_phase_questions(phase):
    """Get questions for current phase"""
    # Existing question logic...
    return []  # Placeholder

# Rest of the existing code...
