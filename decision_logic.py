from dlt_data import questions, dlt_classes, consensus_algorithms

def get_recommendation(answers, weights):
    score = {
        "Public Blockchain": 0,
        "Permissioned Blockchain": 0,
        "Private Blockchain": 0,
        "Hybrid Blockchain": 0,
        "Distributed Ledger": 0,
        "Consortium Blockchain": 0
    }

    # Calculate scores based on answers and weights
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

    # Recommend the DLT with the highest score
    recommended_dlt = max(score, key=score.get)

    # Calculate scores for consensus algorithms
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

    # Adjust scores based on energy efficiency and scalability
    if answers.get("energy_efficiency") == "Sim":
        consensus_score["Proof of Stake (PoS)"] += 1 * weights["energy_efficiency"]
        consensus_score["Practical Byzantine Fault Tolerance (PBFT)"] += 1 * weights["energy_efficiency"]
        consensus_score["Proof of Authority (PoA)"] += 1 * weights["energy_efficiency"]

    if answers.get("scalability") == "Sim":
        consensus_score["Delegated Proof of Stake (DPoS)"] += 1 * weights["scalability"]
        consensus_score["Directed Acyclic Graph (DAG)"] += 2 * weights["scalability"]
        consensus_score["Tangle"] += 2 * weights["scalability"]

    # Recommend the consensus algorithm with the highest score
    recommended_consensus = max(consensus_score, key=consensus_score.get)

    return {
        "dlt": recommended_dlt,
        "consensus": recommended_consensus
    }

def get_comparison_data(recommended_dlt, recommended_consensus):
    # This is a simplified comparison. In a real-world scenario, you would have more detailed data.
    comparison_data = {
        "Security": {
            recommended_consensus: 5,
            "Proof of Stake (PoS)": 4,
            "Proof of Work (PoW)": 5,
            "Practical Byzantine Fault Tolerance (PBFT)": 4
        },
        "Scalability": {
            recommended_consensus: 4,
            "Proof of Stake (PoS)": 4,
            "Proof of Work (PoW)": 2,
            "Practical Byzantine Fault Tolerance (PBFT)": 3
        },
        "Energy Efficiency": {
            recommended_consensus: 4,
            "Proof of Stake (PoS)": 5,
            "Proof of Work (PoW)": 1,
            "Practical Byzantine Fault Tolerance (PBFT)": 4
        },
        "Governance": {
            recommended_consensus: 3,
            "Proof of Stake (PoS)": 4,
            "Proof of Work (PoW)": 2,
            "Practical Byzantine Fault Tolerance (PBFT)": 3
        }
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
