import statistics
from dlt_data import questions, dlt_classes, consensus_algorithms, dlt_metrics, dlt_type_weights

def calculate_weighted_score(metrics, answers):
    """Calculate weighted score based on metrics and user answers."""
    # Base weights without user input
    weights = {
        'security': 0.25,
        'scalability': 0.25,
        'energy_efficiency': 0.25,
        'governance': 0.25
    }
    
    # Adjust weights based on user answers
    if answers.get('network_security') == 'Sim':
        weights['security'] += 0.1
    if answers.get('scalability') == 'Sim':
        weights['scalability'] += 0.1
    if answers.get('energy_efficiency') == 'Sim':
        weights['energy_efficiency'] += 0.1
    if answers.get('governance_flexibility') == 'Sim':
        weights['governance'] += 0.1
        
    # Normalize weights
    total = sum(weights.values())
    weights = {k: v/total for k, v in weights.items()}
    
    return sum(metrics[metric] * weights[metric] for metric in metrics.keys())

def select_consensus_group(dlt_type, answers):
    """Select the consensus group based on DLT type."""
    type_to_group = {
        "DLT Permissionada Privada": "Alta Segurança e Controle",
        "DLT Permissionada Simples": "Alta Eficiência",
        "DLT Híbrida": "Escalabilidade e Governança",
        "DLT com Consenso Delegado": "Alta Escalabilidade IoT",
        "DLT Pública": "Alta Segurança e Controle",
        "DLT Pública Permissionless": "Escalabilidade e Governança"
    }
    return type_to_group.get(dlt_type, "Alta Segurança e Controle")

def select_consensus_algorithm(consensus_group, answers):
    """Select the best consensus algorithm from the given group."""
    group_algorithms = {
        "Alta Segurança e Controle": ["PBFT", "PoW"],
        "Alta Eficiência": ["PoA", "RAFT"],
        "Escalabilidade e Governança": ["PoS", "DPoS"],
        "Alta Escalabilidade IoT": ["Tangle", "DAG"]
    }
    
    if consensus_group not in group_algorithms:
        return "Não disponível"
        
    algorithms = group_algorithms[consensus_group]
    algorithm_scores = {}
    
    for algorithm in algorithms:
        score = 0
        if answers.get('network_security') == 'Sim':
            score += 0.4  # Security weight
        if answers.get('scalability') == 'Sim':
            score += 0.3  # Scalability weight
        if answers.get('energy_efficiency') == 'Sim':
            score += 0.2  # Energy efficiency weight
        if answers.get('governance_flexibility') == 'Sim':
            score += 0.1  # Governance weight
        algorithm_scores[algorithm] = score
    
    return max(algorithm_scores.items(), key=lambda x: x[1])[0] if algorithm_scores else algorithms[0]

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
        answer_consistency = sum(1 for ans in answers.values() if ans == "Sim") / len(answers) if answers else 0
        
        confidence = (
            separation_factor * 0.4 +
            consistency_factor * 0.3 +
            answer_consistency * 0.3
        )
        
        return confidence
    except (statistics.StatisticsError, ValueError, ZeroDivisionError):
        return 0.0

def get_recommendation(answers):
    """Get DLT and consensus algorithm recommendations based on user answers."""
    if not answers:
        return create_empty_recommendation()
    
    try:
        weighted_scores = {}
        evaluation_matrix = {}
        
        for dlt_name, dlt_info in dlt_metrics.items():
            metrics = dlt_info["metrics"]
            weighted_score = calculate_weighted_score(metrics, answers)
            
            weighted_scores[dlt_name] = weighted_score
            evaluation_matrix[dlt_name] = {
                "type": dlt_info["type"],
                "metrics": metrics,
                "weighted_score": weighted_score
            }
        
        # Select DLT with highest weighted score
        recommended_dlt = max(weighted_scores.items(), key=lambda x: x[1])[0]
        dlt_type = dlt_metrics[recommended_dlt]["type"]
        
        # Select consensus group based on DLT type
        consensus_group = select_consensus_group(dlt_type, answers)
        
        # Select algorithm from consensus group
        consensus_algorithm = select_consensus_algorithm(consensus_group, answers)
        
        # Calculate confidence metrics
        confidence_value = calculate_confidence(weighted_scores, evaluation_matrix[recommended_dlt]["metrics"], answers)
        
        return {
            "dlt": recommended_dlt,
            "dlt_type": dlt_type,
            "consensus_group": consensus_group,
            "consensus": consensus_algorithm,
            "evaluation_matrix": evaluation_matrix,
            "weighted_scores": weighted_scores,
            "confidence": confidence_value > 0.7,
            "confidence_value": confidence_value
        }
        
    except Exception as e:
        print(f"Error in get_recommendation: {str(e)}")
        return create_empty_recommendation()

def create_empty_recommendation():
    """Create an empty recommendation structure."""
    return {
        "dlt": "Não disponível",
        "dlt_type": "Não disponível",
        "consensus_group": "Não disponível",
        "consensus": "Não disponível",
        "evaluation_matrix": {},
        "weighted_scores": {},
        "confidence": False,
        "confidence_value": 0.0
    }
