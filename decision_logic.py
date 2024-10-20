from dlt_data import questions, dlt_classes, consensus_algorithms

def get_recommendation(answers, weights):
    score = {
        "Public Blockchain": 0,
        "Permissioned Blockchain": 0,
        "Private Blockchain": 0,
        "Hybrid Blockchain": 0,
        "Distributed Ledger": 0,
        "Consortium Blockchain": 0
    }

    # Calculate scores based on answers and weights
    for question_id, answer in answers.items():
        if question_id == "privacy" and answer == "Sim":
            score["Permissioned Blockchain"] += 2 * weights["security"]
            score["Private Blockchain"] += 2 * weights["security"]
            score["Consortium Blockchain"] += 2 * weights["security"]
        elif question_id == "integration" and answer == "Sim":
            score["Hybrid Blockchain"] += 2 * weights["scalability"]
            score["Distributed Ledger"] += 1 * weights["scalability"]
        elif question_id == "data_volume" and answer == "Sim":
            score["Distributed Ledger"] += 2 * weights["scalability"]
            score["Public Blockchain"] += 1 * weights["scalability"]
        elif question_id == "energy_efficiency" and answer == "Sim":
            score["Permissioned Blockchain"] += 1 * weights["energy_efficiency"]
            score["Private Blockchain"] += 1 * weights["energy_efficiency"]
            score["Distributed Ledger"] += 2 * weights["energy_efficiency"]
        elif question_id == "network_security" and answer == "Sim":
            score["Public Blockchain"] += 2 * weights["security"]
            score["Consortium Blockchain"] += 1 * weights["security"]
        elif question_id == "scalability" and answer == "Sim":
            score["Public Blockchain"] += 1 * weights["scalability"]
            score["Distributed Ledger"] += 2 * weights["scalability"]
        elif question_id == "governance_flexibility" and answer == "Sim":
            score["Consortium Blockchain"] += 2 * weights["governance"]
            score["Hybrid Blockchain"] += 1 * weights["governance"]
        elif question_id == "interoperability" and answer == "Sim":
            score["Hybrid Blockchain"] += 2 * weights["scalability"]
            score["Public Blockchain"] += 1 * weights["scalability"]

    # Recommend the DLT with the highest score
    recommended_dlt = max(score, key=score.get)

    # Select the appropriate consensus algorithm group
    if recommended_dlt in ["Public Blockchain", "Hybrid Blockchain"]:
        consensus_group = "Public"
    elif recommended_dlt in ["Permissioned Blockchain", "Private Blockchain", "Consortium Blockchain"]:
        consensus_group = "Permissioned"
    else:
        consensus_group = "Distributed"

    return {
        "dlt": recommended_dlt,
        "consensus_group": consensus_group
    }

def compare_algorithms(consensus_group):
    if consensus_group == "Public":
        algorithms = ["Proof of Stake (PoS)", "Proof of Work (PoW)", "Delegated Proof of Stake (DPoS)"]
    elif consensus_group == "Permissioned":
        algorithms = ["Practical Byzantine Fault Tolerance (PBFT)", "Proof of Authority (PoA)", "Raft Consensus"]
    else:
        algorithms = ["Directed Acyclic Graph (DAG)", "Tangle"]

    comparison_data = {
        "Security": {},
        "Scalability": {},
        "Energy Efficiency": {},
        "Governance": {}
    }

    for alg in algorithms:
        comparison_data["Security"][alg] = consensus_algorithms[alg].get("security", 3)
        comparison_data["Scalability"][alg] = consensus_algorithms[alg].get("scalability", 3)
        comparison_data["Energy Efficiency"][alg] = consensus_algorithms[alg].get("energy_efficiency", 3)
        comparison_data["Governance"][alg] = consensus_algorithms[alg].get("governance", 3)

    return comparison_data

def select_final_algorithm(consensus_group, percentages):
    comparison_data = compare_algorithms(consensus_group)
    algorithms = list(comparison_data["Security"].keys())
    
    scores = {alg: 0 for alg in algorithms}
    
    for alg in algorithms:
        scores[alg] += comparison_data["Security"][alg] * percentages["Segurança"] / 100
        scores[alg] += comparison_data["Scalability"][alg] * percentages["Escalabilidade"] / 100
        scores[alg] += comparison_data["Energy Efficiency"][alg] * percentages["Eficiência Energética"] / 100
        scores[alg] += comparison_data["Governance"][alg] * percentages["Governança"] / 100

    return max(scores, key=scores.get)

