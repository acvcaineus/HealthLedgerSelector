from dlt_data import questions, dlt_classes, consensus_algorithms
from metrics import calcular_gini, calcular_entropia, calcular_profundidade_decisoria, calcular_pruning, calcular_confiabilidade_recomendacao

# Updated DLT groups and mappings from reference table
dlt_groups = {
    "Alta Segurança e Controle": {
        "dlts": ["Hyperledger Fabric", "Bitcoin", "Ethereum (PoW)"],
        "algorithms": ["PBFT", "PoW"],
        "characteristics": ["security", "privacy"],
        "use_cases": "Prontuários eletrônicos, integração de dados sensíveis, sistemas de pagamento descentralizados"
    },
    "Alta Eficiência Operacional": {
        "dlts": ["Quorum", "VeChain"],
        "algorithms": ["RAFT", "PoA"],  # VeChain uses PoA, Quorum uses RAFT
        "characteristics": ["efficiency", "scalability"],
        "use_cases": "Sistemas locais de saúde, agendamento de pacientes, redes locais de hospitais"
    },
    "Escalabilidade e Governança Flexível": {
        "dlts": ["Ethereum 2.0", "EOS"],
        "algorithms": ["PoS", "DPoS"],
        "characteristics": ["scalability", "governance"],
        "use_cases": "Monitoramento de saúde pública, redes regionais de saúde, integração de EHRs"
    },
    "Alta Escalabilidade em Redes IoT": {
        "dlts": ["IOTA"],
        "algorithms": ["Tangle"],
        "characteristics": ["scalability", "iot_compatibility"],
        "use_cases": "Monitoramento de dispositivos IoT em saúde, dados em tempo real"
    }
}

# Academic validation scores and references
academic_scores = {
    "Hyperledger Fabric": {
        "score": 4.5,
        "reference": "Mehmood et al. (2025) - BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain",
        "validation": "Alta segurança e resiliência contra falhas bizantinas"
    },
    "VeChain": {
        "score": 4.2,
        "reference": "Popoola et al. (2024) - A critical literature review of security and privacy in smart home healthcare",
        "validation": "Simplicidade e eficiência em redes permissionadas menores"
    },
    "Quorum": {
        "score": 4.0,
        "reference": "Mehmood et al. (2025) - BLPCA-ledger",
        "validation": "Alta escalabilidade e governança flexível"
    },
    "IOTA": {
        "score": 4.3,
        "reference": "Salim et al. (2024) - Privacy-preserving and scalable federated blockchain scheme",
        "validation": "Alta escalabilidade e eficiência para IoT"
    },
    "Ethereum 2.0": {
        "score": 4.4,
        "reference": "Nawaz et al. (2024) - Hyperledger sawtooth based supply chain traceability system",
        "validation": "Alta escalabilidade e eficiência energética"
    },
    "Bitcoin": {
        "score": 4.5,
        "reference": "Liu et al. (2024) - A systematic study on blockchain in healthcare",
        "validation": "Alta segurança e descentralização"
    },
    "Ethereum (PoW)": {
        "score": 4.2,
        "reference": "Makhdoom et al. (2024) - PrivySeC: A secure framework for data sharing",
        "validation": "Segurança robusta e suporte a contratos inteligentes"
    },
    "EOS": {
        "score": 4.1,
        "reference": "Wang et al. (2024) - Blockchain for healthcare data management",
        "validation": "Alta escalabilidade e governança democrática"
    }
}

def calculate_characteristic_scores(answers):
    """Calculate scores for each characteristic based on user answers"""
    scores = {
        "security": float(0.0),
        "privacy": float(0.0),
        "efficiency": float(0.0),
        "scalability": float(0.0),
        "governance": float(0.0),
        "iot_compatibility": float(0.0)
    }
    
    if answers.get("privacy") == "Sim":
        scores["privacy"] += float(2.0)
        scores["security"] += float(1.0)
    
    if answers.get("integration") == "Sim":
        scores["scalability"] += float(1.0)
        scores["efficiency"] += float(1.0)
    
    if answers.get("data_volume") == "Sim":
        scores["scalability"] += float(2.0)
    
    if answers.get("energy_efficiency") == "Sim":
        scores["efficiency"] += float(2.0)
    
    if answers.get("network_security") == "Sim":
        scores["security"] += float(2.0)
    
    if answers.get("scalability") == "Sim":
        scores["scalability"] += float(1.0)
        scores["iot_compatibility"] += float(1.0)
    
    if answers.get("governance_flexibility") == "Sim":
        scores["governance"] += float(2.0)
    
    if answers.get("interoperability") == "Sim":
        scores["iot_compatibility"] += float(1.0)
        scores["scalability"] += float(1.0)
    
    return scores

def create_evaluation_matrix(answers, characteristic_scores):
    """Create evaluation matrix based on characteristic scores and DLT groups"""
    matrix = {}
    
    for group_name, group_data in dlt_groups.items():
        for dlt in group_data["dlts"]:
            matrix[dlt] = {
                "group": group_name,
                "score": float(0),
                "metrics": {
                    "security": float(0),
                    "privacy": float(0),
                    "efficiency": float(0),
                    "scalability": float(0),
                    "governance": float(0),
                    "iot_compatibility": float(0)
                },
                "use_cases": group_data["use_cases"],
                "algorithms": group_data["algorithms"],
                "possible_algorithms": group_data["algorithms"]
            }
            
            # Calculate scores based on DLT characteristics
            for characteristic in group_data["characteristics"]:
                matrix[dlt]["metrics"][characteristic] = float(characteristic_scores[characteristic])
            
            # Add academic validation score if available
            if dlt in academic_scores:
                matrix[dlt]["academic_validation"] = academic_scores[dlt]
    
    return matrix

