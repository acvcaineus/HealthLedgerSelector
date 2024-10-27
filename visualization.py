import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from decision_logic import consensus_algorithms

def show_metrics():
    st.title("Métricas de Avaliação DLT")
    
    # Security metrics
    st.header("1. Segurança (40%)")
    with st.expander("Ver Detalhes de Segurança"):
        st.markdown("""
        ### Componentes de Segurança
        - **Proteção de Dados**: Criptografia e controle de acesso
        - **Privacidade**: Conformidade com LGPD/HIPAA
        - **Resistência a Ataques**: Mecanismos de consenso
        - **Auditoria**: Rastreabilidade de transações
        
        ### Fórmula de Cálculo:
        ```python
        score_seguranca = (peso_protecao * score_protecao + 
                          peso_privacidade * score_privacidade +
                          peso_resistencia * score_resistencia +
                          peso_auditoria * score_auditoria) / soma_pesos
        ```
        """)
        
        # Sample security scores
        security_data = {
            'Proteção de Dados': 0.4,
            'Privacidade': 0.3,
            'Resistência a Ataques': 0.2,
            'Auditoria': 0.1
        }
        
        fig = go.Figure(data=[go.Pie(labels=list(security_data.keys()),
                                    values=list(security_data.values()),
                                    hole=.3)])
        fig.update_layout(title="Distribuição dos Pesos de Segurança")
        st.plotly_chart(fig)
    
    # Scalability metrics
    st.header("2. Escalabilidade (25%)")
    with st.expander("Ver Detalhes de Escalabilidade"):
        st.markdown("""
        ### Métricas de Escalabilidade
        - **TPS**: Transações por segundo
        - **Latência**: Tempo de confirmação
        - **Capacidade**: Armazenamento e processamento
        
        ### Fórmula de Cálculo:
        ```python
        score_escalabilidade = (tps_normalizado * 0.4 +
                               latencia_normalizada * 0.3 +
                               capacidade_normalizada * 0.3)
        ```
        """)
        
        # Sample scalability data
        scalability_data = {
            'DLT': ['Hyperledger', 'Ethereum', 'IOTA', 'Quorum'],
            'TPS': [3000, 15, 1000, 1000],
            'Latência (s)': [1, 15, 60, 2],
            'Capacidade': [5, 4, 3, 4]
        }
        df = pd.DataFrame(scalability_data)
        st.table(df)
    
    # Energy efficiency metrics
    st.header("3. Eficiência Energética (20%)")
    with st.expander("Ver Detalhes de Eficiência Energética"):
        st.markdown("""
        ### Métricas de Eficiência
        - **Consumo por Transação**: kWh/transação
        - **Sustentabilidade**: Impacto ambiental
        - **Otimização**: Uso de recursos
        
        ### Fórmula de Normalização:
        ```python
        eficiencia = 1 - (consumo_atual - consumo_minimo) / (consumo_maximo - consumo_minimo)
        ```
        """)
        
        # Sample energy data
        energy_data = {
            'Algoritmo': ['PoW', 'PoS', 'PBFT', 'DPoS'],
            'Consumo (kWh/tx)': [885, 0.01, 0.001, 0.1]
        }
        df = pd.DataFrame(energy_data)
        fig = go.Figure(data=[go.Bar(x=df['Algoritmo'], y=df['Consumo (kWh/tx)'])])
        fig.update_layout(title="Consumo de Energia por Algoritmo de Consenso")
        st.plotly_chart(fig)
    
    # Governance metrics
    st.header("4. Governança (15%)")
    with st.expander("Ver Detalhes de Governança"):
        st.markdown("""
        ### Aspectos de Governança
        - **Controle de Acesso**: Gerenciamento de permissões
        - **Conformidade**: Regulamentações de saúde
        - **Flexibilidade**: Adaptação a mudanças
        
        ### Critérios de Avaliação:
        1. Estrutura de governança
        2. Mecanismos de votação
        3. Gestão de atualizações
        4. Resolução de conflitos
        """)
        
        # Sample governance scores
        governance_data = {
            'Critério': ['Estrutura', 'Votação', 'Atualizações', 'Conflitos'],
            'Peso': [0.3, 0.2, 0.25, 0.25],
            'Descrição': [
                'Hierarquia e responsabilidades',
                'Processo decisório',
                'Gestão de mudanças',
                'Resolução de disputas'
            ]
        }
        st.table(pd.DataFrame(governance_data))

