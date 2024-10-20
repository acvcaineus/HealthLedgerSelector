# Perguntas que o sistema faz para determinar o tipo de DLT e o algoritmo de consenso.
questions = {
    "Registros Médicos Eletrônicos (EMR)": [
        {
            "id": "privacy",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"],
            "explanation": "Esta pergunta avalia a necessidade de controle de acesso e proteção de dados sensíveis na rede.",
            "shermin_layer": "Aplicação",
            "characteristics": ["Segurança", "Governança"]
        },
        {
            "id": "interoperability",
            "text": "A interoperabilidade com outros sistemas de saúde é necessária?",
            "options": ["Sim", "Não"],
            "explanation": "Determina se a solução DLT precisa se comunicar e trocar dados com outros sistemas de saúde.",
            "shermin_layer": "Infraestrutura",
            "characteristics": ["Interoperabilidade", "Escalabilidade"]
        },
        {
            "id": "scalability",
            "text": "O sistema precisa lidar com um grande volume de registros médicos?",
            "options": ["Sim", "Não"],
            "explanation": "Avalia a necessidade de alta capacidade de armazenamento e processamento de dados.",
            "shermin_layer": "Consenso",
            "characteristics": ["Escalabilidade", "Desempenho"]
        },
        {
            "id": "access_control",
            "text": "É necessário um controle de acesso granular aos registros?",
            "options": ["Sim", "Não"],
            "explanation": "Verifica se é necessário um sistema de permissões detalhado para acesso aos registros médicos.",
            "shermin_layer": "Aplicação",
            "characteristics": ["Segurança", "Privacidade"]
        },
        {
            "id": "data_integrity",
            "text": "A integridade dos dados é uma preocupação crítica?",
            "options": ["Sim", "Não"],
            "explanation": "Avalia a necessidade de garantir que os dados não sejam alterados sem autorização.",
            "shermin_layer": "Consenso",
            "characteristics": ["Segurança", "Confiabilidade"]
        },
        {
            "id": "real_time_access",
            "text": "O acesso em tempo real aos dados é necessário?",
            "options": ["Sim", "Não"],
            "explanation": "Determina se o sistema precisa fornecer acesso imediato aos dados atualizados.",
            "shermin_layer": "Internet",
            "characteristics": ["Desempenho", "Acessibilidade"]
        }
    ],
    # ... other scenarios ...
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

# Métricas de avaliação de diferentes DLTs (valores fictícios apenas como exemplo).
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

# Cenários de aplicação para o sistema.
scenarios = {
    "Registros Médicos Eletrônicos (EMR)": "Gerenciar e proteger registros de saúde dos pacientes",
    "Cadeia de Suprimentos Farmacêutica": "Rastrear produtos farmacêuticos ao longo da cadeia de suprimentos",
    "Pesquisa Clínica": "Gerenciar dados de pesquisas clínicas de forma segura e transparente",
    "Consentimento do Paciente": "Gerenciar e verificar o consentimento do paciente para compartilhamento de dados e procedimentos",
    "Faturamento e Reivindicações": "Gerenciar processos de faturamento e reivindicações de forma eficiente e transparente"
}

# Opções de DLT e consenso para o sistema.
dlt_options = list(dlt_classes.keys())
consensus_options = list(consensus_algorithms.keys())
