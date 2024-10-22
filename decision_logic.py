from dlt_data import questions, dlt_classes, consensus_algorithms

consensus_groups = {
    'Alta Segurança e Controle': ['PBFT', 'PoW'],
    'Alta Eficiência Operacional': ['RAFT', 'PoA'],
    'Escalabilidade e Governança Flexível': ['PoS', 'DPoS'],
    'Alta Escalabilidade em Redes IoT': ['Tangle'],
    'Alta Segurança e Descentralização de Dados Críticos': ['PoW', 'PoS']
}

def create_evaluation_matrix(answers):
    matrix = {
        "DLT Permissionada Privada": 0,
        "DLT Pública Permissionless": 0,
        "DLT Permissionada Simples": 0,
        "DLT Híbrida": 0,
        "DLT com Consenso Delegado": 0,
        "DLT Pública": 0
    }

    for question_id, answer in answers.items():
        if question_id == "privacy" and answer == "Sim":
            matrix["DLT Permissionada Privada"] += 2
        elif question_id == "integration" and answer == "Sim":
            matrix["DLT Híbrida"] += 2
        elif question_id == "data_volume" and answer == "Sim":
            matrix["DLT Pública"] += 2
        elif question_id == "energy_efficiency" and answer == "Sim":
            matrix["DLT Permissionada Simples"] += 2
        elif question_id == "network_security" and answer == "Sim":
            matrix["DLT Pública Permissionless"] += 2
        elif question_id == "scalability" and answer == "Sim":
            matrix["DLT com Consenso Delegado"] += 2
        elif question_id == "governance_flexibility" and answer == "Sim":
            matrix["DLT Híbrida"] += 2
        elif question_id == "interoperability" and answer == "Sim":
            matrix["DLT Pública"] += 2

    return matrix

def get_recommendation(answers, weights):
    evaluation_matrix = create_evaluation_matrix(answers)
    score = {dlt: value * weights["security"] for dlt, value in evaluation_matrix.items()}

    for question_id, answer in answers.items():
        if question_id == "scalability" and answer == "Sim":
            score["DLT Pública"] += weights["scalability"]
            score["DLT com Consenso Delegado"] += weights["scalability"]
        elif question_id == "energy_efficiency" and answer == "Sim":
            score["DLT Permissionada Simples"] += weights["energy_efficiency"]
        elif question_id == "governance_flexibility" and answer == "Sim":
            score["DLT Híbrida"] += weights["governance"]

    recommended_dlt = max(score, key=score.get)

    group_scores = {
        "Alta Segurança e Controle": weights["security"] * 2,
        "Alta Eficiência Operacional": weights["energy_efficiency"] * 2,
        "Escalabilidade e Governança Flexível": weights["scalability"] + weights["governance"],
        "Alta Escalabilidade em Redes IoT": weights["scalability"] * 2,
        "Alta Segurança e Descentralização de Dados Críticos": weights["security"] + weights.get("decentralization", 0)
    }

    recommended_group = max(group_scores, key=group_scores.get)

    return {
        "dlt": recommended_dlt,
        "consensus_group": recommended_group,
        "consensus": select_final_algorithm(recommended_group, weights),
        "algorithms": consensus_groups[recommended_group],
        "evaluation_matrix": evaluation_matrix
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
        for metric in comparison_data.keys():
            comparison_data[metric][alg] = consensus_algorithms.get(alg, {}).get(metric.lower().replace(" ", "_"), 3)

    return comparison_data

def select_final_algorithm(consensus_group, priorities):
    comparison_data = compare_algorithms(consensus_group)
    algorithms = list(comparison_data.get("Segurança", {}).keys())
    
    scores = {alg: 0 for alg in algorithms}
    
    for alg in algorithms:
        for metric, priority in priorities.items():
            metric_name = metric.capitalize()
            if metric_name in comparison_data and alg in comparison_data[metric_name]:
                scores[alg] += comparison_data[metric_name][alg] * priority
    
    if not scores:
        return "No suitable algorithm found"
    
    return max(scores, key=scores.get)