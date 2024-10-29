import statistics
from dlt_data import questions, dlt_classes, consensus_algorithms

# Question weights for characteristic alignment
question_weights = {
    "privacy": 2.0,  # Higher weight for privacy in healthcare
    "integration": 1.5,
    "data_volume": 1.5,
    "energy_efficiency": 1.0,
    "network_security": 2.0,  # Higher weight for security
    "scalability": 1.5,
    "governance_flexibility": 1.0,
    "interoperability": 1.5
}

# DLT consensus mapping
dlt_consensus_mapping = {
    "DLT Permissionada Privada": {
        'group': "Alta Segurança e Controle",
        'weight': 1.2,
        'characteristics': ['security', 'governance']
    },
    "DLT Pública Permissionless": {
        'group': "Alta Segurança e Descentralização de Dados Críticos",
        'weight': 1.1,
        'characteristics': ['security', 'scalability']
    },
    "DLT Permissionada Simples": {
        'group': "Alta Eficiência Operacional",
        'weight': 1.0,
        'characteristics': ['energy_efficiency', 'governance']
    },
    "DLT Híbrida": {
        'group': "Escalabilidade e Governança Flexível",
        'weight': 1.1,
        'characteristics': ['scalability', 'governance']
    },
    "DLT com Consenso Delegado": {
        'group': "Escalabilidade e Governança Flexível",
        'weight': 1.0,
        'characteristics': ['scalability', 'energy_efficiency']
    },
    "DLT Pública": {
        'group': "Alta Escalabilidade em Redes IoT",
        'weight': 1.0,
        'characteristics': ['scalability', 'energy_efficiency']
    }
}

# Consensus groups
consensus_groups = {
    'Alta Segurança e Controle': {
        'algorithms': ['Practical Byzantine Fault Tolerance (PBFT)', 'Proof of Work (PoW)'],
        'characteristics': {
            'security': 5.0,
            'scalability': 3.0,
            'energy_efficiency': 2.0,
            'governance': 4.0
        },
        'description': 'Ideal para dados sensíveis de saúde com foco em segurança máxima'
    },
    'Alta Eficiência Operacional': {
        'algorithms': ['Raft Consensus', 'Proof of Authority (PoA)'],
        'characteristics': {
            'security': 4.0,
            'scalability': 4.0,
            'energy_efficiency': 5.0,
            'governance': 3.0
        },
        'description': 'Otimizado para eficiência em redes hospitalares locais'
    },
    'Escalabilidade e Governança Flexível': {
        'algorithms': ['Proof of Stake (PoS)', 'Delegated Proof of Stake (DPoS)'],
        'characteristics': {
            'security': 4.0,
            'scalability': 5.0,
            'energy_efficiency': 4.0,
            'governance': 5.0
        },
        'description': 'Balanceamento entre escalabilidade e governança adaptável'
    },
    'Alta Escalabilidade em Redes IoT': {
        'algorithms': ['Tangle', 'Directed Acyclic Graph (DAG)'],
        'characteristics': {
            'security': 4.0,
            'scalability': 5.0,
            'energy_efficiency': 5.0,
            'governance': 3.0
        },
        'description': 'Especializado em dispositivos IoT e dados em tempo real'
    },
    'Alta Segurança e Descentralização de Dados Críticos': {
        'algorithms': ['Proof of Work (PoW)', 'Proof of Stake (PoS)'],
        'characteristics': {
            'security': 5.0,
            'scalability': 3.0,
            'energy_efficiency': 2.0,
            'governance': 4.0
        },
        'description': 'Máxima segurança para dados críticos de saúde'
    }
}

