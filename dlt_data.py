scenarios = {
    "Electronic Medical Records": "Manage and secure patient health records",
    "Supply Chain": "Track pharmaceutical products through the supply chain",
    "Patient Consent": "Manage and verify patient consent for data sharing and procedures"
}

questions = {
    "Electronic Medical Records": [
        {
            "id": "privacy",
            "text": "Is data privacy a critical concern?",
            "options": ["Yes", "No"]
        },
        {
            "id": "high_scalability",
            "text": "Do you need high scalability?",
            "options": ["Yes", "No"]
        },
        {
            "id": "fast_transactions",
            "text": "Do you need fast transaction processing?",
            "options": ["Yes", "No"]
        }
    ],
    "Supply Chain": [
        {
            "id": "transparency",
            "text": "Is full transparency across all parties required?",
            "options": ["Yes", "No"]
        },
        {
            "id": "high_scalability",
            "text": "Do you need high scalability?",
            "options": ["Yes", "No"]
        },
        {
            "id": "fast_transactions",
            "text": "Do you need fast transaction processing?",
            "options": ["Yes", "No"]
        }
    ],
    "Patient Consent": [
        {
            "id": "privacy",
            "text": "Is data privacy a critical concern?",
            "options": ["Yes", "No"]
        },
        {
            "id": "auditability",
            "text": "Is full auditability of consent changes required?",
            "options": ["Yes", "No"]
        },
        {
            "id": "fast_transactions",
            "text": "Do you need fast transaction processing?",
            "options": ["Yes", "No"]
        }
    ]
}

dlt_options = [
    "Public Blockchain",
    "Permissioned Blockchain",
    "Directed Acyclic Graph (DAG)",
    "Hybrid Blockchain"
]

consensus_options = [
    "Proof of Work (PoW)",
    "Proof of Stake (PoS)",
    "Delegated Proof of Stake (DPoS)",
    "Practical Byzantine Fault Tolerance (PBFT)",
    "Proof of Authority (PoA)"
]
