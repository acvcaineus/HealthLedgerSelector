# DLT metrics and weights for healthcare applications
dlt_metrics = {
    "Hyperledger Fabric": {"type": "DLT Permissionada Privada", "metrics": {"security": 0.85, "scalability": 0.65, "energy_efficiency": 0.80, "governance": 0.75}},
    "Corda": {"type": "DLT Permissionada Simples", "metrics": {"security": 0.70, "scalability": 0.55, "energy_efficiency": 0.75, "governance": 0.80}},
    "Quorum": {"type": "DLT Híbrida", "metrics": {"security": 0.78, "scalability": 0.70, "energy_efficiency": 0.80, "governance": 0.78}},
    "VeChain": {"type": "DLT Híbrida", "metrics": {"security": 0.75, "scalability": 0.80, "energy_efficiency": 0.85, "governance": 0.70}},
    "IOTA": {"type": "DLT com Consenso Delegado", "metrics": {"security": 0.80, "scalability": 0.85, "energy_efficiency": 0.90, "governance": 0.60}},
    "Ripple": {"type": "DLT com Consenso Delegado", "metrics": {"security": 0.78, "scalability": 0.88, "energy_efficiency": 0.70, "governance": 0.80}},
    "Stellar": {"type": "DLT com Consenso Delegado", "metrics": {"security": 0.75, "scalability": 0.82, "energy_efficiency": 0.70, "governance": 0.85}},
    "Bitcoin": {"type": "DLT Pública", "metrics": {"security": 0.95, "scalability": 0.40, "energy_efficiency": 0.35, "governance": 0.50}},
    "Ethereum (PoW)": {"type": "DLT Pública", "metrics": {"security": 0.90, "scalability": 0.50, "energy_efficiency": 0.40, "governance": 0.60}},
    "Ethereum 2.0": {"type": "DLT Pública Permissionless", "metrics": {"security": 0.85, "scalability": 0.75, "energy_efficiency": 0.65, "governance": 0.80}}
}

# Dynamic weights based on DLT type
dlt_type_weights = {
    "DLT Permissionada Privada": {"security": 0.35, "scalability": 0.20, "energy_efficiency": 0.20, "governance": 0.25},
    "DLT Permissionada Simples": {"security": 0.30, "scalability": 0.25, "energy_efficiency": 0.25, "governance": 0.20},
    "DLT Híbrida": {"security": 0.25, "scalability": 0.30, "energy_efficiency": 0.25, "governance": 0.20},
    "DLT com Consenso Delegado": {"security": 0.25, "scalability": 0.35, "energy_efficiency": 0.25, "governance": 0.15},
    "DLT Pública": {"security": 0.40, "scalability": 0.20, "energy_efficiency": 0.15, "governance": 0.25},
    "DLT Pública Permissionless": {"security": 0.30, "scalability": 0.30, "energy_efficiency": 0.20, "governance": 0.20}
}

# Questions for determining DLT type and consensus algorithm
questions = [
    {
        "id": "privacy",
        "text": "A privacidade dos dados do paciente é crítica?",
        "options": ["Sim", "Não"],
        "phase": "Aplicação",
        "characteristic": "Privacidade"
    },
    {
        "id": "integration",
        "text": "É necessária integração com outros sistemas de saúde?",
        "options": ["Sim", "Não"],
        "phase": "Aplicação",
        "characteristic": "Integração"
    },
    {
        "id": "data_volume",
        "text": "O sistema precisa lidar com grandes volumes de registros?",
        "options": ["Sim", "Não"],
        "phase": "Infraestrutura",
        "characteristic": "Volume de Dados"
    },
    {
        "id": "energy_efficiency",
        "text": "A eficiência energética é uma preocupação importante?",
        "options": ["Sim", "Não"],
        "phase": "Infraestrutura",
        "characteristic": "Eficiência Energética"
    },
    {
        "id": "network_security",
        "text": "É necessário alto nível de segurança na rede?",
        "options": ["Sim", "Não"],
        "phase": "Consenso",
        "characteristic": "Segurança"
    },
    {
        "id": "scalability",
        "text": "A escalabilidade é uma característica chave?",
        "options": ["Sim", "Não"],
        "phase": "Consenso",
        "characteristic": "Escalabilidade"
    },
    {
        "id": "governance_flexibility",
        "text": "A governança do sistema precisa ser flexível?",
        "options": ["Sim", "Não"],
        "phase": "Internet",
        "characteristic": "Governança"
    },
    {
        "id": "interoperability",
        "text": "A interoperabilidade com outros sistemas é importante?",
        "options": ["Sim", "Não"],
        "phase": "Internet",
        "characteristic": "Interoperabilidade"
    }
]

# DLT classes with descriptions
dlt_classes = {
    "Public Blockchain": "DLT pública com alta descentralização e segurança, como o Bitcoin ou Ethereum.",
    "Permissioned Blockchain": "DLT permissionada onde o controle sobre os participantes da rede é centralizado, como o Hyperledger Fabric.",
    "Private Blockchain": "DLT privada onde uma entidade tem controle completo sobre a rede.",
    "Hybrid Blockchain": "Combinação de blockchain pública e privada, aproveitando os benefícios de ambas.",
    "Distributed Ledger": "Sistemas de ledger distribuído que não utilizam necessariamente a tecnologia de blockchain.",
    "Consortium Blockchain": "Blockchain gerido por um grupo de instituições (consórcio), ideal para setores regulamentados."
}

# Consensus algorithms with descriptions
consensus_algorithms = {
    "Proof of Stake (PoS)": "Algoritmo de consenso eficiente energeticamente usado por blockchains públicos como Ethereum 2.0.",
    "Proof of Work (PoW)": "Algoritmo de consenso intensivo em energia usado por blockchains como Bitcoin.",
    "Practical Byzantine Fault Tolerance (PBFT)": "Algoritmo usado por blockchains permissionados como Hyperledger Fabric, garantindo resiliência a falhas bizantinas.",
    "Delegated Proof of Stake (DPoS)": "Um algoritmo onde validadores são eleitos pela comunidade, como em EOS ou TRON.",
    "Proof of Authority (PoA)": "Algoritmo onde validadores confiáveis são selecionados com base em sua identidade, usado por redes permissionadas.",
    "Raft Consensus": "Algoritmo de consenso simples, geralmente usado em sistemas distribuídos para alcançar consistência sem grandes requisitos de processamento.",
    "Directed Acyclic Graph (DAG)": "Uma alternativa ao blockchain, usada em redes como a IOTA para IoT e alta escalabilidade.",
    "Nominated Proof of Stake (NPoS)": "Variante de PoS usada em blockchains como o Polkadot, onde validadores são indicados por seus nominadores.",
    "Tangle": "Estrutura de consenso usada pela IOTA, especialmente para redes de IoT, oferecendo alta escalabilidade."
}