def calculate_answer_consistency(answers):
    """Calculate consistency score based on potentially conflicting answers."""
    if not answers:
        return 0.0
        
    consistency_score = 1.0
    
    # Check for conflicting combinations
    conflicts = {
        ("privacy", "interoperability"): lambda a, b: a == "Sim" and b == "Sim",
        ("energy_efficiency", "network_security"): lambda a, b: a == "Sim" and b == "Sim",
        ("scalability", "privacy"): lambda a, b: a == "Sim" and b == "Sim"
    }
    
    for (q1, q2), conflict_check in conflicts.items():
        if q1 in answers and q2 in answers:
            if conflict_check(answers[q1], answers[q2]):
                consistency_score -= 0.2  # Reduce score for each conflict
    
    return max(0.0, consistency_score)

def calculate_confidence(weighted_scores, characteristics, answers):
    """Calculate confidence score for the recommendation."""
    if not weighted_scores:
        return 0.0
        
    try:
        max_score = max(weighted_scores.values())
        mean_score = sum(weighted_scores.values()) / len(weighted_scores)
        std_dev = statistics.stdev(weighted_scores.values())
        
        # Calculate factors
        separation_factor = (max_score - mean_score) / max_score if max_score > 0 else 0
        consistency_factor = 1 - (std_dev / max_score) if max_score > 0 else 0
        answer_consistency = calculate_answer_consistency(answers)
        
        # Weight the factors
        confidence = (
            separation_factor * 0.4 +  # How clear the winner is
            consistency_factor * 0.3 +  # How consistent the scores are
            answer_consistency * 0.3    # How consistent the answers are
        )
        
        return confidence
    except (statistics.StatisticsError, ValueError, ZeroDivisionError):
        return 0.0

def calculate_characteristic_alignment(answers, dlt_type):
    """Calculate how well user answers align with DLT characteristics."""
    if not answers or dlt_type not in dlt_consensus_mapping:
        return 0.0
    
    alignment_score = 0
    total_weight = 0
    
    for question_id, answer in answers.items():
        weight = question_weights.get(question_id, 1)
        if question_id in dlt_consensus_mapping[dlt_type]['characteristics'] and answer == "Sim":
            alignment_score += weight
        total_weight += weight
    
    return alignment_score / total_weight if total_weight > 0 else 0

def get_recommendation(answers, weights):
    """Get DLT and consensus algorithm recommendations based on user answers and weights."""
    if not answers or not weights:
        return create_empty_recommendation()

    try:
        # Calculate weighted scores for each DLT
        weighted_scores = {}
        for dlt_type in dlt_consensus_mapping.keys():
            score = 0.0
            
            # Calculate base score from characteristics
            for characteristic in dlt_consensus_mapping[dlt_type]['characteristics']:
                if characteristic in weights:
                    weight = float(weights[characteristic])
                    # Add score based on aligned answers
                    for question_id, answer in answers.items():
                        if answer == "Sim" and question_id in question_weights:
                            if question_id == "privacy" and characteristic == "security":
                                score += weight * 2.0
                            elif question_id == "integration" and characteristic == "scalability":
                                score += weight * 1.5
                            elif question_id == "network_security" and characteristic == "security":
                                score += weight * 2.0
                            elif question_id == "scalability" and characteristic == "scalability":
                                score += weight * 2.0
                            elif question_id == "energy_efficiency" and characteristic == "energy_efficiency":
                                score += weight * 2.0
                            elif question_id == "governance_flexibility" and characteristic == "governance":
                                score += weight * 2.0
            
            # Apply DLT weight
            score *= dlt_consensus_mapping[dlt_type]['weight']
            weighted_scores[dlt_type] = float(score)

        if not weighted_scores:
            return create_empty_recommendation()
            
        # Find DLT with maximum weighted score
        recommended_dlt = max(weighted_scores.items(), key=lambda x: float(x[1]))[0]
        
        # Get corresponding consensus group
        recommended_group = dlt_consensus_mapping[recommended_dlt]['group']
        group_description = consensus_groups[recommended_group]['description']
        group_characteristics = consensus_groups[recommended_group]['characteristics']
        
        # Select best algorithm from the group based on characteristics
        recommended_algorithm = select_consensus_algorithm(recommended_group, weights, answers)
        
        # Calculate confidence metrics
        confidence_value = calculate_confidence(weighted_scores, group_characteristics, answers)
        
        # Calculate confidence components
        confidence_components = {
            "Separação": (max(weighted_scores.values()) - sum(weighted_scores.values()) / len(weighted_scores)) / max(weighted_scores.values()),
            "Consistência": calculate_answer_consistency(answers),
            "Alinhamento": calculate_characteristic_alignment(answers, recommended_dlt)
        }
        
        # Create evaluation matrix
        evaluation_matrix = {}
        for dlt, score in weighted_scores.items():
            evaluation_matrix[dlt] = {
                "score": score,
                "metrics": {
                    "security": float(group_characteristics.get('security', 3.0)),
                    "scalability": float(group_characteristics.get('scalability', 3.0)),
                    "energy_efficiency": float(group_characteristics.get('energy_efficiency', 3.0)),
                    "governance": float(group_characteristics.get('governance', 3.0))
                }
            }
        
        return {
            "dlt": recommended_dlt,
            "consensus": recommended_algorithm,
            "consensus_group": recommended_group,
            "group_description": group_description,
            "evaluation_matrix": evaluation_matrix,
            "confidence": confidence_value > 0.7,
            "confidence_value": confidence_value,
            "confidence_components": confidence_components,
            "group_characteristics": group_characteristics,
            "weighted_scores": weighted_scores
        }
        
    except Exception as e:
        print(f"Error in get_recommendation: {str(e)}")
        return create_empty_recommendation()

