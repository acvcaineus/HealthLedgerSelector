# Perguntas que o sistema faz para determinar o tipo de DLT e o algoritmo de consenso.
questions = {
    "Registros Médicos Eletrônicos": [
        {
            "id": "privacy",
            "text": "A privacidade é crítica?",
            "options": ["Sim", "Não"],
            "explanation": "Esta pergunta avalia a necessidade de controle de acesso e proteção de dados sensíveis na rede."
        },
        {
            "id": "integration",
            "text": "A integração com outros sistemas é necessária?",
            "options": ["Sim", "Não"],
            "explanation": "Determina se a solução DLT precisa se comunicar e interoperar com sistemas externos."
        },
        {
            "id": "data_volume",
            "text": "A rede lida com grandes volumes de dados?",
            "options": ["Sim", "Não"],
            "explanation": "Avalia a necessidade de alta capacidade de armazenamento e processamento de dados."
        },
        {
            "id": "energy_efficiency",
            "text": "A eficiência energética é importante?",
            "options": ["Sim", "Não"],
            "explanation": "Considera o impacto ambiental e os custos operacionais relacionados ao consumo de energia."
        }
    ],
    "Cadeia de Suprimentos": [
        {
            "id": "network_security",
            "text": "A segurança da rede é alta?",
            "options": ["Sim", "Não"],
            "explanation": "Avalia a necessidade de proteção contra ataques e manipulação de dados."
        },
        {
            "id": "scalability",
            "text": "A escalabilidade é chave para o sucesso?",
            "options": ["Sim", "Não"],
            "explanation": "Determina se a rede precisa crescer e lidar com um aumento significativo no número de transações."
        },
        {
            "id": "governance_flexibility",
            "text": "A governança da rede precisa ser flexível?",
            "options": ["Sim", "Não"],
            "explanation": "Avalia a necessidade de adaptar as regras e protocolos da rede ao longo do tempo."
        },
        {
            "id": "interoperability",
            "text": "A interoperabilidade com outras redes é importante?",
            "options": ["Sim", "Não"],
            "explanation": "Considera a necessidade de comunicação e troca de dados com outras redes blockchain ou sistemas externos."
        }
    ],
    "Consentimento do Paciente": [
        {
            "id": "privacy",
            "text": "A privacidade é crítica?",
            "options": ["Sim", "Não"],
            "explanation": "Esta pergunta avalia a necessidade de controle de acesso e proteção de dados sensíveis na rede."
        },
        {
            "id": "integration",
            "text": "A integração com outros sistemas é necessária?",
            "options": ["Sim", "Não"],
            "explanation": "Determina se a solução DLT precisa se comunicar e interoperar com sistemas externos."
        },
        {
            "id": "network_security",
            "text": "A segurança da rede é alta?",
            "options": ["Sim", "Não"],
            "explanation": "Avalia a necessidade de proteção contra ataques e manipulação de dados."
        },
        {
            "id": "governance_flexibility",
            "text": "A governança da rede precisa ser flexível?",
            "options": ["Sim", "Não"],
            "explanation": "Avalia a necessidade de adaptar as regras e protocolos da rede ao longo do tempo."
        }
    ]
}

# Classes de DLT (Distributed Ledger Technology) que podem ser recomendadas pelo sistema.
dlt_classes = {
    "Public Blockchain": "DLT pública com alta descentralização e segurança, como o Bitcoin ou Ethereum.",
    "Permissioned Blockchain": "DLT permissionada onde o controle sobre os participantes da rede é centralizado, como o Hyperledger Fabric.",
    "Private Blockchain": "DLT privada onde uma entidade tem controle completo sobre a rede.",
    "Hybrid Blockchain": "Combinação de blockchain pública e privada, aproveitando os benefícios de ambas.",
    "Distributed Ledger": "Sistemas de ledger distribuído que não utilizam necessariamente a tecnologia de blockchain.",
    "Consortium Blockchain": "Blockchain gerido por um grupo de instituições (consórcio), ideal para setores regulamentados."
}

# Algoritmos de consenso que podem ser recomendados.
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

