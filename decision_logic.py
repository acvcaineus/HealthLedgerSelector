from dlt_data import dlt_options, consensus_options

def get_recommendation(scenario, answers):
    privacy_score = 1 if answers.get('privacy', '') == 'Yes' else 0
    scalability_score = 1 if answers.get('scalability', '') == 'High' else 0
    speed_score = 1 if answers.get('speed', '') == 'Fast' else 0
    transparency_score = 1 if answers.get('transparency', '') == 'Yes' else 0
    auditability_score = 1 if answers.get('auditability', '') == 'Yes' else 0
    
    total_score = privacy_score + scalability_score + speed_score + transparency_score + auditability_score
    
    if total_score >= 3:
        dlt = "Permissioned Blockchain"
        consensus = "Practical Byzantine Fault Tolerance (PBFT)"
    elif total_score == 2:
        dlt = "Hybrid Blockchain"
        consensus = "Proof of Authority (PoA)"
    else:
        dlt = "Public Blockchain"
        consensus = "Proof of Stake (PoS)"
    
    dlt_explanation = {
        "Permissioned Blockchain": f"For your {scenario} use case, a Permissioned Blockchain is recommended. This type of DLT offers controlled access, which is crucial for healthcare applications where data privacy and security are paramount. It allows for faster transaction processing and better scalability compared to public blockchains, making it suitable for handling large volumes of sensitive medical data.",
        "Hybrid Blockchain": f"Considering your requirements for the {scenario}, a Hybrid Blockchain is suggested. This solution combines elements of both public and private blockchains, offering a balance between transparency and privacy. It's particularly useful in healthcare scenarios where some data needs to be publicly accessible while keeping sensitive information private.",
        "Public Blockchain": f"Based on your answers for the {scenario}, a Public Blockchain could be suitable. While it offers the highest level of transparency and decentralization, it's important to note that in healthcare applications, additional measures may be needed to ensure data privacy and compliance with regulations like HIPAA."
    }
    
    consensus_explanation = {
        "Practical Byzantine Fault Tolerance (PBFT)": "PBFT is recommended for its ability to provide high transaction throughput with low latency, which is crucial in healthcare systems where quick access to information can be life-saving. It's also energy-efficient and well-suited for permissioned networks, aligning with the privacy needs of healthcare data.",
        "Proof of Authority (PoA)": "PoA is suggested for its efficiency and scalability. In a healthcare context, it allows for fast transaction processing while maintaining a level of trust through authorized validators. This can be particularly useful in scenarios where quick decision-making is crucial, such as in emergency medical situations.",
        "Proof of Stake (PoS)": "PoS is recommended for its energy efficiency and improved transaction speed compared to Proof of Work. In a healthcare setting, it can provide a good balance between security and performance, allowing for faster updates to medical records or supply chain information while maintaining the integrity of the data."
    }
    
    detailed_explanation = f"""
    DLT Recommendation: {dlt}
    {dlt_explanation[dlt]}
    
    Consensus Algorithm Recommendation: {consensus}
    {consensus_explanation[consensus]}
    
    This recommendation is based on your specific requirements for the {scenario} use case:
    - Privacy: {"High priority" if privacy_score else "Lower priority"}
    - Scalability: {"High" if scalability_score else "Lower"}
    - Speed: {"Fast" if speed_score else "Not as critical"}
    - Transparency: {"Required" if transparency_score else "Not as important"}
    - Auditability: {"Critical" if auditability_score else "Less emphasized"}
    
    The combination of {dlt} with {consensus} provides an optimal solution that addresses these requirements, offering a balance of security, efficiency, and performance tailored to your healthcare application needs.
    """
    
    return {
        "dlt": dlt,
        "consensus": consensus,
        "explanation": detailed_explanation
    }