def show_bench_comparisons():
    st.title("Comparação de Benchmarks de DLT em Saúde")
    
    # Security comparison
    st.header("1. Comparação de Segurança")
    with st.expander("Ver Análise de Segurança"):
        st.markdown("""
        ### Análise de Segurança por DLT
        Comparação das características de segurança entre diferentes DLTs
        """)
        
        # Security radar chart data
        security_metrics = {
            'Hyperledger': [0.9, 0.85, 0.95, 0.8],
            'Ethereum': [0.85, 0.8, 0.9, 0.85],
            'IOTA': [0.8, 0.85, 0.75, 0.9],
            'Quorum': [0.9, 0.8, 0.85, 0.8]
        }
        
        categories = ['Proteção de Dados', 'Privacidade', 
                     'Resistência a Ataques', 'Auditoria']
        
        fig = go.Figure()
        for dlt, scores in security_metrics.items():
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name=dlt
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title="Comparação de Segurança entre DLTs"
        )
        st.plotly_chart(fig)
    
    # Performance metrics
    st.header("2. Métricas de Performance")
    with st.expander("Ver Comparação de Performance"):
        st.markdown("""
        ### Análise Comparativa de Performance
        Comparação de métricas chave de performance entre diferentes DLTs
        """)
        
        performance_data = {
            'DLT': ['Hyperledger', 'Ethereum', 'IOTA', 'Quorum'],
            'TPS': [3000, 15, 1000, 1000],
            'Latência (s)': [1, 15, 60, 2],
            'Consumo (kWh/tx)': [0.001, 62, 0.0001, 0.002]
        }
        
        df = pd.DataFrame(performance_data)
        st.table(df)
        
        # Performance visualization
        fig = go.Figure()
        for metric in ['TPS', 'Latência (s)', 'Consumo (kWh/tx)']:
            fig.add_trace(go.Bar(
                name=metric,
                x=df['DLT'],
                y=df[metric],
                text=df[metric],
                textposition='auto',
            ))
        
        fig.update_layout(
            barmode='group',
            title="Métricas de Performance por DLT"
        )
        st.plotly_chart(fig)
    
    # Consensus comparison
    st.header("3. Comparação de Algoritmos de Consenso")
    with st.expander("Ver Análise de Consenso"):
        st.markdown("""
        ### Características dos Algoritmos de Consenso
        Comparação detalhada entre diferentes algoritmos de consenso
        """)
        
        # Create consensus comparison table
        consensus_data = []
        for alg, metrics in consensus_algorithms.items():
            row = {'Algoritmo': alg}
            row.update(metrics)
            consensus_data.append(row)
        
        df = pd.DataFrame(consensus_data)
        st.table(df)
        
        # Consensus radar chart
        fig = go.Figure()
        metrics = ['security', 'scalability', 'energy_efficiency', 'governance']
        
        for alg, data in consensus_algorithms.items():
            fig.add_trace(go.Scatterpolar(
                r=[float(data[m]) for m in metrics],
                theta=metrics,
                fill='toself',
                name=alg
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True,
            title="Comparação de Características dos Algoritmos de Consenso"
        )
        st.plotly_chart(fig)
    
    # Implementation examples
    st.header("4. Casos de Implementação")
    with st.expander("Ver Casos de Uso"):
        st.markdown("""
        ### Exemplos de Implementação na Saúde
        
        #### 1. Prontuários Eletrônicos
        - **DLT**: Hyperledger Fabric
        - **Consenso**: PBFT
        - **Benefícios**: Alta segurança e privacidade
        
        #### 2. Rastreamento de Medicamentos
        - **DLT**: VeChain
        - **Consenso**: PoA
        - **Benefícios**: Eficiência e rastreabilidade
        
        #### 3. Monitoramento IoT
        - **DLT**: IOTA
        - **Consenso**: Tangle
        - **Benefícios**: Escalabilidade e tempo real
        """)