def get_scenario_pros_cons(scenario, dlt, consensus_algorithm):
    pros_cons = {
        "Registros Médicos Eletrônicos (EMR)": {
            "Public Blockchain": {
                "pros": [
                    "Alta transparência e auditabilidade",
                    "Descentralização total dos dados",
                    "Resistência à censura"
                ],
                "cons": [
                    "Preocupações com privacidade dos dados sensíveis",
                    "Escalabilidade limitada para grande volume de registros",
                    "Alto custo de transação em algumas redes públicas"
                ]
            },
            "Permissioned Blockchain": {
                "pros": [
                    "Maior controle sobre acesso aos dados",
                    "Melhor desempenho e escalabilidade",
                    "Conformidade com regulamentações de saúde"
                ],
                "cons": [
                    "Menor descentralização comparado a blockchains públicas",
                    "Potencial para centralização de controle",
                    "Complexidade na gestão de permissões"
                ]
            },
            "Distributed Ledger": {
                "pros": [
                    "Alta escalabilidade para grande volume de registros",
                    "Flexibilidade na estrutura de dados",
                    "Eficiência energética"
                ],
                "cons": [
                    "Menor maturidade tecnológica em comparação com blockchains",
                    "Potencial complexidade na implementação",
                    "Ecossistema menos desenvolvido"
                ]
            }
        },
        "Cadeia de Suprimentos Farmacêutica": {
            "Public Blockchain": {
                "pros": [
                    "Rastreabilidade completa e transparente",
                    "Confiança entre múltiplos stakeholders",
                    "Imutabilidade dos registros"
                ],
                "cons": [
                    "Desafios de privacidade para informações sensíveis",
                    "Possível lentidão em transações de alto volume",
                    "Custo potencialmente alto para pequenas transações"
                ]
            },
            "Permissioned Blockchain": {
                "pros": [
                    "Controle de acesso para participantes autorizados",
                    "Maior velocidade de transação",
                    "Conformidade com regulamentações farmacêuticas"
                ],
                "cons": [
                    "Menor resistência à manipulação comparado a redes públicas",
                    "Potencial para centralização",
                    "Complexidade na gestão de permissões entre múltiplas organizações"
                ]
            },
            "Distributed Ledger": {
                "pros": [
                    "Alta escalabilidade para rastreamento de grandes volumes",
                    "Flexibilidade para diferentes tipos de dados na cadeia de suprimentos",
                    "Potencial para microtransações eficientes"
                ],
                "cons": [
                    "Possível complexidade na integração com sistemas legados",
                    "Menor estabelecimento no setor farmacêutico",
                    "Desafios na interoperabilidade com outras redes"
                ]
            }
        },
        "Consentimento de Pacientes": {
            "Public Blockchain": {
                "pros": [
                    "Transparência total no histórico de consentimentos",
                    "Controle do paciente sobre seus dados",
                    "Auditabilidade pública"
                ],
                "cons": [
                    "Preocupações com a privacidade dos dados pessoais",
                    "Possível complexidade para usuários não técnicos",
                    "Desafios regulatórios em algumas jurisdições"
                ]
            },
            "Permissioned Blockchain": {
                "pros": [
                    "Melhor controle de privacidade",
                    "Conformidade com regulamentações de proteção de dados",
                    "Maior velocidade de processamento"
                ],
                "cons": [
                    "Menor transparência comparado a redes públicas",
                    "Potencial para controle centralizado das permissões",
                    "Complexidade na gestão de acessos para múltiplas instituições de saúde"
                ]
            },
            "Distributed Ledger": {
                "pros": [
                    "Alta escalabilidade para gerenciar múltiplos consentimentos",
                    "Flexibilidade para diferentes tipos de consentimento",
                    "Potencial para processamento mais rápido"
                ],
                "cons": [
                    "Possível complexidade na implementação de smart contracts",
                    "Menor familiaridade dos usuários com a tecnologia",
                    "Desafios na integração com sistemas de saúde existentes"
                ]
            }
        }
    }

    return pros_cons[scenario][dlt]["pros"], pros_cons[scenario][dlt]["cons"]

# Keep the existing functions (get_comparison_data and get_sunburst_data) unchanged
