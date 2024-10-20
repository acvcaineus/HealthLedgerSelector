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
        }
    ],
    # ... other scenarios ...
}

# The rest of the file remains unchanged
