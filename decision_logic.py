import statistics
from dlt_data import questions, dlt_classes, consensus_algorithms, dlt_metrics, dlt_type_weights

# DLT classification structure based on the provided data
dlt_classification = {
    'Hyperledger Fabric': {
        'type': 'DLT Permissionada Privada',
        'group': 'Alta Segurança e Controle dos Dados',
        'algorithms': ['RAFT', 'IBFT'],
        'technical_characteristics': 'Alta segurança e resiliência contra falhas bizantinas. Máxima proteção de dados sensíveis em redes permissionadas e descentralizadas.',
        'use_cases': 'Rastreabilidade de medicamentos na cadeia de suprimentos',
        'challenges': 'Baixa escalabilidade para redes muito grandes',
        'references': 'Mehmood et al. (2025) - "BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain"'
    },
    'VeChain': {
        'type': 'DLT Híbrida',
        'group': 'Alta Eficiência Operacional em Redes Locais',
        'algorithms': ['PoA'],
        'technical_characteristics': 'Simplicidade e eficiência em redes permissionadas menores. Validação rápida e leve, ideal para redes locais.',
        'use_cases': 'Rastreamento de suprimentos médicos e cadeia farmacêutica',
        'challenges': 'Dependência de validadores centralizados',
        'references': 'Popoola et al. (2024) - "A critical literature review of security and privacy in smart home healthcare schemes adopting IoT & blockchain"'
    },
    'Quorum': {
        'type': 'DLT Híbrida',
        'group': 'Escalabilidade e Governança Flexível',
        'algorithms': ['RAFT', 'IBFT'],
        'technical_characteristics': 'Alta escalabilidade e eficiência energética com governança descentralizada ou semi-descentralizada.',
        'use_cases': 'Monitoramento e rastreamento de medicamentos',
        'challenges': 'Escalabilidade limitada em redes públicas',
        'references': 'Mehmood et al. (2025) - "BLPCA-ledger: A lightweight plenum consensus protocols for consortium blockchain"'
    },
    'IOTA': {
        'type': 'DLT com Consenso Delegado',
        'group': 'Alta Escalabilidade em Redes IoT',
        'algorithms': ['Tangle'],
        'technical_characteristics': 'Alta escalabilidade e eficiência para o monitoramento de dispositivos IoT em tempo real.',
        'use_cases': 'Compartilhamento seguro de dados de pacientes via IoT',
        'challenges': 'Maturidade tecnológica (não totalmente implementada)',
        'references': 'Salim et al. (2024) - "Privacy-preserving and scalable federated blockchain scheme for healthcare 4.0"'
    },
    'Ripple': {
        'type': 'DLT com Consenso Delegado',
        'group': 'Alta Eficiência Operacional em Redes Locais',
        'algorithms': ['Ripple Consensus Algorithm'],
        'technical_characteristics': 'Processamento eficiente de transações e alta segurança de dados.',
        'use_cases': 'Processamento eficiente de transações e segurança de dados',
        'challenges': 'Centralização nos validadores principais',
        'references': 'Makhdoom et al. (2024) - "PrivySeC: A secure and privacy-compliant distributed framework for personal data sharing in IoT ecosystems"'
    },
    'Bitcoin': {
        'type': 'DLT Pública',
        'group': 'Alta Segurança e Descentralização',
        'algorithms': ['PoW'],
        'technical_characteristics': 'Máxima segurança e descentralização para redes públicas.',
        'use_cases': 'Armazenamento seguro de dados médicos críticos',
        'challenges': 'Consumo energético elevado, escalabilidade limitada',
        'references': 'Liu et al. (2024) - "A systematic study on integrating blockchain in healthcare for electronic health record management and tracking medical supplies"'
    },
    'Ethereum (PoW)': {
        'type': 'DLT Pública',
        'group': 'Alta Segurança e Descentralização',
        'algorithms': ['PoW'],
        'technical_characteristics': 'Alta segurança e suporte a contratos inteligentes.',
        'use_cases': 'Contratos inteligentes e registros médicos eletrônicos',
        'challenges': 'Consumo de energia elevado',
        'references': 'Makhdoom et al. (2024) - "PrivySeC: A secure and privacy-compliant distributed framework for personal data sharing in IoT ecosystems"'
    },
    'Ethereum 2.0': {
        'type': 'DLT Pública Permissionless',
        'group': 'Escalabilidade e Governança Flexível',
        'algorithms': ['PoS'],
        'technical_characteristics': 'Alta escalabilidade e eficiência energética com governança flexível.',
        'use_cases': 'Aceleração de ensaios clínicos e compartilhamento de dados',
        'challenges': 'Governança flexível, mas centralização é possível',
        'references': 'Nawaz et al. (2024) - "Hyperledger sawtooth based supply chain traceability system for counterfeit drugs"'
    }
}