def select_consensus_algorithm(consensus_group, weights, answers):
    """Select the best consensus algorithm based on group and characteristics."""
    if consensus_group not in consensus_groups:
        return "Não disponível"
    
    algorithms = consensus_groups[consensus_group]['algorithms']
    scores = {}
    
    for algorithm in algorithms:
        if algorithm in consensus_algorithms:
            score = 0.0
            algo_data = consensus_algorithms[algorithm]
            
            # Calculate weighted score based on characteristics
            for characteristic, weight in weights.items():
                if characteristic in algo_data:
                    base_score = float(algo_data[characteristic])
                    # Adjust score based on answers
                    for question_id, answer in answers.items():
                        if answer == "Sim":
                            if question_id == "energy_efficiency" and characteristic == "energy_efficiency":
                                base_score *= 1.2
                            elif question_id == "scalability" and characteristic == "scalability":
                                base_score *= 1.2
                            elif question_id == "network_security" and characteristic == "security":
                                base_score *= 1.2
                    score += base_score * float(weight)
            
            scores[algorithm] = float(score)
    
    return max(scores.items(), key=lambda x: float(x[1]))[0] if scores else "Não disponível"

def create_empty_recommendation():
    """Create an empty recommendation structure."""
    return {
        "dlt": "Não disponível",
        "consensus": "Não disponível",
        "consensus_group": "Não disponível",
        "group_description": "Não foi possível gerar uma recomendação",
        "evaluation_matrix": {},
        "confidence": False,
        "confidence_value": 0.0,
        "confidence_components": {},
        "group_characteristics": {},
        "weighted_scores": {}
    }

def compare_algorithms(consensus_group):
    """Compare algorithms within a consensus group."""
    if consensus_group not in consensus_groups:
        return {}
    
    algorithms = consensus_groups[consensus_group]['algorithms']
    comparison_data = {
        "Segurança": {},
        "Escalabilidade": {},
        "Eficiência Energética": {},
        "Governança": {}
    }
    
    for alg in algorithms:
        if alg in consensus_algorithms:
            comparison_data["Segurança"][alg] = float(consensus_algorithms[alg].get("security", 3))
            comparison_data["Escalabilidade"][alg] = float(consensus_algorithms[alg].get("scalability", 3))
            comparison_data["Eficiência Energética"][alg] = float(consensus_algorithms[alg].get("energy_efficiency", 3))
            comparison_data["Governança"][alg] = float(consensus_algorithms[alg].get("governance", 3))
    
    return comparison_data
