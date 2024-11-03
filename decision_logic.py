import statistics
from dlt_data import questions, dlt_classes, consensus_algorithms, dlt_metrics, dlt_type_weights

def get_adjusted_weights(answers):
    """Calculate adjusted weights based on user answers."""
    base_weights = {
        'security': 0.40,
        'scalability': 0.25,
        'energy_efficiency': 0.20,
        'governance': 0.15
    }
    
    weight_adjustments = {
        'security': {
            'privacy': 0.1,
            'network_security': 0.1
        },
        'scalability': {
            'data_volume': 0.1,
            'scalability': 0.1
        },
        'energy_efficiency': {
            'energy_efficiency': 0.1
        },
        'governance': {
            'governance_flexibility': 0.1,
            'interoperability': 0.1
        }
    }
    
    adjusted_weights = base_weights.copy()
    weight_explanations = {k: [] for k in base_weights.keys()}
    
    # Apply adjustments based on answers
    for weight, related_questions in weight_adjustments.items():
        for question, adjustment in related_questions.items():
            if answers.get(question) == 'Sim':
                adjusted_weights[weight] += adjustment
                weight_explanations[weight].append(
                    next(q['text'] for q in questions if q['id'] == question)
                )
    
    # Normalize weights to sum to 1
    total = sum(adjusted_weights.values())
    adjusted_weights = {k: v/total for k, v in adjusted_weights.items()}
    
    return adjusted_weights, weight_explanations

def calculate_weighted_score(metrics, weights):
    """Calculate weighted score based on metrics and adjusted weights."""
    return sum(metrics[metric] * weights[metric] for metric in metrics.keys())

def select_consensus_group(dlt_type, answers):
    """Select the consensus group based on DLT type and healthcare requirements."""
    type_to_group = {
        "DLT Permissionada Privada": "Alta Segurança e Controle",
        "DLT Permissionada Simples": "Alta Eficiência",
        "DLT Híbrida": "Escalabilidade e Governança",
        "DLT com Consenso Delegado": "Alta Escalabilidade IoT",
        "DLT Pública": "Alta Segurança e Controle",
        "DLT Pública Permissionless": "Escalabilidade e Governança"
    }
    
    if answers.get('network_security') == 'Sim' and answers.get('privacy') == 'Sim':
        selected_group = "Alta Segurança e Controle"
        reason = "requisitos elevados de segurança e privacidade"
    elif answers.get('scalability') == 'Sim' and answers.get('energy_efficiency') == 'Sim':
        selected_group = "Alta Eficiência"
        reason = "necessidade de alta eficiência e escalabilidade"
    elif answers.get('data_volume') == 'Sim' and answers.get('interoperability') == 'Sim':
        selected_group = "Escalabilidade e Governança"
        reason = "requisitos de volume de dados e interoperabilidade"
    else:
        selected_group = type_to_group.get(dlt_type, "Alta Segurança e Controle")
        reason = f"características padrão do tipo de DLT ({dlt_type})"
    
    explanation = f"Grupo selecionado devido a {reason}. "
    explanation += "Este grupo oferece o melhor equilíbrio entre as características necessárias para seu caso de uso."
    
    return {
        "group": selected_group,
        "explanation": explanation
    }

def get_consensus_group_algorithms(group_name):
    """Get available algorithms for a specific consensus group."""
    group_algorithms = {
        "Alta Segurança e Controle": {
            "algorithms": ["PBFT", "PoW"],
            "characteristics": {
                "PBFT": {
                    "security": 0.95,
                    "scalability": 0.70,
                    "energy_efficiency": 0.85,
                    "governance": 0.80
                },
                "PoW": {
                    "security": 0.90,
                    "scalability": 0.40,
                    "energy_efficiency": 0.35,
                    "governance": 0.60
                }
            }
        },
        "Alta Eficiência": {
            "algorithms": ["PoA", "RAFT"],
            "characteristics": {
                "PoA": {
                    "security": 0.75,
                    "scalability": 0.85,
                    "energy_efficiency": 0.90,
                    "governance": 0.70
                },
                "RAFT": {
                    "security": 0.70,
                    "scalability": 0.90,
                    "energy_efficiency": 0.95,
                    "governance": 0.75
                }
            }
        },
        "Escalabilidade e Governança": {
            "algorithms": ["PoS", "DPoS"],
            "characteristics": {
                "PoS": {
                    "security": 0.85,
                    "scalability": 0.80,
                    "energy_efficiency": 0.90,
                    "governance": 0.85
                },
                "DPoS": {
                    "security": 0.80,
                    "scalability": 0.90,
                    "energy_efficiency": 0.85,
                    "governance": 0.90
                }
            }
        },
        "Alta Escalabilidade IoT": {
            "algorithms": ["Tangle", "DAG"],
            "characteristics": {
                "Tangle": {
                    "security": 0.75,
                    "scalability": 0.95,
                    "energy_efficiency": 0.90,
                    "governance": 0.70
                },
                "DAG": {
                    "security": 0.70,
                    "scalability": 0.95,
                    "energy_efficiency": 0.95,
                    "governance": 0.75
                }
            }
        }
    }
    
    return group_algorithms.get(group_name, {"algorithms": [], "characteristics": {}})

