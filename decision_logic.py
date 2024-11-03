import statistics
from dlt_data import questions, dlt_classes, consensus_algorithms, dlt_metrics, dlt_type_weights

# Reference data for DLTs
dlt_reference_data = {
    'Hyperledger Fabric': {
        'technical_characteristics': 'Alta segurança e resiliência contra falhas bizantinas. Máxima proteção de dados sensíveis em redes permissionadas e descentralizadas.',
        'use_cases': 'Rastreabilidade de medicamentos na cadeia de suprimentos',
        'challenges': 'Baixa escalabilidade para redes muito grandes',
        'references': 'Mehmood et al. (2025) - "BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain"'
    },
    'VeChain': {
        'technical_characteristics': 'Simplicidade e eficiência em redes permissionadas menores. Validação rápida e leve, ideal para redes locais.',
        'use_cases': 'Rastreamento de suprimentos médicos e cadeia farmacêutica',
        'challenges': 'Dependência de validadores centralizados',
        'references': 'Popoola et al. (2024) - "A critical literature review of security and privacy in smart home healthcare schemes adopting IoT & blockchain"'
    },
    'Quorum': {
        'technical_characteristics': 'Alta escalabilidade e eficiência energética com governança descentralizada ou semi-descentralizada.',
        'use_cases': 'Monitoramento e rastreamento de medicamentos',
        'challenges': 'Escalabilidade limitada em redes públicas',
        'references': 'Mehmood et al. (2025) - "BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain"'
    },
    'IOTA': {
        'technical_characteristics': 'Alta escalabilidade e eficiência para o monitoramento de dispositivos IoT em tempo real.',
        'use_cases': 'Compartilhamento seguro de dados de pacientes via IoT',
        'challenges': 'Maturidade tecnológica (não totalmente implementada)',
        'references': 'Salim et al. (2024) - "Privacy-preserving and scalable federated blockchain scheme for healthcare 4.0"'
    },
    'Ripple': {
        'technical_characteristics': 'Processamento eficiente de transações e alta segurança de dados.',
        'use_cases': 'Processamento eficiente de transações e segurança de dados',
        'challenges': 'Centralização nos validadores principais',
        'references': 'Makhdoom et al. (2024) - "PrivySeC: A secure and privacy-compliant distributed framework for personal data sharing in IoT ecosystems"'
    },
    'Bitcoin': {
        'technical_characteristics': 'Máxima segurança e descentralização para redes públicas.',
        'use_cases': 'Armazenamento seguro de dados médicos críticos',
        'challenges': 'Consumo energético elevado, escalabilidade limitada',
        'references': 'Liu et al. (2024) - "A systematic study on integrating blockchain in healthcare for electronic health record management and tracking medical supplies"'
    },
    'Ethereum (PoW)': {
        'technical_characteristics': 'Alta segurança e suporte a contratos inteligentes.',
        'use_cases': 'Contratos inteligentes e registros médicos eletrônicos',
        'challenges': 'Consumo de energia elevado',
        'references': 'Makhdoom et al. (2024) - "PrivySeC: A secure and privacy-compliant distributed framework for personal data sharing in IoT ecosystems"'
    },
    'Ethereum 2.0': {
        'technical_characteristics': 'Alta escalabilidade e eficiência energética com governança flexível.',
        'use_cases': 'Aceleração de ensaios clínicos e compartilhamento de dados',
        'challenges': 'Governança flexível, mas centralização é possível',
        'references': 'Nawaz et al. (2024) - "Hyperledger sawtooth based supply chain traceability system for counterfeit drugs"'
    }
}

def normalize_scores(scores):
    """Normalize scores to a 0-1 range."""
    min_score = min(scores.values())
    max_score = max(scores.values())
    if max_score == min_score:
        return {k: 1.0 for k in scores}
    return {k: (v - min_score) / (max_score - min_score) for k, v in scores.items()}

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
    
    for weight, related_questions in weight_adjustments.items():
        for question, adjustment in related_questions.items():
            if answers.get(question) == 'Sim':
                adjusted_weights[weight] += adjustment
                weight_explanations[weight].append(
                    next(q['text'] for q in questions if q['id'] == question)
                )
    
    total = sum(adjusted_weights.values())
    adjusted_weights = {k: v/total for k, v in adjusted_weights.items()}
    
    return adjusted_weights, weight_explanations

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
                score = sum(characteristics[algorithm][metric] * weight 
                          for metric, weight in weights.items())
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
            weighted_score = sum(metrics[metric] * weight 
                              for metric, weight in adjusted_weights.items())
            
            weighted_scores[dlt_name] = weighted_score
            evaluation_matrix[dlt_name] = {
                "type": dlt_info.get("type", "Não disponível"),
                "metrics": metrics,
                "weighted_score": weighted_score
            }
        
        # Normalize scores
        normalized_scores = normalize_scores(weighted_scores)
        
        # Select DLT with highest normalized score
        recommended_dlt = max(normalized_scores.items(), key=lambda x: x[1])[0]
        dlt_type = dlt_metrics.get(recommended_dlt, {}).get("type", "Não disponível")
        
        # Get consensus group based on DLT type and answers
        consensus_group_info = select_consensus_group(dlt_type, answers)
        
        # Select best consensus algorithm using adjusted weights
        algorithm_info = select_consensus_algorithm(
            consensus_group_info["group"],
            answers,
            adjusted_weights
        )
        
        confidence_value = calculate_confidence(normalized_scores, 
                                           evaluation_matrix.get(recommended_dlt, {}).get("metrics", {}),
                                           answers)
        
        # Get detailed information from reference data
        dlt_details = dlt_reference_data.get(recommended_dlt, {})
        
        return {
            "dlt": recommended_dlt,
            "dlt_type": dlt_type,
            "consensus_group": consensus_group_info["group"],
            "consensus_group_explanation": consensus_group_info["explanation"],
            "consensus": algorithm_info["algorithm"],
            "consensus_characteristics": algorithm_info["characteristics"],
            "consensus_score": algorithm_info["score"],
            "evaluation_matrix": evaluation_matrix,
            "weighted_scores": normalized_scores,
            "confidence": confidence_value > 0.7,
            "confidence_value": confidence_value,
            "adjusted_weights": adjusted_weights,
            "weight_explanations": weight_explanations,
            "dlt_details": dlt_details
        }
        
    except Exception as e:
        print(f"Error in get_recommendation: {str(e)}")
        return create_empty_recommendation()