# Métricas de avaliação de diferentes DLTs
metrics = {
    "Tempo de confirmação de transação (segundos)": {
        "Hyperledger Fabric (PBFT)": 1,
        "Bitcoin (PoW)": 600,
        "Ethereum (PoW/PoS)": 15,
        "Quorum (RAFT)": 2,
        "VeChain (PoA)": 10,
        "Ethereum 2.0 (PoS)": 12,
        "EOS (DPoS)": 0.5,
        "IOTA": 60
    },
    "Throughput (transações por segundo)": {
        "Hyperledger Fabric (PBFT)": 3000,
        "Bitcoin (PoW)": 7,
        "Ethereum (PoW/PoS)": 15,
        "Quorum (RAFT)": 1000,
        "VeChain (PoA)": 2000,
        "Ethereum 2.0 (PoS)": 100000,
        "EOS (DPoS)": 4000,
        "IOTA": 1000
    },
    "Custo por transação (USD)": {
        "Hyperledger Fabric (PBFT)": 0.001,
        "Bitcoin (PoW)": 1.5,
        "Ethereum (PoW/PoS)": 0.5,
        "Quorum (RAFT)": 0.001,
        "VeChain (PoA)": 0.005,
        "Ethereum 2.0 (PoS)": 0.01,
        "EOS (DPoS)": 0.001,
        "IOTA": 0
    },
    "Consumo de energia (kWh por transação)": {
        "Hyperledger Fabric (PBFT)": 0.001,
        "Bitcoin (PoW)": 885,
        "Ethereum (PoW/PoS)": 62,
        "Quorum (RAFT)": 0.002,
        "VeChain (PoA)": 0.005,
        "Ethereum 2.0 (PoS)": 0.01,
        "EOS (DPoS)": 0.1,
        "IOTA": 0.0001
    },
    "Nível de descentralização (1-10)": {
        "Hyperledger Fabric (PBFT)": 5,
        "Bitcoin (PoW)": 10,
        "Ethereum (PoW/PoS)": 9,
        "Quorum (RAFT)": 4,
        "VeChain (PoA)": 6,
        "Ethereum 2.0 (PoS)": 8,
        "EOS (DPoS)": 7,
        "IOTA": 8
    },
    "Flexibilidade de programação (1-10)": {
        "Hyperledger Fabric (PBFT)": 9,
        "Bitcoin (PoW)": 3,
        "Ethereum (PoW/PoS)": 10,
        "Quorum (RAFT)": 8,
        "VeChain (PoA)": 7,
        "Ethereum 2.0 (PoS)": 10,
        "EOS (DPoS)": 9,
        "IOTA": 6
    },
    "Interoperabilidade (1-10)": {
        "Hyperledger Fabric (PBFT)": 8,
        "Bitcoin (PoW)": 4,
        "Ethereum (PoW/PoS)": 7,
        "Quorum (RAFT)": 6,
        "VeChain (PoA)": 7,
        "Ethereum 2.0 (PoS)": 9,
        "EOS (DPoS)": 8,
        "IOTA": 6
    },
    "Resistência a ataques quânticos (1-10)": {
        "Hyperledger Fabric (PBFT)": 7,
        "Bitcoin (PoW)": 5,
        "Ethereum (PoW/PoS)": 6,
        "Quorum (RAFT)": 7,
        "VeChain (PoA)": 7,
        "Ethereum 2.0 (PoS)": 8,
        "EOS (DPoS)": 7,
        "IOTA": 9
    }
}

# Adding the 'scenarios' variable
scenarios = {
    "Registros Médicos Eletrônicos": "Gerenciar e proteger registros de saúde dos pacientes",
    "Cadeia de Suprimentos": "Rastrear produtos farmacêuticos ao longo da cadeia de suprimentos",
    "Consentimento do Paciente": "Gerenciar e verificar o consentimento do paciente para compartilhamento de dados e procedimentos"
}

# Adding the 'dlt_options' and 'consensus_options' variables
dlt_options = list(dlt_classes.keys())
consensus_options = list(consensus_algorithms.keys())
