# Perguntas que o sistema faz para determinar o tipo de DLT e o algoritmo de consenso.
questions = {
    "Registros Médicos Eletrônicos (EMR)": [
        {
            "id": "privacy",
            "text": "A privacidade dos dados do paciente é crítica?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Aplicação",
            "characteristics": ["Segurança", "Governança"],
            "next_layer": {"Sim": "Consenso", "Não": "Aplicação"}
        },
        {
            "id": "access_control",
            "text": "É necessário um controle de acesso granular aos registros?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Aplicação",
            "characteristics": ["Segurança", "Privacidade"],
            "next_layer": {"Sim": "Consenso", "Não": "Consenso"}
        },
        {
            "id": "scalability",
            "text": "O sistema precisa lidar com um grande volume de registros médicos?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Consenso",
            "characteristics": ["Escalabilidade", "Desempenho"],
            "next_layer": {"Sim": "Infraestrutura", "Não": "Consenso"}
        },
        {
            "id": "data_integrity",
            "text": "A integridade dos dados é uma preocupação crítica?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Consenso",
            "characteristics": ["Segurança", "Confiabilidade"],
            "next_layer": {"Sim": "Infraestrutura", "Não": "Infraestrutura"}
        },
        {
            "id": "interoperability",
            "text": "A interoperabilidade com outros sistemas de saúde é necessária?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Infraestrutura",
            "characteristics": ["Interoperabilidade", "Escalabilidade"],
            "next_layer": {"Sim": "Internet", "Não": "Infraestrutura"}
        },
        {
            "id": "storage_capacity",
            "text": "É necessária uma grande capacidade de armazenamento?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Infraestrutura",
            "characteristics": ["Escalabilidade", "Armazenamento"],
            "next_layer": {"Sim": "Internet", "Não": "Internet"}
        },
        {
            "id": "real_time_access",
            "text": "O acesso em tempo real aos dados é necessário?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Internet",
            "characteristics": ["Desempenho", "Acessibilidade"],
            "next_layer": {"Sim": "Aplicação", "Não": "Internet"}
        },
        {
            "id": "global_access",
            "text": "É necessário acesso global aos registros médicos?",
            "options": ["Sim", "Não"],
            "shermin_layer": "Internet",
            "characteristics": ["Acessibilidade", "Escalabilidade"],
            "next_layer": {"Sim": "Aplicação", "Não": "Aplicação"}
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

# The rest of the file remains unchanged
