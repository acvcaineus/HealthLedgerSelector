# Consensus algorithms with numeric values
consensus_algorithms = {
    "Proof of Stake (PoS)": {
        "security": float(4.0),
        "scalability": float(5.0),
        "energy_efficiency": float(5.0),
        "governance": float(4.0)
    },
    "Proof of Work (PoW)": {
        "security": float(5.0),
        "scalability": float(2.0),
        "energy_efficiency": float(1.0),
        "governance": float(3.0)
    },
    "Practical Byzantine Fault Tolerance (PBFT)": {
        "security": float(5.0),
        "scalability": float(3.0),
        "energy_efficiency": float(4.0),
        "governance": float(4.0)
    },
    "Delegated Proof of Stake (DPoS)": {
        "security": float(4.0),
        "scalability": float(5.0),
        "energy_efficiency": float(4.0),
        "governance": float(3.0)
    },
    "Proof of Authority (PoA)": {
        "security": float(4.0),
        "scalability": float(4.0),
        "energy_efficiency": float(5.0),
        "governance": float(3.0)
    },
    "Raft Consensus": {
        "security": float(3.0),
        "scalability": float(4.0),
        "energy_efficiency": float(5.0),
        "governance": float(3.0)
    },
    "Directed Acyclic Graph (DAG)": {
        "security": float(4.0),
        "scalability": float(5.0),
        "energy_efficiency": float(4.0),
        "governance": float(3.0)
    },
    "Nominated Proof of Stake (NPoS)": {
        "security": float(4.0),
        "scalability": float(4.0),
        "energy_efficiency": float(5.0),
        "governance": float(4.0)
    },
    "Tangle": {
        "security": float(4.0),
        "scalability": float(5.0),
        "energy_efficiency": float(5.0),
        "governance": float(3.0)
    }
}

# Questions for determining DLT type and consensus algorithm
questions = [
    {
        "id": "privacy",
        "phase": "Aplicação",
        "text": "A privacidade dos dados do paciente é crítica?",
        "options": ["Sim", "Não"],
        "characteristic": "Segurança",
        "tooltip": "Considere os requisitos de privacidade dos dados dos pacientes"
    },
    {
        "id": "integration",
        "phase": "Aplicação",
        "text": "É necessária integração com outros sistemas de saúde?",
        "options": ["Sim", "Não"],
        "characteristic": "Interoperabilidade",
        "tooltip": "Avalie a necessidade de integração com sistemas existentes"
    },
    {
        "id": "data_volume",
        "phase": "Consenso",
        "text": "O sistema precisa lidar com grandes volumes de registros médicos?",
        "options": ["Sim", "Não"],
        "characteristic": "Escalabilidade",
        "tooltip": "Considere o volume de dados que o sistema precisará processar"
    },
    {
        "id": "energy_efficiency",
        "phase": "Infraestrutura",
        "text": "A eficiência energética é uma preocupação importante?",
        "options": ["Sim", "Não"],
        "characteristic": "Eficiência Energética",
        "tooltip": "Avalie o impacto do consumo de energia do sistema"
    }
]

# DLT classes that can be recommended by the system
dlt_classes = {
    "DLT Permissionada Privada": "DLT privada com alta segurança e controle para dados sensíveis de saúde.",
    "DLT Pública Permissionless": "DLT pública com alta descentralização e segurança.",
    "DLT Permissionada Simples": "DLT permissionada eficiente para redes locais de saúde.",
    "DLT Híbrida": "Combinação de características públicas e privadas para flexibilidade.",
    "DLT com Consenso Delegado": "DLT com validadores eleitos para maior escalabilidade.",
    "DLT Pública": "DLT totalmente pública para máxima transparência."
}