def create_empty_characteristics():
    """Create default characteristics structure."""
    return {
        "security": 0.0,
        "scalability": 0.0,
        "energy_efficiency": 0.0,
        "governance": 0.0
    }

def calculate_confidence(weighted_scores, characteristics, answers):
    """Calculate confidence score for the recommendation."""
    if not weighted_scores:
        return 0.0
    
    try:
        max_score = max(weighted_scores.values())
        mean_score = statistics.mean(weighted_scores.values())
        std_dev = statistics.stdev(weighted_scores.values())
        
        separation_factor = (max_score - mean_score) / max_score if max_score > 0 else 0
        consistency_factor = 1 - (std_dev / max_score) if max_score > 0 else 0
        answer_consistency = sum(1 for ans in answers.values() if ans == "Sim") / len(answers) if answers else 0
        
        confidence = (
            separation_factor * 0.40 +
            consistency_factor * 0.35 +
            answer_consistency * 0.25
        )
        
        return confidence
    except (statistics.StatisticsError, ValueError, ZeroDivisionError):
        return 0.0

def create_empty_recommendation():
    """Create an empty recommendation structure with proper initialization."""
    return {
        "dlt": "Não disponível",
        "dlt_type": "Não disponível",
        "consensus_group": "Não disponível",
        "consensus_group_explanation": "",
        "consensus": "Não disponível",
        "consensus_characteristics": create_empty_characteristics(),
        "consensus_score": 0.0,
        "evaluation_matrix": {},
        "weighted_scores": {},
        "confidence": False,
        "confidence_value": 0.0
    }

def select_consensus_algorithm(consensus_group, answers, weights):
    """Select the best consensus algorithm from the given group using adjusted weights."""
    try:
        group_info = get_consensus_group_algorithms(consensus_group)
        algorithms = group_info.get("algorithms", [])
        characteristics = group_info.get("characteristics", {})
        
        if not algorithms:
            return {
                "algorithm": "Não disponível",
                "score": 0.0,
                "characteristics": create_empty_characteristics()
            }
        
        algorithm_scores = {}
        for algorithm in algorithms:
            if algorithm in characteristics:
                score = calculate_weighted_score(characteristics[algorithm], weights)
                algorithm_scores[algorithm] = score
        
        if not algorithm_scores:
            return {
                "algorithm": algorithms[0],
                "score": 0.0,
                "characteristics": create_empty_characteristics()
            }
        
        selected_algorithm = max(algorithm_scores.items(), key=lambda x: x[1])
        return {
            "algorithm": selected_algorithm[0],
            "score": selected_algorithm[1],
            "characteristics": characteristics.get(selected_algorithm[0], create_empty_characteristics())
        }
    except Exception as e:
        print(f"Error in select_consensus_algorithm: {str(e)}")
        return {
            "algorithm": "Não disponível",
            "score": 0.0,
            "characteristics": create_empty_characteristics()
        }

def get_recommendation(answers):
    """Get DLT and consensus algorithm recommendations based on user answers."""
    if not answers:
        return create_empty_recommendation()
    
    try:
        # Calculate adjusted weights based on user answers
        adjusted_weights, weight_explanations = get_adjusted_weights(answers)
        
        weighted_scores = {}
        evaluation_matrix = {}
        
        # Calculate scores for each DLT using adjusted weights
        for dlt_name, dlt_info in dlt_metrics.items():
            metrics = dlt_info.get("metrics", {})
            weighted_score = calculate_weighted_score(metrics, adjusted_weights)
            
            weighted_scores[dlt_name] = weighted_score
            evaluation_matrix[dlt_name] = {
                "type": dlt_info.get("type", "Não disponível"),
                "metrics": metrics,
                "weighted_score": weighted_score
            }
        
        if not weighted_scores:
            return create_empty_recommendation()
        
        # Select DLT with highest weighted score
        recommended_dlt = max(weighted_scores.items(), key=lambda x: x[1])[0]
        dlt_type = dlt_metrics.get(recommended_dlt, {}).get("type", "Não disponível")
        
        # Get consensus group based on DLT type and answers
        consensus_group_info = select_consensus_group(dlt_type, answers)
        
        # Select best consensus algorithm using adjusted weights
        algorithm_info = select_consensus_algorithm(
            consensus_group_info["group"],
            answers,
            adjusted_weights
        )
        
        confidence_value = calculate_confidence(weighted_scores, 
                                           evaluation_matrix.get(recommended_dlt, {}).get("metrics", {}),
                                           answers)
        
        return {
            "dlt": recommended_dlt,
            "dlt_type": dlt_type,
            "consensus_group": consensus_group_info["group"],
            "consensus_group_explanation": consensus_group_info["explanation"],
            "consensus": algorithm_info["algorithm"],
            "consensus_characteristics": algorithm_info["characteristics"],
            "consensus_score": algorithm_info["score"],
            "evaluation_matrix": evaluation_matrix,
            "weighted_scores": weighted_scores,
            "confidence": confidence_value > 0.7,
            "confidence_value": confidence_value,
            "adjusted_weights": adjusted_weights,
            "weight_explanations": weight_explanations
        }
        
    except Exception as e:
        print(f"Error in get_recommendation: {str(e)}")
        return create_empty_recommendation()
