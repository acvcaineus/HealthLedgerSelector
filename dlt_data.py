# Scenarios for DLT application in healthcare
scenarios = {
    "Registros Médicos Eletrônicos (EMR)": "Implementação de DLT para gerenciar registros médicos eletrônicos de forma segura e interoperável.",
    "Cadeia de Suprimentos Farmacêutica": "Uso de DLT para rastrear e autenticar medicamentos ao longo da cadeia de suprimentos.",
    "Consentimento de Pacientes": "Aplicação de DLT para gerenciar consentimentos de pacientes de forma transparente e auditável."
}

# Questions based on the Shermin stack layers
questions = {
    "Registros Médicos Eletrônicos (EMR)": [
        {
            "id": "privacy",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Aplicação",
            "characteristics": ["Segurança", "Privacidade"],
            "next_layer": {"Sim": "Consenso", "Não": "Aplicação"}
        },
        {
            "id": "integration",
            "text": "É necessária integração com outros sistemas de saúde?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Aplicação",
            "characteristics": ["Interoperabilidade", "Escalabilidade"],
            "next_layer": {"Sim": "Consenso", "Não": "Consenso"}
        },
        {
            "id": "data_volume",
            "text": "O sistema precisa lidar com grandes volumes de registros médicos?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Consenso",
            "characteristics": ["Escalabilidade", "Desempenho"],
            "next_layer": {"Sim": "Infraestrutura", "Não": "Consenso"}
        },
        {
            "id": "energy_efficiency",
            "text": "A eficiência energética é uma preocupação importante?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Consenso",
            "characteristics": ["Eficiência Energética", "Sustentabilidade"],
            "next_layer": {"Sim": "Infraestrutura", "Não": "Infraestrutura"}
        },
        {
            "id": "network_security",
            "text": "A segurança da rede é uma prioridade crítica?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Infraestrutura",
            "characteristics": ["Segurança", "Confiabilidade"],
            "next_layer": {"Sim": "Internet", "Não": "Infraestrutura"}
        },
        {
            "id": "scalability",
            "text": "A escalabilidade é uma característica chave para o sucesso do sistema?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Infraestrutura",
            "characteristics": ["Escalabilidade", "Desempenho"],
            "next_layer": {"Sim": "Internet", "Não": "Internet"}
        },
        {
            "id": "governance_flexibility",
            "text": "É necessária flexibilidade na governança da rede?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Internet",
            "characteristics": ["Governança", "Flexibilidade"],
            "next_layer": {"Sim": "Aplicação", "Não": "Internet"}
        },
        {
            "id": "interoperability",
            "text": "A interoperabilidade com outras redes é importante?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Internet",
            "characteristics": ["Interoperabilidade", "Conectividade"],
            "next_layer": {"Sim": "Aplicação", "Não": "Aplicação"}
        }
    ]
}

# DLT classes that can be recommended by the system
dlt_classes = {
    "Public Blockchain": "DLT pública com alta descentralização e segurança, como o Bitcoin ou Ethereum.",
    "Permissioned Blockchain": "DLT permissionada onde o controle sobre os participantes da rede é centralizado, como o Hyperledger Fabric.",
    "Private Blockchain": "DLT privada onde uma entidade tem controle completo sobre a rede.",
    "Hybrid Blockchain": "Combinação de blockchain pública e privada, aproveitando os benefícios de ambas.",
    "Distributed Ledger": "Sistemas de ledger distribuído que não utilizam necessariamente a tecnologia de blockchain.",
    "Consortium Blockchain": "Blockchain gerido por um grupo de instituições (consórcio), ideal para setores regulamentados."
}

# Consensus algorithms that can be recommended
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
