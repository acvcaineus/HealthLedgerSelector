from dlt_data import questions, dlt_classes, consensus_algorithms
from metrics import calcular_gini, calcular_entropia, calcular_confiabilidade_recomendacao

consensus_groups = {
    'Alta Segurança e Controle': ['PBFT', 'PoW'],
    'Alta Eficiência Operacional': ['RAFT', 'PoA'],
    'Escalabilidade e Governança Flexível': ['PoS', 'DPoS'],
    'Alta Escalabilidade em Redes IoT': ['Tangle'],
    'Alta Segurança e Descentralização de Dados Críticos': ['PoW', 'PoS']
}

academic_scores = {
    "Hyperledger Fabric": {
        "score": 4.5,
        "citations": 128,
        "reference": "Mehmood et al. (2025) - BLPCA-ledger",
        "validation": "Implementado em hospitais e sistemas de saúde"
    },
    "VeChain": {
        "score": 4.2,
        "citations": 89,
        "reference": "Popoola et al. (2024)",
        "validation": "Usado em cadeias de suprimentos médicos"
    },
    "Quorum": {
        "score": 4.0,
        "citations": 76,
        "reference": "Mehmood et al. (2025)",
        "validation": "Testado em redes hospitalares"
    },
    "IOTA": {
        "score": 4.3,
        "citations": 95,
        "reference": "Salim et al. (2024)",
        "validation": "Implementado em sistemas IoT de saúde"
    }
}

def create_evaluation_matrix(answers):
    matrix = {
        "DLT Permissionada Privada": {
            "score": 0,
            "metrics": {
                "security": 0,
                "scalability": 0,
                "energy_efficiency": 0,
                "governance": 0,
                "academic_validation": 0
            }
        },
        "DLT Pública Permissionless": {
            "score": 0,
            "metrics": {
                "security": 0,
                "scalability": 0,
                "energy_efficiency": 0,
                "governance": 0,
                "academic_validation": 0
            }
        },
        "DLT Permissionada Simples": {
            "score": 0,
            "metrics": {
                "security": 0,
                "scalability": 0,
                "energy_efficiency": 0,
                "governance": 0,
                "academic_validation": 0
            }
        },
        "DLT Híbrida": {
            "score": 0,
            "metrics": {
                "security": 0,
                "scalability": 0,
                "energy_efficiency": 0,
                "governance": 0,
                "academic_validation": 0
            }
        },
        "DLT com Consenso Delegado": {
            "score": 0,
            "metrics": {
                "security": 0,
                "scalability": 0,
                "energy_efficiency": 0,
                "governance": 0,
                "academic_validation": 0
            }
        },
        "DLT Pública": {
            "score": 0,
            "metrics": {
                "security": 0,
                "scalability": 0,
                "energy_efficiency": 0,
                "governance": 0,
                "academic_validation": 0
            }
        }
    }

    # Update scores based on answers
    for question_id, answer in answers.items():
        if question_id == "privacy" and answer == "Sim":
            matrix["DLT Permissionada Privada"]["metrics"]["security"] += 2
            matrix["DLT Permissionada Privada"]["metrics"]["academic_validation"] += academic_scores.get("Hyperledger Fabric", {}).get("score", 0)
        elif question_id == "integration" and answer == "Sim":
            matrix["DLT Híbrida"]["metrics"]["scalability"] += 2
            matrix["DLT Híbrida"]["metrics"]["academic_validation"] += academic_scores.get("Quorum", {}).get("score", 0)
        # Add other conditions for metrics...

    # Calculate final scores
    for dlt in matrix:
        matrix[dlt]["score"] = sum(matrix[dlt]["metrics"].values()) / len(matrix[dlt]["metrics"])

    return matrix

def get_recommendation(answers, weights):
    evaluation_matrix = create_evaluation_matrix(answers)
    
    # Calculate weighted scores
    weighted_scores = {}
    for dlt, data in evaluation_matrix.items():
        weighted_score = (
            data["metrics"]["security"] * weights["security"] +
            data["metrics"]["scalability"] * weights["scalability"] +
            data["metrics"]["energy_efficiency"] * weights["energy_efficiency"] +
            data["metrics"]["governance"] * weights["governance"] +
            data["metrics"]["academic_validation"] * 0.1  # Academic validation weight
        )
        weighted_scores[dlt] = weighted_score

    recommended_dlt = max(weighted_scores, key=weighted_scores.get)

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
    
    # Calculate confidence score
    confidence_scores = list(weighted_scores.values())
    is_reliable = calcular_confiabilidade_recomendacao(confidence_scores)

    return {
        "dlt": recommended_dlt,
        "consensus_group": recommended_group,
        "consensus": select_final_algorithm(recommended_group, weights),
        "algorithms": consensus_groups[recommended_group],
        "evaluation_matrix": evaluation_matrix,
        "confidence": is_reliable,
        "academic_validation": academic_scores.get(recommended_dlt, {})
    }

def compare_algorithms(consensus_group):
    algorithms = consensus_groups[consensus_group]
    comparison_data = {
        "Segurança": {},
        "Escalabilidade": {},
        "Eficiência Energética": {},
        "Governança": {},
        "Validação Acadêmica": {}
    }

    for alg in algorithms:
        for metric in comparison_data.keys():
            if metric == "Validação Acadêmica":
                comparison_data[metric][alg] = academic_scores.get(alg, {}).get("score", 3)
            else:
                comparison_data[metric][alg] = consensus_algorithms.get(alg, {}).get(metric.lower().replace(" ", "_"), 3)

    return comparison_data

def select_final_algorithm(consensus_group, priorities):
    comparison_data = compare_algorithms(consensus_group)
    algorithms = consensus_groups.get(consensus_group, [])
    
    if not algorithms:
        return "No suitable algorithm found"
    
    scores = {alg: 0 for alg in algorithms}
    
    for alg in algorithms:
        for metric, priority in priorities.items():
            metric_name = metric.capitalize()
            if metric_name in comparison_data and alg in comparison_data[metric_name]:
                scores[alg] += comparison_data[metric_name][alg] * priority
        
        # Add academic validation score
        academic_score = comparison_data.get("Validação Acadêmica", {}).get(alg, 0)
        scores[alg] += academic_score * 0.1  # Academic validation weight
    
    return max(scores, key=scores.get) if scores else "No suitable algorithm found"
