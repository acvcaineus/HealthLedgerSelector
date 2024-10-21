from dlt_data import questions, dlt_classes, consensus_algorithms

consensus_groups = {
    'Alta Segurança e Controle': ['PBFT', 'PoW'],
    'Alta Eficiência Operacional': ['RAFT', 'PoA'],
    'Escalabilidade e Governança Flexível': ['PoS', 'DPoS'],
    'Alta Escalabilidade em Redes IoT': ['Tangle'],
    'Alta Segurança e Descentralização de Dados Críticos': ['PoW', 'PoS']
}

def get_recommendation(answers, weights):
    score = {
        "DLT Permissionada Privada": 0,
        "DLT Pública Permissionless": 0,
        "DLT Permissionada Simples": 0,
        "DLT Híbrida": 0,
        "DLT com Consenso Delegado": 0,
        "DLT Pública": 0
    }

    for question_id, answer in answers.items():
        if question_id == "privacy" and answer == "Sim":
            score["DLT Permissionada Privada"] += 2 * weights["security"]
        elif question_id == "integration" and answer == "Sim":
            score["DLT Híbrida"] += 2 * weights["scalability"]
        elif question_id == "data_volume" and answer == "Sim":
            score["DLT Pública"] += 2 * weights["scalability"]
        elif question_id == "energy_efficiency" and answer == "Sim":
            score["DLT Permissionada Simples"] += 2 * weights["energy_efficiency"]
        elif question_id == "network_security" and answer == "Sim":
            score["DLT Pública Permissionless"] += 2 * weights["security"]
        elif question_id == "scalability" and answer == "Sim":
            score["DLT com Consenso Delegado"] += 2 * weights["scalability"]
        elif question_id == "governance_flexibility" and answer == "Sim":
            score["DLT Híbrida"] += 2 * weights["governance"]
        elif question_id == "interoperability" and answer == "Sim":
            score["DLT Pública"] += 2 * weights["scalability"]

    recommended_dlt = max(score, key=score.get)

    group_scores = {
        "Alta Segurança e Controle": weights["security"] * 2,
        "Alta Eficiência Operacional": weights["energy_efficiency"] * 2,
        "Escalabilidade e Governança Flexível": weights["scalability"] + weights["governance"],
        "Alta Escalabilidade em Redes IoT": weights["scalability"] * 2,
        "Alta Segurança e Descentralização de Dados Críticos": weights["security"] + weights["decentralization"]
    }

    recommended_group = max(group_scores, key=group_scores.get)

    return {
        "dlt": recommended_dlt,
        "consensus_group": recommended_group,
        "algorithms": consensus_groups[recommended_group]
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
    algorithms = list(comparison_data["Segurança"].keys())
    
    scores = {alg: 0 for alg in algorithms}
    
    for alg in algorithms:
        for metric, priority in priorities.items():
            scores[alg] += comparison_data[metric][alg] * priority

    if not scores:
        return "No suitable algorithm found"

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

# Updated pros and cons based on the new information
pros_cons = {
    "Registros Médicos Eletrônicos (EMR)": {
        "DLT Permissionada Privada": {
            "pros": ["Alta segurança e resiliência contra falhas bizantinas", "Máxima proteção de dados sensíveis"],
            "cons": ["Menor descentralização", "Potencial centralização de controle"],
            "algorithm_applicability": {
                "PBFT": "Excelente para EMR com alta segurança e proteção de dados sensíveis",
                "PoW": "Pode ser usado para EMR, mas com maior consumo energético"
            }
        },
        "DLT Pública Permissionless": {
            "pros": ["Alta segurança e descentralização", "Transparência dos registros"],
            "cons": ["Menor privacidade", "Alto consumo energético (PoW)"],
            "algorithm_applicability": {
                "PoW": "Fornece alta segurança, mas com alto consumo energético",
                "PoS": "Mais eficiente energeticamente, mantendo boa segurança"
            }
        }
    },
    "Sistemas locais de saúde": {
        "DLT Permissionada Simples": {
            "pros": ["Simplicidade e eficiência", "Validação rápida e leve"],
            "cons": ["Menor descentralização", "Potencial vulnerabilidade em redes maiores"],
            "algorithm_applicability": {
                "RAFT": "Ideal para sistemas locais de saúde com necessidade de consenso rápido",
                "PoA": "Bom para redes locais de hospitais com autoridades conhecidas"
            }
        }
    },
    "Monitoramento de saúde pública": {
        "DLT Híbrida": {
            "pros": ["Alta escalabilidade", "Governança flexível"],
            "cons": ["Complexidade de implementação", "Potencial conflito entre partes públicas e privadas"],
            "algorithm_applicability": {
                "PoS": "Adequado para redes regionais de saúde com necessidade de escalabilidade",
                "DPoS": "Bom para sistemas de monitoramento com delegação de responsabilidades"
            }
        }
    },
    "Monitoramento de dispositivos IoT em saúde": {
        "DLT Pública": {
            "pros": ["Alta escalabilidade para IoT", "Eficiência para dados em tempo real"],
            "cons": ["Potencial sobrecarga da rede", "Desafios de privacidade"],
            "algorithm_applicability": {
                "Tangle": "Excelente para monitoramento de dispositivos IoT em saúde em tempo real"
            }
        }
    }
}
