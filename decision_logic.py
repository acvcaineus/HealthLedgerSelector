from dlt_data import questions, dlt_classes, consensus_algorithms
from metrics import calcular_gini, calcular_entropia, calcular_profundidade_decisoria, calcular_pruning, calcular_confiabilidade_recomendacao

# DLT groups with their characteristics and mappings
dlt_groups = {
    "Alta Segurança e Controle": {
        "dlts": ["Hyperledger Fabric", "Bitcoin", "Ethereum (PoW)"],
        "algorithms": ["PBFT", "PoW"],
        "characteristics": ["security", "privacy"],
        "use_cases": "Prontuários eletrônicos, integração de dados sensíveis, sistemas de pagamento descentralizados"
    },
    "Alta Eficiência Operacional": {
        "dlts": ["Quorum", "VeChain"],
        "algorithms": ["RAFT", "PoA"],
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

def normalize_scores(scores):
    """Normalize scores to 0-1 range"""
    max_score = max(scores.values()) if scores.values() else 1.0
    return {k: float(v/max_score) for k, v in scores.items()}

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
    
    # Normalize scores before returning
    return normalize_scores(scores)

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
                }
            }
            
            # Calculate scores based on DLT characteristics
            base_score = 3.0  # Base score for all metrics
            for characteristic in group_data["characteristics"]:
                matrix[dlt]["metrics"][characteristic] = float(base_score + characteristic_scores[characteristic])
            
            # Normalize metrics to 0-1 range
            max_metric = max(matrix[dlt]["metrics"].values())
            if max_metric > 0:
                matrix[dlt]["metrics"] = {k: float(v/max_metric) for k, v in matrix[dlt]["metrics"].items()}
            
            # Add academic validation if available
            if dlt in academic_scores:
                matrix[dlt]["academic_validation"] = academic_scores[dlt]
    
    return matrix

def select_consensus_group(answers, characteristic_scores, weights):
    """Select consensus group based on user answers and characteristic scores"""
    group_scores = {}
    
    # Initialize scores for each group
    for group_name in dlt_groups.keys():
        group_scores[group_name] = float(0.0)
    
    # Score based on answers
    if answers.get("privacy") == "Sim":
        group_scores["Alta Segurança e Controle"] += float(2.0)
    if answers.get("energy_efficiency") == "Sim":
        group_scores["Alta Eficiência Operacional"] += float(1.5)
    if answers.get("scalability") == "Sim":
        group_scores["Escalabilidade e Governança Flexível"] += float(1.5)
    if answers.get("interoperability") == "Sim":
        group_scores["Alta Escalabilidade em Redes IoT"] += float(1.0)
    
    # Add weighted characteristic scores
    for group_name, group_data in dlt_groups.items():
        for char in group_data["characteristics"]:
            group_scores[group_name] += float(characteristic_scores[char]) * float(weights.get(char, 0.25))
    
    return max(group_scores.items(), key=lambda x: float(x[1]))[0]

def match_dlt_with_algorithms(dlt_name, consensus_group):
    """Match DLT with compatible consensus algorithms"""
    compatible_algorithms = []
    
    # Get all possible algorithms for the DLT from reference table
    for group_name, group_data in dlt_groups.items():
        if dlt_name in group_data["dlts"]:
            compatible_algorithms.extend(group_data["algorithms"])
    
    # Filter algorithms based on consensus group
    group_algorithms = dlt_groups[consensus_group]["algorithms"]
    return list(set(compatible_algorithms) & set(group_algorithms))

def get_recommendation(answers, weights):
    """Get DLT recommendation based on user answers and weights using dynamic selection"""
    try:
        # Calculate characteristic scores
        characteristic_scores = calculate_characteristic_scores(answers)
        
        # First select consensus group based on answers and characteristics
        recommended_group = select_consensus_group(answers, characteristic_scores, weights)
        
        # Get possible DLTs for the group
        possible_dlts = dlt_groups[recommended_group]["dlts"]
        
        # Score each DLT based on characteristics
        dlt_scores = {}
        for dlt in possible_dlts:
            score = float(0)
            for char, char_score in characteristic_scores.items():
                score += float(char_score) * float(weights.get(char, 0.25))
            dlt_scores[dlt] = score
        
        # Select best DLT
        recommended_dlt = max(dlt_scores.items(), key=lambda x: float(x[1]))[0]
        
        # Get compatible algorithms for the selected DLT
        compatible_algorithms = match_dlt_with_algorithms(recommended_dlt, recommended_group)
        
        # Select best algorithm from compatible ones
        if compatible_algorithms:
            algorithm_scores = {}
            for alg in compatible_algorithms:
                if alg in consensus_algorithms:
                    score = float(sum(
                        float(consensus_algorithms[alg][metric]) * float(weights.get(metric, 0.25))
                        for metric in weights.keys()
                    ))
                    algorithm_scores[alg] = score
            recommended_algorithm = max(algorithm_scores.items(), key=lambda x: float(x[1]))[0]
        else:
            recommended_algorithm = dlt_groups[recommended_group]["algorithms"][0]
        
        # Create evaluation matrix and calculate confidence
        evaluation_matrix = create_evaluation_matrix(answers, characteristic_scores)
        
        # Fix confidence calculation
        weighted_scores = {dlt: float(sum(
            float(data["metrics"][metric]) * float(weights.get(metric, 0.25))
            for metric in weights.keys()
            if metric in data["metrics"]  # Only include metrics that exist
        )) for dlt, data in evaluation_matrix.items()}

        confidence_scores = list(weighted_scores.values())
        if confidence_scores:
            max_score = max(confidence_scores)
            mean_score = sum(confidence_scores) / len(confidence_scores)
            confidence_value = (max_score - mean_score) / max_score if max_score > 0 else 0.0
        else:
            confidence_value = 0.0

        is_reliable = confidence_value > 0.7
        
        return {
            "dlt": recommended_dlt,
            "consensus_group": recommended_group,
            "consensus": recommended_algorithm,
            "algorithms": compatible_algorithms,
            "possible_algorithms": compatible_algorithms,
            "evaluation_matrix": evaluation_matrix,
            "confidence": is_reliable,
            "confidence_value": confidence_value,
            "academic_validation": academic_scores.get(recommended_dlt, academic_scores["Hyperledger Fabric"]),
            "use_cases": dlt_groups[recommended_group]["use_cases"]
        }
    except Exception as e:
        return {
            "error": str(e),
            "dlt": "Hyperledger Fabric",
            "consensus_group": "Alta Segurança e Controle",
            "consensus": "PBFT",
            "algorithms": ["PBFT"],
            "possible_algorithms": ["PBFT"],
            "evaluation_matrix": {},
            "confidence": False,
            "confidence_value": float(0.0),
            "academic_validation": academic_scores["Hyperledger Fabric"],
            "use_cases": dlt_groups["Alta Segurança e Controle"]["use_cases"]
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
