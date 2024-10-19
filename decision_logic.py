from dlt_data import questions, dlt_classes, consensus_algorithms, metrics

def get_recommendation(answers, weights):
    score = {
        "Public Blockchain": 0,
        "Permissioned Blockchain": 0,
        "Private Blockchain": 0,
        "Hybrid Blockchain": 0,
        "Distributed Ledger": 0,
        "Consortium Blockchain": 0
    }

    # Calcula as pontuações de acordo com as respostas e os pesos
    for question_id, answer in answers.items():
        if question_id == "privacy" and answer == "Sim":
            score["Permissioned Blockchain"] += 2 * weights["security"]
            score["Private Blockchain"] += 2 * weights["security"]
            score["Consortium Blockchain"] += 2 * weights["security"]
        elif question_id == "integration" and answer == "Sim":
            score["Hybrid Blockchain"] += 2 * weights["scalability"]
            score["Distributed Ledger"] += 1 * weights["scalability"]
        elif question_id == "data_volume" and answer == "Sim":
            score["Distributed Ledger"] += 2 * weights["scalability"]
            score["Public Blockchain"] += 1 * weights["scalability"]
        elif question_id == "energy_efficiency" and answer == "Sim":
            score["Permissioned Blockchain"] += 1 * weights["energy_efficiency"]
            score["Private Blockchain"] += 1 * weights["energy_efficiency"]
            score["Distributed Ledger"] += 2 * weights["energy_efficiency"]
        elif question_id == "network_security" and answer == "Sim":
            score["Public Blockchain"] += 2 * weights["security"]
            score["Consortium Blockchain"] += 1 * weights["security"]
        elif question_id == "scalability" and answer == "Sim":
            score["Public Blockchain"] += 1 * weights["scalability"]
            score["Distributed Ledger"] += 2 * weights["scalability"]
        elif question_id == "governance_flexibility" and answer == "Sim":
            score["Consortium Blockchain"] += 2 * weights["governance"]
            score["Hybrid Blockchain"] += 1 * weights["governance"]
        elif question_id == "interoperability" and answer == "Sim":
            score["Hybrid Blockchain"] += 2 * weights["scalability"]
            score["Public Blockchain"] += 1 * weights["scalability"]

    # Recomenda a DLT com a maior pontuação
    recommended_dlt = max(score, key=score.get)

    # Calcula a pontuação para os algoritmos de consenso
    consensus_score = {
        "Proof of Stake (PoS)": 0,
        "Proof of Work (PoW)": 0,
        "Practical Byzantine Fault Tolerance (PBFT)": 0,
        "Delegated Proof of Stake (DPoS)": 0,
        "Proof of Authority (PoA)": 0,
        "Raft Consensus": 0,
        "Directed Acyclic Graph (DAG)": 0,
        "Nominated Proof of Stake (NPoS)": 0,
        "Tangle": 0
    }

    if recommended_dlt in ["Public Blockchain", "Hybrid Blockchain"]:
        consensus_score["Proof of Stake (PoS)"] += 2 * weights["energy_efficiency"]
        consensus_score["Proof of Work (PoW)"] += 1 * weights["security"]
        consensus_score["Delegated Proof of Stake (DPoS)"] += 2 * weights["scalability"]
    elif recommended_dlt in ["Permissioned Blockchain", "Private Blockchain", "Consortium Blockchain"]:
        consensus_score["Practical Byzantine Fault Tolerance (PBFT)"] += 2 * weights["security"]
        consensus_score["Proof of Authority (PoA)"] += 2 * weights["governance"]
        consensus_score["Raft Consensus"] += 1 * weights["scalability"]
    elif recommended_dlt == "Distributed Ledger":
        consensus_score["Directed Acyclic Graph (DAG)"] += 2 * weights["scalability"]
        consensus_score["Tangle"] += 2 * weights["scalability"]

    # Ajusta a pontuação com base na eficiência energética e escalabilidade
    if answers.get("energy_efficiency") == "Sim":
        consensus_score["Proof of Stake (PoS)"] += 1 * weights["energy_efficiency"]
        consensus_score["Practical Byzantine Fault Tolerance (PBFT)"] += 1 * weights["energy_efficiency"]
        consensus_score["Proof of Authority (PoA)"] += 1 * weights["energy_efficiency"]

    if answers.get("scalability") == "Sim":
        consensus_score["Delegated Proof of Stake (DPoS)"] += 1 * weights["scalability"]
        consensus_score["Directed Acyclic Graph (DAG)"] += 2 * weights["scalability"]
        consensus_score["Tangle"] += 2 * weights["scalability"]

    # Recomenda o algoritmo de consenso com a maior pontuação
    recommended_consensus = max(consensus_score, key=consensus_score.get)

    return {
        "dlt": recommended_dlt,
        "consensus": recommended_consensus,
        "dlt_explanation": dlt_classes[recommended_dlt],
        "consensus_explanation": consensus_algorithms[recommended_consensus]
    }

def get_comparison_data(recommended_dlt, recommended_consensus):
    dlt_consensus_mapping = {
        "Public Blockchain": "Bitcoin (PoW)",
        "Permissioned Blockchain": "Hyperledger Fabric (PBFT)",
        "Private Blockchain": "Quorum (RAFT)",
        "Hybrid Blockchain": "VeChain (PoA)",
        "Distributed Ledger": "IOTA",
        "Consortium Blockchain": "Hyperledger Fabric (PBFT)"
    }

    recommended_system = dlt_consensus_mapping.get(recommended_dlt, "Ethereum (PoW/PoS)")
    comparison_data = {}

    for metric, values in metrics.items():
        comparison_data[metric] = {
            "Recomendado": values[recommended_system],
            "Bitcoin (PoW)": values["Bitcoin (PoW)"],
            "Ethereum 2.0 (PoS)": values["Ethereum 2.0 (PoS)"],
            "Hyperledger Fabric (PBFT)": values["Hyperledger Fabric (PBFT)"]
        }

    return comparison_data

def get_sunburst_data():
    return [
        {"id": "DLT", "parent": "", "name": "Tecnologias DLT"},
        {"id": "Public", "parent": "DLT", "name": "Blockchain Público"},
        {"id": "Private", "parent": "DLT", "name": "Blockchain Privado"},
        {"id": "Permissioned", "parent": "DLT", "name": "Blockchain Permissionado"},
        {"id": "Hybrid", "parent": "DLT", "name": "Blockchain Híbrido"},
        {"id": "PoW", "parent": "Public", "name": "Proof of Work", "consensus": "PoW"},
        {"id": "PoS", "parent": "Public", "name": "Proof of Stake", "consensus": "PoS"},
        {"id": "PBFT", "parent": "Private", "name": "PBFT", "consensus": "PBFT"},
        {"id": "PoA", "parent": "Permissioned", "name": "Proof of Authority", "consensus": "PoA"},
        {"id": "Raft", "parent": "Private", "name": "Raft", "consensus": "Raft"},
        {"id": "DPoS", "parent": "Hybrid", "name": "Delegated Proof of Stake", "consensus": "DPoS"}
    ]