def normalize_scores(scores):
    """Normalize scores to a 0-1 range."""
    if not scores:
        return {}
    min_score = min(scores.values())
    max_score = max(scores.values())
    if max_score == min_score:
        return {k: 1.0 for k in scores}
    return {k: (v - min_score) / (max_score - min_score) for k, v in scores.items()}

def get_dlt_type_requirements(answers):
    """Determine DLT type requirements based on user answers."""
    type_scores = {
        'DLT Permissionada Privada': 0,
        'DLT Híbrida': 0,
        'DLT com Consenso Delegado': 0,
        'DLT Pública': 0,
        'DLT Pública Permissionless': 0
    }
    
    if answers.get('privacy') == 'Sim':
        type_scores['DLT Permissionada Privada'] += 2
        type_scores['DLT Híbrida'] += 1
    
    if answers.get('integration') == 'Sim':
        type_scores['DLT Híbrida'] += 2
        type_scores['DLT com Consenso Delegado'] += 1
    
    if answers.get('scalability') == 'Sim':
        type_scores['DLT Pública Permissionless'] += 2
        type_scores['DLT com Consenso Delegado'] += 1
    
    if answers.get('network_security') == 'Sim':
        type_scores['DLT Pública'] += 2
        type_scores['DLT Permissionada Privada'] += 1
    
    return max(type_scores.items(), key=lambda x: x[1])[0]

def get_recommendation(answers):
    """Get DLT and consensus algorithm recommendations based on user answers."""
    if not answers:
        return {
            "dlt": "Não disponível",
            "dlt_type": "Não disponível",
            "group": "Não disponível",
            "algorithms": [],
            "evaluation_matrix": {},
            "metrics": {},
            "details": {}
        }
    
    try:
        # First, determine the required DLT type
        required_type = get_dlt_type_requirements(answers)
        
        # Filter DLTs by type
        candidates = {
            name: info for name, info in dlt_classification.items()
            if info['type'] == required_type
        }
        
        # Calculate scores for candidate DLTs
        scores = {}
        evaluation_matrix = {}
        for dlt_name, dlt_info in candidates.items():
            if dlt_name in dlt_metrics:
                metrics = dlt_metrics[dlt_name]['metrics']
                score = sum(
                    metrics[metric] * weight
                    for metric, weight in dlt_type_weights[required_type].items()
                )
                scores[dlt_name] = score
                evaluation_matrix[dlt_name] = {
                    'type': dlt_info['type'],
                    'group': dlt_info['group'],
                    'algorithms': dlt_info['algorithms'],
                    'metrics': metrics,
                    'score': score
                }
        
        # Normalize scores
        normalized_scores = normalize_scores(scores)
        
        # Select DLT with highest score
        if normalized_scores:
            selected_dlt = max(normalized_scores.items(), key=lambda x: x[1])[0]
            dlt_info = dlt_classification[selected_dlt]
            
            return {
                "dlt": selected_dlt,
                "dlt_type": dlt_info['type'],
                "group": dlt_info['group'],
                "algorithms": dlt_info['algorithms'],
                "evaluation_matrix": evaluation_matrix,
                "metrics": dlt_metrics[selected_dlt]['metrics'],
                "details": {
                    "technical_characteristics": dlt_info['technical_characteristics'],
                    "use_cases": dlt_info['use_cases'],
                    "challenges": dlt_info['challenges'],
                    "references": dlt_info['references']
                }
            }
        
        return {
            "dlt": "Não disponível",
            "dlt_type": "Não disponível",
            "group": "Não disponível",
            "algorithms": [],
            "evaluation_matrix": {},
            "metrics": {},
            "details": {}
        }
        
    except Exception as e:
        print(f"Error in get_recommendation: {str(e)}")
        return {
            "dlt": "Não disponível",
            "dlt_type": "Não disponível",
            "group": "Não disponível",
            "algorithms": [],
            "evaluation_matrix": {},
            "metrics": {},
            "details": {}
        }
