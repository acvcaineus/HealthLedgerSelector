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

    recommended_dlt = max(score, key=score.get)

    # Update consensus group selection based on prioritized characteristics
    if weights["security"] > weights["scalability"] and weights["security"] > weights["energy_efficiency"]:
        if recommended_dlt in ["Public Blockchain", "Hybrid Blockchain"]:
            consensus_group = "Public_Security"
        else:
            consensus_group = "Permissioned_Security"
    elif weights["scalability"] > weights["security"] and weights["scalability"] > weights["energy_efficiency"]:
        if recommended_dlt in ["Public Blockchain", "Hybrid Blockchain"]:
            consensus_group = "Public_Scalability"
        else:
            consensus_group = "Permissioned_Scalability"
    elif weights["energy_efficiency"] > weights["security"] and weights["energy_efficiency"] > weights["scalability"]:
        consensus_group = "Energy_Efficient"
    else:
        consensus_group = "Balanced"

    return {
        "dlt": recommended_dlt,
        "consensus_group": consensus_group
    }

def compare_algorithms(consensus_group):
    if consensus_group == "Public_Security":
        algorithms = ["Proof of Work (PoW)", "Delegated Proof of Stake (DPoS)"]
    elif consensus_group == "Public_Scalability":
        algorithms = ["Proof of Stake (PoS)", "Delegated Proof of Stake (DPoS)"]
    elif consensus_group == "Permissioned_Security":
        algorithms = ["Practical Byzantine Fault Tolerance (PBFT)", "Proof of Authority (PoA)"]
    elif consensus_group == "Permissioned_Scalability":
        algorithms = ["Proof of Authority (PoA)", "Raft Consensus"]
    elif consensus_group == "Energy_Efficient":
        algorithms = ["Proof of Stake (PoS)", "Directed Acyclic Graph (DAG)", "Tangle"]
    else:  # Balanced
        algorithms = ["Proof of Stake (PoS)", "Practical Byzantine Fault Tolerance (PBFT)", "Directed Acyclic Graph (DAG)"]

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

def select_final_algorithm(consensus_group, priorities):
    comparison_data = compare_algorithms(consensus_group)
    algorithms = list(comparison_data["Security"].keys())
    
    scores = {alg: 0 for alg in algorithms}
    
    for alg in algorithms:
        scores[alg] += comparison_data["Security"][alg] * priorities["Segurança"]
        scores[alg] += comparison_data["Scalability"][alg] * priorities["Escalabilidade"]
        scores[alg] += comparison_data["Energy Efficiency"][alg] * priorities["Eficiência Energética"]
        scores[alg] += comparison_data["Governance"][alg] * priorities["Governança"]

    return max(scores, key=scores.get)

def get_scenario_pros_cons(scenario, dlt, consensus_algorithm):
    # The content of this function remains the same as before
    # ...

    return pros_cons[scenario][dlt]["pros"], pros_cons[scenario][dlt]["cons"], pros_cons[scenario][dlt]["algorithm_applicability"].get(consensus_algorithm, "Informação não disponível para este algoritmo específico.")