def select_consensus_group(characteristic_scores, weights):
    """Select the most suitable consensus group based on weighted characteristics"""
    group_scores = {
        "Alta Segurança e Controle": float(0.0),
        "Alta Eficiência Operacional": float(0.0),
        "Escalabilidade e Governança Flexível": float(0.0),
        "Alta Escalabilidade em Redes IoT": float(0.0)
    }
    
    # Calculate scores for each group based on their primary characteristics
    for group_name, group_data in dlt_groups.items():
        score = float(sum(
            characteristic_scores[char] * weights.get(char, 0.25)
            for char in group_data["characteristics"]
        ))
        group_scores[group_name] = score
    
    # Return the group with highest score
    return max(group_scores.items(), key=lambda x: float(x[1]))[0]

def select_algorithm_from_group(consensus_group, characteristic_scores, weights):
    """Select the most suitable algorithm from within a consensus group"""
    possible_algorithms = dlt_groups[consensus_group]["algorithms"]
    algorithm_scores = {}
    
    for algorithm in possible_algorithms:
        if algorithm in consensus_algorithms:
            score = float(
                float(consensus_algorithms[algorithm]["security"]) * float(weights["security"]) +
                float(consensus_algorithms[algorithm]["scalability"]) * float(weights["scalability"]) +
                float(consensus_algorithms[algorithm]["energy_efficiency"]) * float(weights["energy_efficiency"]) +
                float(consensus_algorithms[algorithm]["governance"]) * float(weights["governance"])
            )
            algorithm_scores[algorithm] = score
    
    return max(algorithm_scores.items(), key=lambda x: float(x[1]))[0] if algorithm_scores else possible_algorithms[0]

def get_recommendation(answers, weights):
    """Get DLT recommendation based on user answers and weights using two-step process"""
    try:
        # Calculate characteristic scores
        characteristic_scores = calculate_characteristic_scores(answers)
        
        # First select consensus group
        recommended_group = select_consensus_group(characteristic_scores, weights)
        
        # Then select specific algorithm from that group
        recommended_algorithm = select_algorithm_from_group(recommended_group, characteristic_scores, weights)
        
        # Select DLT based on the chosen group
        recommended_dlt = dlt_groups[recommended_group]["dlts"][0]  # Choose first DLT in group as default
        
        # Create evaluation matrix
        evaluation_matrix = create_evaluation_matrix(answers, characteristic_scores)
        
        # Calculate confidence value
        weighted_scores = {dlt: float(sum(
            float(data["metrics"][metric]) * float(weights.get(metric, 0.25))
            for metric in weights.keys()
        )) for dlt, data in evaluation_matrix.items()}
        
        confidence_scores = list(weighted_scores.values())
        confidence_value = float(max(confidence_scores) - (sum(confidence_scores) / len(confidence_scores))) if confidence_scores else float(0)
        is_reliable = confidence_value > 0.7
        
        return {
            "dlt": recommended_dlt,
            "consensus_group": recommended_group,
            "consensus": recommended_algorithm,
            "algorithms": dlt_groups[recommended_group]["algorithms"],
            "possible_algorithms": dlt_groups[recommended_group]["algorithms"],
            "evaluation_matrix": evaluation_matrix,
            "confidence": is_reliable,
            "confidence_value": confidence_value,
            "academic_validation": academic_scores.get(str(recommended_dlt), academic_scores["Hyperledger Fabric"]),
            "use_cases": dlt_groups[recommended_group]["use_cases"]
        }
    except Exception as e:
        return {
            "dlt": "Hyperledger Fabric",
            "consensus_group": "Alta Segurança e Controle",
            "consensus": "PBFT",
            "algorithms": ["PBFT"],
            "possible_algorithms": ["PBFT"],
            "evaluation_matrix": {},
            "confidence": False,
            "confidence_value": float(0.0),
            "academic_validation": academic_scores["Hyperledger Fabric"],
            "use_cases": dlt_groups["Alta Segurança e Controle"]["use_cases"],
            "error": str(e)
        }

def compare_algorithms(consensus_group):
    """Compare algorithms within a consensus group"""
    try:
        algorithms = []
        for group_data in dlt_groups.values():
            if any(alg in consensus_group for alg in group_data["algorithms"]):
                algorithms.extend(group_data["algorithms"])
        
        comparison_data = {
            "Segurança": {},
            "Escalabilidade": {},
            "Eficiência Energética": {},
            "Governança": {}
        }
        
        for alg in set(algorithms):
            if alg in consensus_algorithms:
                data = consensus_algorithms[alg]
                comparison_data["Segurança"][alg] = float(data.get("security", 3))
                comparison_data["Escalabilidade"][alg] = float(data.get("scalability", 3))
                comparison_data["Eficiência Energética"][alg] = float(data.get("energy_efficiency", 3))
                comparison_data["Governança"][alg] = float(data.get("governance", 3))
        
        return comparison_data
    except Exception as e:
        return {
            "Segurança": {},
            "Escalabilidade": {},
            "Eficiência Energética": {},
            "Governança": {},
            "error": str(e)
        }
