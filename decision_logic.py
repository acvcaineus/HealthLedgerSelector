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
            score["Permissioned Blockchain"] += 2 * weights["segurança"]
            score["Private Blockchain"] += 2 * weights["segurança"]
            score["Consortium Blockchain"] += 2 * weights["segurança"]
        elif question_id == "integration" and answer == "Sim":
            score["Hybrid Blockchain"] += 2 * weights["escalabilidade"]
            score["Distributed Ledger"] += 1 * weights["escalabilidade"]
        elif question_id == "data_volume" and answer == "Sim":
            score["Distributed Ledger"] += 2 * weights["escalabilidade"]
            score["Public Blockchain"] += 1 * weights["escalabilidade"]
        elif question_id == "energy_efficiency" and answer == "Sim":
            score["Permissioned Blockchain"] += 1 * weights["eficiência energética"]
            score["Private Blockchain"] += 1 * weights["eficiência energética"]
            score["Distributed Ledger"] += 2 * weights["eficiência energética"]
        elif question_id == "network_security" and answer == "Sim":
            score["Public Blockchain"] += 2 * weights["segurança"]
            score["Consortium Blockchain"] += 1 * weights["segurança"]
        elif question_id == "scalability" and answer == "Sim":
            score["Public Blockchain"] += 1 * weights["escalabilidade"]
            score["Distributed Ledger"] += 2 * weights["escalabilidade"]
        elif question_id == "governance_flexibility" and answer == "Sim":
            score["Consortium Blockchain"] += 2 * weights["governança"]
            score["Hybrid Blockchain"] += 1 * weights["governança"]
        elif question_id == "interoperability" and answer == "Sim":
            score["Hybrid Blockchain"] += 2 * weights["escalabilidade"]
            score["Public Blockchain"] += 1 * weights["escalabilidade"]

    recommended_dlt = max(score, key=score.get)

    # Update consensus group selection based on prioritized characteristics
    if weights["segurança"] > weights["escalabilidade"] and weights["segurança"] > weights["eficiência energética"]:
        if recommended_dlt in ["Public Blockchain", "Hybrid Blockchain"]:
            consensus_group = "Public_Security"
        else:
            consensus_group = "Permissioned_Security"
    elif weights["escalabilidade"] > weights["segurança"] and weights["escalabilidade"] > weights["eficiência energética"]:
        if recommended_dlt in ["Public Blockchain", "Hybrid Blockchain"]:
            consensus_group = "Public_Scalability"
        else:
            consensus_group = "Permissioned_Scalability"
    elif weights["eficiência energética"] > weights["segurança"] and weights["eficiência energética"] > weights["escalabilidade"]:
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
        "Segurança": {},
        "Escalabilidade": {},
        "Eficiência Energética": {},
        "Governança": {}
    }

    for alg in algorithms:
        comparison_data["Segurança"][alg] = consensus_algorithms[alg].get("segurança", 3)
        comparison_data["Escalabilidade"][alg] = consensus_algorithms[alg].get("escalabilidade", 3)
        comparison_data["Eficiência Energética"][alg] = consensus_algorithms[alg].get("eficiência energética", 3)
        comparison_data["Governança"][alg] = consensus_algorithms[alg].get("governança", 3)

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

def get_scenario_pros_cons(scenario, dlt, consensus_algorithm):
    # The content of this function remains the same as before
    # ...

    return pros_cons[scenario][dlt]["pros"], pros_cons[scenario][dlt]["cons"], pros_cons[scenario][dlt]["algorithm_applicability"].get(consensus_algorithm, "Informação não disponível para este algoritmo específico.")
