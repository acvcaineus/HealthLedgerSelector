from dlt_data import questions, dlt_classes, consensus_algorithms
from metrics import calcular_gini, calcular_entropia, calcular_profundidade_decisoria, calcular_pruning, calcular_confiabilidade_recomendacao

# Updated DLT groups and mappings from reference table
dlt_groups = {
    "Alta Segurança e Controle": {
        "dlts": ["Hyperledger Fabric"],
        "algorithms": ["RAFT/IBFT"],
        "characteristics": ["security", "privacy"],
        "use_cases": "Prontuários eletrônicos, integração de dados sensíveis, sistemas de pagamento descentralizados"
    },
    "Alta Eficiência Operacional": {
        "dlts": ["Corda", "VeChain"],
        "algorithms": ["RAFT", "PoA"],
        "characteristics": ["efficiency", "scalability"],
        "use_cases": "Sistemas locais de saúde, agendamento de pacientes, redes locais de hospitais"
    },
    "Escalabilidade e Governança Flexível": {
        "dlts": ["Quorum", "Ethereum 2.0"],
        "algorithms": ["RAFT/IBFT", "PoS"],
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
    }
}

def calculate_characteristic_scores(answers):
    """Calculate scores for each characteristic based on user answers"""
    scores = {
        "security": 0.0,
        "privacy": 0.0,
        "efficiency": 0.0,
        "scalability": 0.0,
        "governance": 0.0,
        "iot_compatibility": 0.0
    }
    
    # Map answers to characteristics
    if answers.get("privacy") == "Sim":
        scores["privacy"] += 2.0
        scores["security"] += 1.0
    
    if answers.get("integration") == "Sim":
        scores["scalability"] += 1.0
        scores["efficiency"] += 1.0
    
    if answers.get("data_volume") == "Sim":
        scores["scalability"] += 2.0
    
    if answers.get("energy_efficiency") == "Sim":
        scores["efficiency"] += 2.0
    
    if answers.get("network_security") == "Sim":
        scores["security"] += 2.0
    
    if answers.get("scalability") == "Sim":
        scores["scalability"] += 1.0
        scores["iot_compatibility"] += 1.0
    
    if answers.get("governance_flexibility") == "Sim":
        scores["governance"] += 2.0
    
    if answers.get("interoperability") == "Sim":
        scores["iot_compatibility"] += 1.0
        scores["scalability"] += 1.0
    
    return scores

def create_evaluation_matrix(answers, characteristic_scores):
    """Create evaluation matrix based on characteristic scores and DLT groups"""
    matrix = {}
    
    for group_name, group_data in dlt_groups.items():
        for dlt in group_data["dlts"]:
            matrix[dlt] = {
                "group": group_name,
                "score": 0,
                "metrics": {
                    "security": float(0),
                    "privacy": float(0),
                    "efficiency": float(0),
                    "scalability": float(0),
                    "governance": float(0),
                    "iot_compatibility": float(0)
                },
                "use_cases": group_data["use_cases"],
                "algorithms": group_data["algorithms"]
            }
            
            # Calculate scores based on DLT characteristics
            for characteristic in group_data["characteristics"]:
                matrix[dlt]["metrics"][characteristic] = characteristic_scores[characteristic]
            
            # Add academic validation score
            if dlt in academic_scores:
                matrix[dlt]["academic_validation"] = academic_scores[dlt]
    
    return matrix

def get_recommendation(answers, weights):
    """Get DLT recommendation based on user answers and weights"""
    try:
        # Initialize default values
        recommended_dlt = None
        recommended_group = "Alta Segurança e Controle"  # Default fallback
        recommended_algorithms = dlt_groups["Alta Segurança e Controle"]["algorithms"]
        
        # Calculate characteristic scores
        characteristic_scores = calculate_characteristic_scores(answers)
        
        # Create evaluation matrix
        evaluation_matrix = create_evaluation_matrix(answers, characteristic_scores)
        
        if not evaluation_matrix:
            raise ValueError("Failed to create evaluation matrix")
        
        # Calculate weighted scores for each DLT
        weighted_scores = {}
        for dlt, data in evaluation_matrix.items():
            score = (
                float(data["metrics"]["security"]) * float(weights["security"]) +
                float(data["metrics"]["scalability"]) * float(weights["scalability"]) +
                float(data["metrics"]["efficiency"]) * float(weights["energy_efficiency"]) +
                float(data["metrics"]["governance"]) * float(weights["governance"])
            )
            
            # Add academic validation bonus
            if "academic_validation" in data:
                score += float(data["academic_validation"]["score"]) * 0.1
            
            weighted_scores[dlt] = float(score)
        
        if weighted_scores:
            # Find DLT with maximum weighted score
            recommended_dlt = max(weighted_scores.items(), key=lambda x: float(x[1]))[0]
            
            # Get group and algorithms for recommended DLT
            for group_name, group_data in dlt_groups.items():
                if recommended_dlt in group_data["dlts"]:
                    recommended_group = group_name
                    recommended_algorithms = group_data["algorithms"]
                    break
        
        # Calculate confidence value
        confidence_scores = list(weighted_scores.values())
        confidence_value = max(confidence_scores) - (sum(confidence_scores) / len(confidence_scores)) if confidence_scores else 0
        is_reliable = confidence_value > 0.7
        
        return {
            "dlt": recommended_dlt,
            "consensus_group": recommended_group,
            "consensus": recommended_algorithms[0] if recommended_algorithms else None,
            "algorithms": recommended_algorithms,
            "evaluation_matrix": evaluation_matrix,
            "confidence": is_reliable,
            "confidence_value": confidence_value,
            "academic_validation": academic_scores.get(recommended_dlt, {}),
            "use_cases": evaluation_matrix[recommended_dlt]["use_cases"] if recommended_dlt else ""
        }
    except Exception as e:
        # Return safe default values in case of error
        return {
            "dlt": "Hyperledger Fabric",
            "consensus_group": "Alta Segurança e Controle",
            "consensus": "RAFT/IBFT",
            "algorithms": ["RAFT/IBFT"],
            "evaluation_matrix": {},
            "confidence": False,
            "confidence_value": 0.0,
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
            if "/" in alg:  # Handle combined algorithms (e.g., "RAFT/IBFT")
                alg_parts = alg.split("/")
                scores = []
                for part in alg_parts:
                    if part in consensus_algorithms:
                        scores.append(consensus_algorithms[part])
                if scores:
                    avg_scores = {k: sum(s.get(k, 0) for s in scores) / len(scores) 
                                for k in ["security", "scalability", "energy_efficiency", "governance"]}
                    comparison_data["Segurança"][alg] = float(avg_scores["security"])
                    comparison_data["Escalabilidade"][alg] = float(avg_scores["scalability"])
                    comparison_data["Eficiência Energética"][alg] = float(avg_scores["energy_efficiency"])
                    comparison_data["Governança"][alg] = float(avg_scores["governance"])
            elif alg in consensus_algorithms:
                data = consensus_algorithms[alg]
                comparison_data["Segurança"][alg] = float(data.get("security", 3))
                comparison_data["Escalabilidade"][alg] = float(data.get("scalability", 3))
                comparison_data["Eficiência Energética"][alg] = float(data.get("energy_efficiency", 3))
                comparison_data["Governança"][alg] = float(data.get("governance", 3))
        
        return comparison_data
    except Exception as e:
        # Return empty comparison data in case of error
        return {
            "Segurança": {},
            "Escalabilidade": {},
            "Eficiência Energética": {},
            "Governança": {},
            "error": str(e)
        }
