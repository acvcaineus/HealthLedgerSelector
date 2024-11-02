# Academic references and evaluation metrics for DLTs
academic_references = {
    "Hyperledger Fabric": {
        "source": "Mehmood et al. (2025) - BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain",
        "metrics": {
            "security": float(4.8),
            "scalability": float(4.2),
            "energy_efficiency": float(4.5),
            "governance": float(4.6),
            "interoperability": float(4.3),
            "performance": float(4.4)
        },
        "use_cases": ["EMR", "Supply Chain", "Clinical Trials"],
        "academic_score": float(4.7)
    },
    "Quorum": {
        "source": "Mehmood et al. (2025) - BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain",
        "metrics": {
            "security": float(4.5),
            "scalability": float(4.0),
            "energy_efficiency": float(4.3),
            "governance": float(4.2),
            "interoperability": float(4.1),
            "performance": float(4.3)
        },
        "use_cases": ["Healthcare Data Exchange", "Patient Records"],
        "academic_score": float(4.4)
    },
    "IOTA": {
        "source": "Salim et al. (2024) - Privacy-preserving and scalable federated blockchain scheme for healthcare 4.0",
        "metrics": {
            "security": float(4.2),
            "scalability": float(4.8),
            "energy_efficiency": float(4.7),
            "governance": float(4.0),
            "interoperability": float(4.5),
            "performance": float(4.6)
        },
        "use_cases": ["IoT Healthcare", "Real-time Monitoring"],
        "academic_score": float(4.5)
    },
    "Ethereum": {
        "source": "Makhdoom et al. (2024) - PrivySeC: A secure and privacy-compliant distributed framework for personal data sharing in IoT ecosystems",
        "metrics": {
            "security": float(4.7),
            "scalability": float(3.8),
            "energy_efficiency": float(3.2),
            "governance": float(4.5),
            "interoperability": float(4.4),
            "performance": float(3.9)
        },
        "use_cases": ["Smart Contracts", "Healthcare DApps"],
        "academic_score": float(4.3)
    }
}

# Consensus algorithms with academic values and detailed metrics
consensus_algorithms = {
    "Proof of Stake (PoS)": {
        "security": float(4.5),
        "scalability": float(4.7),
        "energy_efficiency": float(4.8),
        "governance": float(4.2),
        "source": "Liu et al. (2024) - A systematic study on integrating blockchain in healthcare",
        "latency": float(4.6),
        "throughput": float(4.5),
        "decentralization": float(4.3)
    },
    "Proof of Work (PoW)": {
        "security": float(4.8),
        "scalability": float(3.2),
        "energy_efficiency": float(2.5),
        "governance": float(3.8),
        "source": "Liu et al. (2024) - A systematic study on integrating blockchain in healthcare",
        "latency": float(3.5),
        "throughput": float(3.2),
        "decentralization": float(4.8)
    },
    "Practical Byzantine Fault Tolerance (PBFT)": {
        "security": float(4.7),
        "scalability": float(4.0),
        "energy_efficiency": float(4.5),
        "governance": float(4.3),
        "source": "Mehmood et al. (2025) - BLPCA-ledger",
        "latency": float(4.4),
        "throughput": float(4.3),
        "decentralization": float(3.8)
    }
}

# Questions with updated weights and academic sources
questions = [
    {
        "id": "privacy",
        "text": "A privacidade dos dados do paciente é crítica?",
        "options": ["Sim", "Não"],
        "characteristics": ["Segurança", "Privacidade"],
        "weight": float(4.8),
        "source": "Liu et al. (2024) - Healthcare Data Security Study",
        "impact_factor": float(0.95)
    },
    {
        "id": "integration",
        "text": "É necessária integração com outros sistemas de saúde?",
        "options": ["Sim", "Não"],
        "characteristics": ["Interoperabilidade", "Escalabilidade"],
        "weight": float(4.5),
        "source": "Mehmood et al. (2025) - Healthcare Systems Integration",
        "impact_factor": float(0.85)
    },
    {
        "id": "data_volume",
        "text": "O sistema precisa lidar com grandes volumes de registros médicos?",
        "options": ["Sim", "Não"],
        "characteristics": ["Escalabilidade", "Desempenho"],
        "weight": float(4.6),
        "source": "Salim et al. (2024) - Healthcare Data Management",
        "impact_factor": float(0.90)
    },
    {
        "id": "energy_efficiency",
        "text": "A eficiência energética é uma preocupação importante?",
        "options": ["Sim", "Não"],
        "characteristics": ["Eficiência Energética", "Sustentabilidade"],
        "weight": float(4.2),
        "source": "Popoola et al. (2024) - Green Healthcare IT",
        "impact_factor": float(0.80)
    }
]

# DLT classes with updated academic validation and metrics
dlt_classes = {
    "DLT Permissionada Privada": {
        "description": "DLT privada com alta segurança e controle para dados sensíveis de saúde.",
        "academic_score": float(4.7),
        "source": "Mehmood et al. (2025)",
        "characteristics": {
            "security": float(4.8),
            "privacy": float(4.7),
            "scalability": float(4.2),
            "energy_efficiency": float(4.5)
        }
    },
    "DLT Pública Permissionless": {
        "description": "DLT pública com alta descentralização e segurança.",
        "academic_score": float(4.5),
        "source": "Liu et al. (2024)",
        "characteristics": {
            "security": float(4.6),
            "privacy": float(4.0),
            "scalability": float(4.4),
            "energy_efficiency": float(3.8)
        }
    }
}

# Evaluation matrix weights based on academic research
evaluation_weights = {
    "security": float(0.40),  # High priority for healthcare data
    "scalability": float(0.25),  # Important for system growth
    "energy_efficiency": float(0.20),  # Environmental consideration
    "governance": float(0.15)  # Operational flexibility
}
