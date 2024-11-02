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
        "text": "A privacidade dos dados do paciente é crítica?",
        "options": ["Sim", "Não"],
        "characteristics": ["Segurança", "Privacidade"]
    },
    {
        "id": "integration",
        "text": "É necessária integração com outros sistemas de saúde?",
        "options": ["Sim", "Não"],
        "characteristics": ["Interoperabilidade", "Escalabilidade"]
    },
    {
        "id": "data_volume",
        "text": "O sistema precisa lidar com grandes volumes de registros médicos?",
        "options": ["Sim", "Não"],
        "characteristics": ["Escalabilidade", "Desempenho"]
    },
    {
        "id": "energy_efficiency",
        "text": "A eficiência energética é uma preocupação importante?",
        "options": ["Sim", "Não"],
        "characteristics": ["Eficiência Energética", "Sustentabilidade"]
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
