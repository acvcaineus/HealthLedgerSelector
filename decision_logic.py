import statistics
from dlt_data import questions, dlt_classes, consensus_algorithms, dlt_metrics, dlt_type_weights

def calculate_weighted_score(metrics, weights):
    """Calculate weighted score based on metrics and weights."""
    return sum(metrics[metric] * weights[metric] for metric in metrics.keys())

def get_recommendation(answers, user_weights=None):
    """Get DLT and consensus algorithm recommendations based on user answers and weights."""
    if not answers:
        return create_empty_recommendation()

    try:
        # Calculate weighted scores for each DLT using dynamic weights
        weighted_scores = {}
        raw_scores = {}
        evaluation_matrix = {}
        
        for dlt_name, dlt_info in dlt_metrics.items():
            # Get the DLT type and its corresponding weights
            dlt_type = dlt_info["type"]
            type_weights = dlt_type_weights[dlt_type]
            
            # Calculate raw and weighted scores
            metrics = dlt_info["metrics"]
            raw_score = sum(metrics.values()) / len(metrics)
            weighted_score = calculate_weighted_score(metrics, type_weights)
            
            weighted_scores[dlt_name] = weighted_score
            raw_scores[dlt_name] = raw_score
            
            # Store both raw and weighted metrics for visualization
            evaluation_matrix[dlt_name] = {
                "type": dlt_type,
                "raw_metrics": metrics.copy(),
                "weighted_metrics": {
                    metric: value * type_weights[metric]
                    for metric, value in metrics.items()
                },
                "raw_score": raw_score,
                "weighted_score": weighted_score
            }

        if not weighted_scores:
            return create_empty_recommendation()
            
        # Find DLT with maximum weighted score
        recommended_dlt = max(weighted_scores.items(), key=lambda x: x[1])[0]
        
        # Get DLT type and consensus group
        dlt_type = dlt_metrics[recommended_dlt]["type"]
        
        # Select best consensus algorithm based on DLT type
        recommended_algorithm = select_consensus_algorithm(dlt_type, answers)
        
        # Calculate confidence metrics
        confidence_value = calculate_confidence(weighted_scores, evaluation_matrix[recommended_dlt]["raw_metrics"], answers)
        
        # Calculate confidence components
        confidence_components = {
            "Separação": (max(weighted_scores.values()) - sum(weighted_scores.values()) / len(weighted_scores)) / max(weighted_scores.values()),
            "Consistência": calculate_answer_consistency(answers),
            "Alinhamento": calculate_characteristic_alignment(answers, dlt_type)
        }
        
        return {
            "dlt": recommended_dlt,
            "dlt_type": dlt_type,
            "consensus": recommended_algorithm,
            "evaluation_matrix": evaluation_matrix,
            "confidence": confidence_value > 0.7,
            "confidence_value": confidence_value,
            "confidence_components": confidence_components,
            "weighted_scores": weighted_scores,
            "raw_scores": raw_scores
        }
        
    except Exception as e:
        print(f"Error in get_recommendation: {str(e)}")
        return create_empty_recommendation()

def calculate_answer_consistency(answers):
    """Calculate consistency score based on potentially conflicting answers."""
    if not answers:
        return 0.0
        
    consistency_score = 1.0
    
    conflicts = {
        ("privacy", "interoperability"): lambda a, b: a == "Sim" and b == "Sim",
        ("energy_efficiency", "network_security"): lambda a, b: a == "Sim" and b == "Sim",
        ("scalability", "privacy"): lambda a, b: a == "Sim" and b == "Sim"
    }
    
    for (q1, q2), conflict_check in conflicts.items():
        if q1 in answers and q2 in answers:
            if conflict_check(answers[q1], answers[q2]):
                consistency_score -= 0.25
    
    return max(0.0, consistency_score)

def calculate_confidence(weighted_scores, characteristics, answers):
    """Calculate confidence score for the recommendation."""
    if not weighted_scores:
        return 0.0
        
    try:
        max_score = max(weighted_scores.values())
        mean_score = sum(weighted_scores.values()) / len(weighted_scores)
        std_dev = statistics.stdev(weighted_scores.values())
        
        separation_factor = (max_score - mean_score) / max_score if max_score > 0 else 0
        consistency_factor = 1 - (std_dev / max_score) if max_score > 0 else 0
        answer_consistency = calculate_answer_consistency(answers)
        
        confidence = (
            separation_factor * (1/3) +
            consistency_factor * (1/3) +
            answer_consistency * (1/3)
        )
        
        return confidence
    except (statistics.StatisticsError, ValueError, ZeroDivisionError):
        return 0.0

def calculate_characteristic_alignment(answers, dlt_type):
    """Calculate how well user answers align with DLT characteristics."""
    if not answers or dlt_type not in dlt_type_weights:
        return 0.0
    
    weights = dlt_type_weights[dlt_type]
    alignment_score = 0.0
    total_weight = sum(weights.values())
    
    for question_id, answer in answers.items():
        if answer == "Sim":
            if "security" in question_id or "privacy" in question_id:
                alignment_score += weights["security"]
            elif "scalability" in question_id or "integration" in question_id:
                alignment_score += weights["scalability"]
            elif "energy_efficiency" in question_id:
                alignment_score += weights["energy_efficiency"]
            elif "governance" in question_id or "interoperability" in question_id:
                alignment_score += weights["governance"]
    
    return alignment_score / total_weight if total_weight > 0 else 0

def select_consensus_algorithm(dlt_type, answers):
    """Select the best consensus algorithm based on DLT type and characteristics."""
    algorithm_scores = {}
    
    # Define algorithm mappings for each DLT type
    type_algorithms = {
        "DLT Permissionada Privada": ["Practical Byzantine Fault Tolerance (PBFT)", "Raft Consensus"],
        "DLT Permissionada Simples": ["Proof of Authority (PoA)", "Raft Consensus"],
        "DLT Híbrida": ["Proof of Stake (PoS)", "Delegated Proof of Stake (DPoS)"],
        "DLT com Consenso Delegado": ["Delegated Proof of Stake (DPoS)", "Nominated Proof of Stake (NPoS)"],
        "DLT Pública": ["Proof of Work (PoW)", "Proof of Stake (PoS)"],
        "DLT Pública Permissionless": ["Proof of Stake (PoS)", "Nominated Proof of Stake (NPoS)"]
    }
    
    if dlt_type not in type_algorithms:
        return "Não disponível"
    
    algorithms = type_algorithms[dlt_type]
    weights = dlt_type_weights[dlt_type]
    
    for algorithm in algorithms:
        score = 0
        if "security" in answers and answers["security"] == "Sim":
            score += weights["security"]
        if "scalability" in answers and answers["scalability"] == "Sim":
            score += weights["scalability"]
        if "energy_efficiency" in answers and answers["energy_efficiency"] == "Sim":
            score += weights["energy_efficiency"]
        if "governance_flexibility" in answers and answers["governance_flexibility"] == "Sim":
            score += weights["governance"]
        algorithm_scores[algorithm] = score
    
    return max(algorithm_scores.items(), key=lambda x: x[1])[0] if algorithm_scores else "Não disponível"

def create_empty_recommendation():
    """Create an empty recommendation structure."""
    return {
        "dlt": "Não disponível",
        "dlt_type": "Não disponível",
        "consensus": "Não disponível",
        "evaluation_matrix": {},
        "confidence": False,
        "confidence_value": 0.0,
        "confidence_components": {},
        "weighted_scores": {},
        "raw_scores": {}
    }
