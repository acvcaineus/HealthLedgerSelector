from dlt_data import questions, dlt_classes, consensus_algorithms

consensus_groups = {
    'Alta Segurança e Controle dos dados sensíveis': ['RAFT/IBFT', 'RAFT'],
    'Escalabilidade e Governança Flexível': ['RAFT/IBFT', 'PoS', 'Liquid PoS', 'Pure PoS', 'NPoS'],
    'Alta Eficiência Operacional em redes locais': ['PoA', 'Ripple Consensus Algorithm', 'SCP'],
    'Alta Escalabilidade em Redes IoT': ['Tangle'],
    'Alta Segurança e Descentralização de dados críticos': ['PoW']
}

pros_cons = {
    "Registros Médicos Eletrônicos (EMR)": {
        "Public Blockchain": {
            "pros": ["Alta transparência", "Imutabilidade dos registros"],
            "cons": ["Problemas de privacidade", "Escalabilidade limitada"],
            "algorithm_applicability": {
                "Proof of Stake (PoS)": "Adequado para EMR com menor consumo de energia",
                "Proof of Work (PoW)": "Não recomendado devido ao alto consumo de energia",
                "Practical Byzantine Fault Tolerance (PBFT)": "Bom para EMR em redes permissionadas"
            }
        },
        "Permissioned Blockchain": {
            "pros": ["Controle de acesso", "Maior privacidade"],
            "cons": ["Menor descentralização", "Potencial centralização de controle"],
            "algorithm_applicability": {
                "Proof of Authority (PoA)": "Excelente para EMR em ambientes controlados",
                "Practical Byzantine Fault Tolerance (PBFT)": "Ótimo para EMR com alta segurança"
            }
        }
    },
    "Cadeia de Suprimentos Farmacêutica": {
        "Hybrid Blockchain": {
            "pros": ["Flexibilidade", "Interoperabilidade"],
            "cons": ["Complexidade de implementação", "Potenciais vulnerabilidades de segurança"],
            "algorithm_applicability": {
                "Delegated Proof of Stake (DPoS)": "Bom para cadeias de suprimentos com múltiplos stakeholders",
                "Proof of Stake (PoS)": "Adequado para rastreamento eficiente de medicamentos"
            }
        }
    }
}

def get_recommendation(answers, weights):
    score = {
        "DLT Permissionada Privada": 0,
        "DLT Permissionada Simples": 0,
        "DLT Híbrida": 0,
        "DLT com Consenso Delegado": 0,
        "DLT Pública": 0,
        "DLT Pública Permissionless": 0
    }

    for question_id, answer in answers.items():
        if question_id == "privacy" and answer == "Sim":
            score["DLT Permissionada Privada"] += 2 * weights["security"]
            score["DLT Permissionada Simples"] += 2 * weights["security"]
        elif question_id == "integration" and answer == "Sim":
            score["DLT Híbrida"] += 2 * weights["scalability"]
            score["DLT com Consenso Delegado"] += 1 * weights["scalability"]
        elif question_id == "data_volume" and answer == "Sim":
            score["DLT com Consenso Delegado"] += 2 * weights["scalability"]
            score["DLT Pública Permissionless"] += 1 * weights["scalability"]
        elif question_id == "energy_efficiency" and answer == "Sim":
            score["DLT Permissionada Privada"] += 1 * weights["energy_efficiency"]
            score["DLT Permissionada Simples"] += 1 * weights["energy_efficiency"]
            score["DLT com Consenso Delegado"] += 2 * weights["energy_efficiency"]
        elif question_id == "network_security" and answer == "Sim":
            score["DLT Pública"] += 2 * weights["security"]
            score["DLT Pública Permissionless"] += 1 * weights["security"]
        elif question_id == "scalability" and answer == "Sim":
            score["DLT Pública Permissionless"] += 2 * weights["scalability"]
            score["DLT com Consenso Delegado"] += 2 * weights["scalability"]
        elif question_id == "governance_flexibility" and answer == "Sim":
            score["DLT Híbrida"] += 2 * weights["governance"]
            score["DLT Pública Permissionless"] += 1 * weights["governance"]
        elif question_id == "interoperability" and answer == "Sim":
            score["DLT Híbrida"] += 2 * weights["scalability"]
            score["DLT Pública Permissionless"] += 1 * weights["scalability"]

    recommended_dlt = max(score, key=score.get)

    group_scores = {
        "Alta Segurança e Controle dos dados sensíveis": weights["security"] * 2,
        "Escalabilidade e Governança Flexível": weights["scalability"] + weights["governance"],
        "Alta Eficiência Operacional em redes locais": weights["energy_efficiency"] * 2,
        "Alta Escalabilidade em Redes IoT": weights["scalability"] * 2,
        "Alta Segurança e Descentralização de dados críticos": weights["security"] + weights["decentralization"]
    }

    recommended_group = max(group_scores, key=group_scores.get)

    return {
        "dlt": recommended_dlt,
        "consensus_group": recommended_group
    }

def compare_algorithms(consensus_group):
    algorithms = consensus_groups[consensus_group]
    comparison_data = {
        "Segurança": {},
        "Escalabilidade": {},
        "Eficiência Energética": {},
        "Governança": {}
    }

    for alg in algorithms:
        if alg in consensus_algorithms:
            comparison_data["Segurança"][alg] = consensus_algorithms[alg].get("security", 3)
            comparison_data["Escalabilidade"][alg] = consensus_algorithms[alg].get("scalability", 3)
            comparison_data["Eficiência Energética"][alg] = consensus_algorithms[alg].get("energy_efficiency", 3)
            comparison_data["Governança"][alg] = consensus_algorithms[alg].get("governance", 3)

    return comparison_data

def select_final_algorithm(consensus_group, priorities):
    comparison_data = compare_algorithms(consensus_group)
    algorithms = list(comparison_data["Segurança"].keys())
    
    scores = {alg: 0 for alg in algorithms}
    
    for alg in algorithms:
        scores[alg] += comparison_data["Segurança"][alg] * priorities["Segurança"]
        scores[alg] += comparison_data["Escalabilidade"][alg] * priorities["Escalabilidade"]
        scores[alg] += comparison_data["Eficiência Energética"][alg] * priorities["Eficiência Energética"]
        scores[alg] += comparison_data["Governança"][alg] * priorities["Governança"]

    return max(scores, key=scores.get)

def get_scenario_pros_cons(dlt, consensus_algorithm):
    applicable_scenarios = {}
    for scenario, dlt_data in pros_cons.items():
        if dlt in dlt_data:
            applicable_scenarios[scenario] = {
                "pros": dlt_data[dlt]["pros"],
                "cons": dlt_data[dlt]["cons"],
                "algorithm_applicability": dlt_data[dlt]["algorithm_applicability"].get(consensus_algorithm, "Informação não disponível para este algoritmo específico.")
            }
    return applicable_scenarios
