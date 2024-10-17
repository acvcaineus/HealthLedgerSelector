scenarios = {
    "Registros Médicos Eletrônicos": "Gerenciar e proteger registros de saúde dos pacientes",
    "Cadeia de Suprimentos": "Rastrear produtos farmacêuticos ao longo da cadeia de suprimentos",
    "Consentimento do Paciente": "Gerenciar e verificar o consentimento do paciente para compartilhamento de dados e procedimentos"
}

questions = {
    "Registros Médicos Eletrônicos": [
        {
            "id": "privacy",
            "text": "A privacidade dos dados é uma preocupação crítica?",
            "options": ["Sim", "Não"],
            "explanation": "Esta pergunta é crucial para determinar o nível de controle de acesso necessário. Em registros médicos, a privacidade é geralmente uma prioridade devido à natureza sensível das informações de saúde."
        },
        {
            "id": "high_scalability",
            "text": "Você precisa de alta escalabilidade?",
            "options": ["Sim", "Não"],
            "explanation": "A escalabilidade é importante se você espera lidar com um grande volume de registros ou transações. Isso afeta a escolha da DLT e do algoritmo de consenso para garantir que o sistema possa crescer conforme necessário."
        },
        {
            "id": "fast_transactions",
            "text": "Você precisa de processamento rápido de transações?",
            "options": ["Sim", "Não"],
            "explanation": "Transações rápidas são cruciais em ambientes médicos onde o acesso imediato às informações pode ser vital. Isso influencia a escolha do algoritmo de consenso e da estrutura DLT."
        }
    ],
    "Cadeia de Suprimentos": [
        {
            "id": "transparency",
            "text": "É necessária total transparência entre todas as partes?",
            "options": ["Sim", "Não"],
            "explanation": "A transparência é fundamental na cadeia de suprimentos farmacêutica para garantir a autenticidade e rastreabilidade dos produtos. Isso afeta a escolha entre blockchains públicos e privados."
        },
        {
            "id": "high_scalability",
            "text": "Você precisa de alta escalabilidade?",
            "options": ["Sim", "Não"],
            "explanation": "A escalabilidade é importante para lidar com um grande número de transações em uma cadeia de suprimentos complexa. Isso influencia a escolha da DLT e do algoritmo de consenso."
        },
        {
            "id": "fast_transactions",
            "text": "Você precisa de processamento rápido de transações?",
            "options": ["Sim", "Não"],
            "explanation": "Transações rápidas podem ser cruciais para eficiência logística e atualizações em tempo real. Isso afeta a escolha do algoritmo de consenso e da estrutura DLT."
        }
    ],
    "Consentimento do Paciente": [
        {
            "id": "privacy",
            "text": "A privacidade dos dados é uma preocupação crítica?",
            "options": ["Sim", "Não"],
            "explanation": "A privacidade é fundamental no gerenciamento de consentimento do paciente, pois envolve informações pessoais sensíveis. Isso influencia a escolha entre soluções mais ou menos controladas."
        },
        {
            "id": "auditability",
            "text": "É necessária total auditabilidade das mudanças de consentimento?",
            "options": ["Sim", "Não"],
            "explanation": "A auditabilidade é crucial para manter um registro imutável e verificável das mudanças de consentimento. Isso afeta a escolha da DLT e suas características de rastreamento."
        },
        {
            "id": "fast_transactions",
            "text": "Você precisa de processamento rápido de transações?",
            "options": ["Sim", "Não"],
            "explanation": "Transações rápidas podem ser importantes para atualizações em tempo real do status de consentimento. Isso influencia a escolha do algoritmo de consenso e da estrutura DLT."
        }
    ]
}

dlt_options = [
    "Blockchain Público",
    "Blockchain Permissionado",
    "Grafo Acíclico Direcionado (DAG)",
    "Blockchain Híbrido"
]

consensus_options = [
    "Prova de Trabalho (PoW)",
    "Prova de Participação (PoS)",
    "Prova de Participação Delegada (DPoS)",
    "Tolerância a Falhas Bizantinas Prática (PBFT)",
    "Prova de Autoridade (PoA)"
]
