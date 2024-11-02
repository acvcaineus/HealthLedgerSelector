# Academic references and evaluation metrics for DLTs
academic_references = {
    "Hyperledger Fabric": {
        "source": "Mehmood et al. (2025) - BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain",
        "metrics": {
            "security": float(4.8),
            "scalability": float(4.2),
            "energy_efficiency": float(4.5),
            "governance": float(4.6)
        }
    },
    "Quorum": {
        "source": "Mehmood et al. (2025) - BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain",
        "metrics": {
            "security": float(4.5),
            "scalability": float(4.0),
            "energy_efficiency": float(4.3),
            "governance": float(4.2)
        }
    },
    "IOTA": {
        "source": "Salim et al. (2024) - Privacy-preserving and scalable federated blockchain scheme for healthcare 4.0",
        "metrics": {
            "security": float(4.2),
            "scalability": float(4.8),
            "energy_efficiency": float(4.7),
            "governance": float(4.0)
        }
    },
    "Ethereum": {
        "source": "Makhdoom et al. (2024) - PrivySeC: A secure and privacy-compliant distributed framework for personal data sharing in IoT ecosystems",
        "metrics": {
            "security": float(4.7),
            "scalability": float(3.8),
            "energy_efficiency": float(3.2),
            "governance": float(4.5)
        }
    }
}

# Consensus algorithms with academic values
consensus_algorithms = {
    "Proof of Stake (PoS)": {
        "security": float(4.5),
        "scalability": float(4.7),
        "energy_efficiency": float(4.8),
        "governance": float(4.2),
        "source": "Liu et al. (2024) - A systematic study on integrating blockchain in healthcare"
    },
    "Proof of Work (PoW)": {
        "security": float(4.8),
        "scalability": float(3.2),
        "energy_efficiency": float(2.5),
        "governance": float(3.8),
        "source": "Liu et al. (2024) - A systematic study on integrating blockchain in healthcare"
    },
    "Practical Byzantine Fault Tolerance (PBFT)": {
        "security": float(4.7),
        "scalability": float(4.0),
        "energy_efficiency": float(4.5),
        "governance": float(4.3),
        "source": "Mehmood et al. (2025) - BLPCA-ledger"
    },
    "Delegated Proof of Stake (DPoS)": {
        "security": float(4.3),
        "scalability": float(4.6),
        "energy_efficiency": float(4.5),
        "governance": float(4.0),
        "source": "Popoola et al. (2024) - Security and privacy in smart home healthcare"
    },
    "Proof of Authority (PoA)": {
        "security": float(4.4),
        "scalability": float(4.5),
        "energy_efficiency": float(4.7),
        "governance": float(3.8),
        "source": "Nawaz et al. (2024) - Hyperledger sawtooth based supply chain"
    },
    "Raft Consensus": {
        "security": float(4.2),
        "scalability": float(4.4),
        "energy_efficiency": float(4.6),
        "governance": float(4.0),
        "source": "Mehmood et al. (2025) - BLPCA-ledger"
    },
    "Directed Acyclic Graph (DAG)": {
        "security": float(4.3),
        "scalability": float(4.8),
        "energy_efficiency": float(4.6),
        "governance": float(3.9),
        "source": "Salim et al. (2024) - Privacy-preserving and scalable federated blockchain"
    },
    "Nominated Proof of Stake (NPoS)": {
        "security": float(4.4),
        "scalability": float(4.5),
        "energy_efficiency": float(4.7),
        "governance": float(4.2),
        "source": "Javed et al. (2024) - Mutual authentication enabled trust model"
    },
    "Tangle": {
        "security": float(4.2),
        "scalability": float(4.9),
        "energy_efficiency": float(4.8),
        "governance": float(3.8),
        "source": "Salim et al. (2024) - Privacy-preserving and scalable federated blockchain"
    }
}

# Questions for determining DLT type and consensus algorithm
questions = [
    {
        "id": "privacy",
        "text": "A privacidade dos dados do paciente é crítica?",
        "options": ["Sim", "Não"],
        "characteristics": ["Segurança", "Privacidade"],
        "weight": float(4.8),  # Updated based on academic research
        "source": "Liu et al. (2024)"
    },
    {
        "id": "integration",
        "text": "É necessária integração com outros sistemas de saúde?",
        "options": ["Sim", "Não"],
        "characteristics": ["Interoperabilidade", "Escalabilidade"],
        "weight": float(4.5),
        "source": "Mehmood et al. (2025)"
    },
    {
        "id": "data_volume",
        "text": "O sistema precisa lidar com grandes volumes de registros médicos?",
        "options": ["Sim", "Não"],
        "characteristics": ["Escalabilidade", "Desempenho"],
        "weight": float(4.6),
        "source": "Salim et al. (2024)"
    },
    {
        "id": "energy_efficiency",
        "text": "A eficiência energética é uma preocupação importante?",
        "options": ["Sim", "Não"],
        "characteristics": ["Eficiência Energética", "Sustentabilidade"],
        "weight": float(4.2),
        "source": "Popoola et al. (2024)"
    }
]

# DLT classes with academic validation
dlt_classes = {
    "DLT Permissionada Privada": {
        "description": "DLT privada com alta segurança e controle para dados sensíveis de saúde.",
        "academic_score": float(4.7),
        "source": "Mehmood et al. (2025)"
    },
    "DLT Pública Permissionless": {
        "description": "DLT pública com alta descentralização e segurança.",
        "academic_score": float(4.5),
        "source": "Liu et al. (2024)"
    },
    "DLT Permissionada Simples": {
        "description": "DLT permissionada eficiente para redes locais de saúde.",
        "academic_score": float(4.4),
        "source": "Nawaz et al. (2024)"
    },
    "DLT Híbrida": {
        "description": "Combinação de características públicas e privadas para flexibilidade.",
        "academic_score": float(4.6),
        "source": "Makhdoom et al. (2024)"
    },
    "DLT com Consenso Delegado": {
        "description": "DLT com validadores eleitos para maior escalabilidade.",
        "academic_score": float(4.3),
        "source": "Javed et al. (2024)"
    },
    "DLT Pública": {
        "description": "DLT totalmente pública para máxima transparência.",
        "academic_score": float(4.2),
        "source": "Liu et al. (2024)"
    }
}
