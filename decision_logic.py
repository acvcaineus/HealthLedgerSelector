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

# Keep the existing functions (get_comparison_data and get_sunburst_data) unchanged
