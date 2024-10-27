from dlt_data import questions, dlt_classes, consensus_algorithms

consensus_groups = {
    'Alta Segurança e Controle': ['Practical Byzantine Fault Tolerance (PBFT)', 'Proof of Work (PoW)', 'Proof of Elapsed Time (PoET)'],
    'Alta Eficiência Operacional': ['Raft Consensus', 'Proof of Authority (PoA)'],
    'Escalabilidade e Governança Flexível': ['Proof of Stake (PoS)', 'Delegated Proof of Stake (DPoS)'],
    'Alta Escalabilidade em Redes IoT': ['Tangle'],
    'Alta Segurança e Descentralização de Dados Críticos': ['Proof of Work (PoW)', 'Proof of Stake (PoS)']
}

def create_evaluation_matrix(answers):
    matrix = {
        "DLT Permissionada Privada": {
            "score": 0,
            "metrics": {
                "security": float(0),
                "scalability": float(0),
                "energy_efficiency": float(0),
                "governance": float(0)
            }
        },
        "DLT Pública Permissionless": {
            "score": 0,
            "metrics": {
                "security": float(0),
                "scalability": float(0),
                "energy_efficiency": float(0),
                "governance": float(0)
            }
        },
        "DLT Permissionada Simples": {
            "score": 0,
            "metrics": {
                "security": float(0),
                "scalability": float(0),
                "energy_efficiency": float(0),
                "governance": float(0)
            }
        },
        "DLT Híbrida": {
            "score": 0,
            "metrics": {
                "security": float(0),
                "scalability": float(0),
                "energy_efficiency": float(0),
                "governance": float(0)
            }
        },
        "DLT com Consenso Delegado": {
            "score": 0,
            "metrics": {
                "security": float(0),
                "scalability": float(0),
                "energy_efficiency": float(0),
                "governance": float(0)
            }
        },
        "DLT Pública": {
            "score": 0,
            "metrics": {
                "security": float(0),
                "scalability": float(0),
                "energy_efficiency": float(0),
                "governance": float(0)
            }
        }
    }

    for question_id, answer in answers.items():
        if question_id == "privacy" and answer == "Sim":
            matrix["DLT Permissionada Privada"]["metrics"]["security"] += float(2)
            matrix["DLT Permissionada Simples"]["metrics"]["security"] += float(1)
        elif question_id == "integration" and answer == "Sim":
            matrix["DLT Híbrida"]["metrics"]["scalability"] += float(2)
            matrix["DLT com Consenso Delegado"]["metrics"]["scalability"] += float(1)
        elif question_id == "data_volume" and answer == "Sim":
            matrix["DLT Pública"]["metrics"]["scalability"] += float(2)
            matrix["DLT com Consenso Delegado"]["metrics"]["scalability"] += float(2)
        elif question_id == "energy_efficiency" and answer == "Sim":
            matrix["DLT Permissionada Simples"]["metrics"]["energy_efficiency"] += float(2)
            matrix["DLT Híbrida"]["metrics"]["energy_efficiency"] += float(1)
        elif question_id == "network_security" and answer == "Sim":
            matrix["DLT Pública Permissionless"]["metrics"]["security"] += float(2)
            matrix["DLT Permissionada Privada"]["metrics"]["security"] += float(2)
        elif question_id == "scalability" and answer == "Sim":
            matrix["DLT com Consenso Delegado"]["metrics"]["scalability"] += float(2)
            matrix["DLT Pública"]["metrics"]["scalability"] += float(2)
        elif question_id == "governance_flexibility" and answer == "Sim":
            matrix["DLT Híbrida"]["metrics"]["governance"] += float(2)
            matrix["DLT Pública Permissionless"]["metrics"]["governance"] += float(1)
        elif question_id == "interoperability" and answer == "Sim":
            matrix["DLT Híbrida"]["metrics"]["scalability"] += float(2)
            matrix["DLT Pública"]["metrics"]["scalability"] += float(1)

    # Calculate final scores
    for dlt in matrix:
        total = sum(float(value) for value in matrix[dlt]["metrics"].values())
        matrix[dlt]["score"] = float(total / len(matrix[dlt]["metrics"]))

    return matrix

def get_recommendation(answers, weights):
    evaluation_matrix = create_evaluation_matrix(answers)
    
    # Calculate weighted scores
    weighted_scores = {}
    for dlt, data in evaluation_matrix.items():
        weighted_score = (
            float(data["metrics"]["security"]) * float(weights["security"]) +
            float(data["metrics"]["scalability"]) * float(weights["scalability"]) +
            float(data["metrics"]["energy_efficiency"]) * float(weights["energy_efficiency"]) +
            float(data["metrics"]["governance"]) * float(weights["governance"])
        )
        weighted_scores[dlt] = float(weighted_score)

    # Find DLT with maximum weighted score
    recommended_dlt = max(weighted_scores.items(), key=lambda x: float(x[1]))[0]

    # Get consensus group based on DLT type
    group_mapping = {
        "DLT Permissionada Privada": "Alta Segurança e Controle",
        "DLT Pública Permissionless": "Alta Segurança e Descentralização de Dados Críticos",
        "DLT Permissionada Simples": "Alta Eficiência Operacional",
        "DLT Híbrida": "Escalabilidade e Governança Flexível",
        "DLT com Consenso Delegado": "Escalabilidade e Governança Flexível",
        "DLT Pública": "Alta Escalabilidade em Redes IoT"
    }

    recommended_group = group_mapping.get(recommended_dlt, "Alta Segurança e Controle")
    
    # Calculate confidence score and value
    confidence_scores = [float(score) for score in weighted_scores.values()]
    confidence_value = float(max(confidence_scores) - (sum(confidence_scores) / len(confidence_scores)))
    is_reliable = confidence_value > 0.7

    # Get recommended consensus algorithm
    recommended_consensus = select_final_algorithm(recommended_group, weights)

    return {
        "dlt": recommended_dlt,
        "consensus_group": recommended_group,
        "consensus": recommended_consensus,
        "algorithms": consensus_groups[recommended_group],
        "evaluation_matrix": evaluation_matrix,
        "confidence": is_reliable,
        "confidence_value": confidence_value
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
        alg_data = consensus_algorithms.get(alg, {})
        comparison_data["Segurança"][alg] = float(alg_data.get("security", 3))
        comparison_data["Escalabilidade"][alg] = float(alg_data.get("scalability", 3))
        comparison_data["Eficiência Energética"][alg] = float(alg_data.get("energy_efficiency", 3))
        comparison_data["Governança"][alg] = float(alg_data.get("governance", 3))

    return comparison_data

def select_final_algorithm(consensus_group, priorities):
    comparison_data = compare_algorithms(consensus_group)
    algorithms = consensus_groups.get(consensus_group, [])
    
    if not algorithms:
        return "No suitable algorithm found"
    
    scores = {alg: float(0) for alg in algorithms}
    
    metric_mapping = {
        "security": "Segurança",
        "scalability": "Escalabilidade",
        "energy_efficiency": "Eficiência Energética",
        "governance": "Governança"
    }
    
    for alg in algorithms:
        for metric, priority in priorities.items():
            metric_name = metric_mapping.get(metric)
            if metric_name and metric_name in comparison_data and alg in comparison_data[metric_name]:
                scores[alg] += float(comparison_data[metric_name][alg]) * float(priority)
    
    # Find algorithm with maximum score
    if scores:
        return max(scores.items(), key=lambda x: float(x[1]))[0]
    return "No suitable algorithm found"
