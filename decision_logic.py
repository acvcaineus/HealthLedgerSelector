from dlt_data import dlt_options, consensus_options

def get_recommendation(scenario, answers):
    # This is a simplified decision logic. In a real-world application,
    # this would be much more complex and based on expert knowledge.
    
    privacy_score = 1 if answers.get('privacy', '') == 'Yes' else 0
    scalability_score = 1 if answers.get('scalability', '') == 'High' else 0
    speed_score = 1 if answers.get('speed', '') == 'Fast' else 0
    
    total_score = privacy_score + scalability_score + speed_score
    
    if total_score >= 2:
        dlt = "Permissioned Blockchain"
        consensus = "Practical Byzantine Fault Tolerance (PBFT)"
    else:
        dlt = "Public Blockchain"
        consensus = "Proof of Stake (PoS)"
    
    explanation = f"Based on your requirements for privacy, scalability, and speed, we recommend a {dlt} with {consensus} consensus algorithm. This combination provides a good balance of security, efficiency, and performance for your {scenario} use case."
    
    return {
        "dlt": dlt,
        "consensus": consensus,
        "explanation": explanation
    }
