from dlt_data import questions, dlt_classes, consensus_algorithms

# Updated consensus groups with more detailed characteristics
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

# Updated mapping between DLT types and consensus groups
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

# Academic validation scores
academic_scores = {
    "Hyperledger Fabric": {
        "score": 4.5,
        "citations": 128,
        "reference": "Mehmood et al. (2025) - BLPCA-ledger",
        "validation": "Implementado em hospitais e sistemas de saúde"
    },
    "VeChain": {
        "score": 4.2,
        "citations": 89,
        "reference": "Popoola et al. (2024)",
        "validation": "Usado em cadeias de suprimentos médicos"
    },
    "Quorum": {
        "score": 4.0,
        "citations": 76,
        "reference": "Mehmood et al. (2025)",
        "validation": "Testado em redes hospitalares"
    },
    "IOTA": {
        "score": 4.3,
        "citations": 95,
        "reference": "Salim et al. (2024)",
        "validation": "Implementado em sistemas IoT de saúde"
    }
}

def calculate_dlt_score(dlt_type, metrics_data, weights):
    """
    Calculate the weighted score for a DLT type considering its characteristics
    and academic validation.
    """
    if dlt_type not in dlt_consensus_mapping:
        return 0.0

    mapping = dlt_consensus_mapping[dlt_type]
    group = consensus_groups[mapping['group']]
    
    # Calculate base score from metrics
    base_score = sum(
        float(metrics_data[metric]) * float(weights[metric])
        for metric in mapping['characteristics']
        if metric in metrics_data and metric in weights
    )
    
    # Apply group characteristics bonus
    group_bonus = sum(
        float(group['characteristics'][metric]) * float(weights[metric]) * 0.2
        for metric in mapping['characteristics']
        if metric in group['characteristics'] and metric in weights
    )
    
    # Apply academic validation bonus if available
    academic_bonus = 0.0
    dlt_name = None
    
    if "Hyperledger" in dlt_type:
        dlt_name = "Hyperledger Fabric"
    elif "VeChain" in dlt_type:
        dlt_name = "VeChain"
    elif "Quorum" in dlt_type:
        dlt_name = "Quorum"
    elif "IOTA" in dlt_type:
        dlt_name = "IOTA"
        
    if dlt_name and dlt_name in academic_scores:
        academic_bonus = academic_scores[dlt_name]["score"] * 0.1
    
    # Calculate final score with weight and bonuses
    final_score = (base_score + group_bonus + academic_bonus) * mapping['weight']
    
    return float(final_score)

def get_recommendation(answers, weights):
    """
    Get DLT and consensus algorithm recommendations based on user answers and weights.
    """
    try:
        evaluation_matrix = create_evaluation_matrix(answers)
        
        # Calculate weighted scores for each DLT with error handling
        weighted_scores = {}
        for dlt, data in evaluation_matrix.items():
            try:
                score = calculate_dlt_score(dlt, data['metrics'], weights)
                weighted_scores[dlt] = float(score)
            except (KeyError, ValueError, TypeError) as e:
                print(f"Error calculating score for {dlt}: {str(e)}")
                weighted_scores[dlt] = 0.0
        
        # Find DLT with maximum weighted score
        if not weighted_scores:
            raise ValueError("No valid scores calculated")
            
        recommended_dlt = max(weighted_scores.items(), key=lambda x: float(x[1]))[0]
        
        # Get corresponding consensus group with error handling
        recommended_group = "Não disponível"
        group_description = ""
        group_characteristics = {}
        
        if recommended_dlt in dlt_consensus_mapping:
            mapping = dlt_consensus_mapping[recommended_dlt]
            recommended_group = mapping['group']
            if recommended_group in consensus_groups:
                group_description = consensus_groups[recommended_group].get('description', '')
                group_characteristics = consensus_groups[recommended_group].get('characteristics', {})
        
        # Select best algorithm from the group
        recommended_algorithm = "Não disponível"
        if recommended_group in consensus_groups:
            recommended_algorithm = select_final_algorithm(recommended_group, weights)
        
        # Calculate confidence metrics with error handling
        confidence_scores = list(weighted_scores.values())
        confidence_value = 0.0
        is_reliable = False
        
        if confidence_scores:
            max_score = max(confidence_scores)
            if max_score > 0:
                confidence_value = (max_score - (sum(confidence_scores) / len(confidence_scores))) / max_score
                is_reliable = confidence_value > 0.7
        
        # Get academic validation with error handling
        academic_validation = {}
        for dlt_name, score_data in academic_scores.items():
            if dlt_name.lower() in recommended_dlt.lower():
                academic_validation = score_data
                break
        
        return {
            "dlt": recommended_dlt,
            "consensus": recommended_algorithm,
            "consensus_group": recommended_group,
            "group_description": group_description,
            "evaluation_matrix": evaluation_matrix,
            "confidence": is_reliable,
            "confidence_value": confidence_value,
            "academic_validation": academic_validation,
            "group_characteristics": group_characteristics,
            "weighted_scores": weighted_scores
        }
    except Exception as e:
        print(f"Error in get_recommendation: {str(e)}")
        return {
            "dlt": "Não disponível",
            "consensus": "Não disponível",
            "consensus_group": "Não disponível",
            "group_description": "Não foi possível gerar uma recomendação",
            "evaluation_matrix": {},
            "confidence": False,
            "confidence_value": 0.0,
            "academic_validation": {},
            "group_characteristics": {},
            "weighted_scores": {}
        }

