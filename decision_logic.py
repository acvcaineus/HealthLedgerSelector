import statistics
from dlt_data import questions, dlt_classes, consensus_algorithms, dlt_metrics, dlt_type_weights

def calculate_weighted_score(metrics, answers):
    """Calculate weighted score based on metrics and healthcare priorities."""
    weights = {
        'security': 0.40,
        'scalability': 0.25,
        'energy_efficiency': 0.20,
        'governance': 0.15
    }
    
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
    elif answers.get('scalability') == 'Sim' and answers.get('energy_efficiency') == 'Sim':
        selected_group = "Alta Eficiência"
    else:
        selected_group = type_to_group.get(dlt_type, "Alta Segurança e Controle")
    
    explanation = {
        "Alta Segurança e Controle": "Selecionado devido aos requisitos de segurança e privacidade dos dados médicos",
        "Alta Eficiência": "Selecionado devido aos requisitos de eficiência operacional e escalabilidade",
        "Escalabilidade e Governança": "Selecionado devido aos requisitos de flexibilidade e governança",
        "Alta Escalabilidade IoT": "Selecionado devido aos requisitos de IoT e alta escalabilidade"
    }
    
    return {
        "group": selected_group,
        "explanation": explanation.get(selected_group, "")
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

def select_consensus_algorithm(consensus_group, answers):
    """Select the best consensus algorithm from the given group."""
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
        
        weights = {
            'security': 0.40,
            'scalability': 0.25,
            'energy_efficiency': 0.20,
            'governance': 0.15
        }
        
        algorithm_scores = {}
        for algorithm in algorithms:
            if algorithm in characteristics:
                score = sum(weights[metric] * characteristics[algorithm].get(metric, 0.0) 
                          for metric in weights.keys())
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

def get_recommendation(answers):
    """Get DLT and consensus algorithm recommendations based on user answers."""
    if not answers:
        return create_empty_recommendation()
    
    try:
        weighted_scores = {}
        evaluation_matrix = {}
        
        for dlt_name, dlt_info in dlt_metrics.items():
            metrics = dlt_info.get("metrics", {})
            weighted_score = calculate_weighted_score(metrics, answers)
            
            weighted_scores[dlt_name] = weighted_score
            evaluation_matrix[dlt_name] = {
                "type": dlt_info.get("type", "Não disponível"),
                "metrics": metrics,
                "weighted_score": weighted_score
            }
        
        if not weighted_scores:
            return create_empty_recommendation()
            
        recommended_dlt = max(weighted_scores.items(), key=lambda x: x[1])[0]
        dlt_type = dlt_metrics.get(recommended_dlt, {}).get("type", "Não disponível")
        
        consensus_group_info = select_consensus_group(dlt_type, answers)
        algorithm_info = select_consensus_algorithm(consensus_group_info["group"], answers)
        
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
            "confidence_value": confidence_value
        }
        
    except Exception as e:
        print(f"Error in get_recommendation: {str(e)}")
        return create_empty_recommendation()