def create_evaluation_matrix(answers):
    """
    Create an evaluation matrix based on user answers.
    """
    matrix = {dlt: {
        "score": 0,
        "metrics": {
            "security": 0,
            "scalability": 0,
            "energy_efficiency": 0,
            "governance": 0,
            "academic_validation": 0
        }
    } for dlt in dlt_consensus_mapping.keys()}
    
    for question_id, answer in answers.items():
        if question_id == "privacy" and answer == "Sim":
            matrix["DLT Permissionada Privada"]["metrics"]["security"] += 2
            matrix["DLT Pública Permissionless"]["metrics"]["security"] += 1
        elif question_id == "integration" and answer == "Sim":
            matrix["DLT Híbrida"]["metrics"]["scalability"] += 2
            matrix["DLT com Consenso Delegado"]["metrics"]["scalability"] += 1
        elif question_id == "data_volume" and answer == "Sim":
            matrix["DLT Pública"]["metrics"]["scalability"] += 2
            matrix["DLT com Consenso Delegado"]["metrics"]["scalability"] += 1
        elif question_id == "energy_efficiency" and answer == "Sim":
            matrix["DLT Permissionada Simples"]["metrics"]["energy_efficiency"] += 2
            matrix["DLT Híbrida"]["metrics"]["energy_efficiency"] += 1
        elif question_id == "network_security" and answer == "Sim":
            matrix["DLT Permissionada Privada"]["metrics"]["security"] += 2
            matrix["DLT Pública Permissionless"]["metrics"]["security"] += 2
        elif question_id == "scalability" and answer == "Sim":
            matrix["DLT com Consenso Delegado"]["metrics"]["scalability"] += 2
            matrix["DLT Pública"]["metrics"]["scalability"] += 2
        elif question_id == "governance_flexibility" and answer == "Sim":
            matrix["DLT Híbrida"]["metrics"]["governance"] += 2
            matrix["DLT com Consenso Delegado"]["metrics"]["governance"] += 1
        elif question_id == "interoperability" and answer == "Sim":
            matrix["DLT Pública"]["metrics"]["scalability"] += 1
            matrix["DLT Híbrida"]["metrics"]["scalability"] += 2

    # Add academic validation scores
    for dlt in matrix:
        for academic_dlt, score_data in academic_scores.items():
            if academic_dlt.lower() in dlt.lower():
                matrix[dlt]["metrics"]["academic_validation"] = score_data["score"]

    # Calculate final scores
    for dlt in matrix:
        total = sum(float(value) for value in matrix[dlt]["metrics"].values())
        matrix[dlt]["score"] = total / len(matrix[dlt]["metrics"])

    return matrix

def select_final_algorithm(consensus_group, weights):
    """
    Select the final consensus algorithm based on the group and weights.
    """
    if consensus_group not in consensus_groups:
        return "Não disponível"
    
    algorithms = consensus_groups[consensus_group]['algorithms']
    scores = {}
    
    for alg in algorithms:
        if alg in consensus_algorithms:
            score = sum(
                float(consensus_algorithms[alg][metric]) * float(weights[metric])
                for metric in weights
                if metric in consensus_algorithms[alg]
            )
            scores[alg] = float(score)
    
    return max(scores.items(), key=lambda x: float(x[1]))[0] if scores else "Não disponível"

def compare_algorithms(consensus_group):
    """
    Compare algorithms within a consensus group.
    """
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
