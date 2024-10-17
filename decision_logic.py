from dlt_data import dlt_options, consensus_options

class DecisionNode:
    def __init__(self, question, yes_node, no_node, recommendation=None):
        self.question = question
        self.yes_node = yes_node
        self.no_node = no_node
        self.recommendation = recommendation

def build_decision_tree():
    # Leaf nodes with recommendations
    leaf_permissioned = DecisionNode(None, None, None, {"dlt": "Permissioned Blockchain", "consensus": "Practical Byzantine Fault Tolerance (PBFT)"})
    leaf_hybrid = DecisionNode(None, None, None, {"dlt": "Hybrid Blockchain", "consensus": "Proof of Authority (PoA)"})
    leaf_public = DecisionNode(None, None, None, {"dlt": "Public Blockchain", "consensus": "Proof of Stake (PoS)"})

    # Build the decision tree
    node_fast = DecisionNode("fast_transactions", leaf_permissioned, leaf_hybrid)
    node_scalability = DecisionNode("high_scalability", node_fast, leaf_hybrid)
    root = DecisionNode("privacy", node_scalability, leaf_public)

    return root

decision_tree = build_decision_tree()

def traverse_tree(node, answers):
    if node.recommendation:
        return node.recommendation
    
    answer = answers.get(node.question, "No")
    if answer == "Yes":
        return traverse_tree(node.yes_node, answers)
    else:
        return traverse_tree(node.no_node, answers)

def get_recommendation(scenario, answers):
    recommendation = traverse_tree(decision_tree, answers)
    
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
    
    decision_path = []
    for question, answer in answers.items():
        decision_path.append(f"{question.replace('_', ' ').title()}: {answer}")
    
    detailed_explanation = f"""
    DLT Recommendation: {recommendation['dlt']}
    {dlt_explanation[recommendation['dlt']]}
    
    Consensus Algorithm Recommendation: {recommendation['consensus']}
    {consensus_explanation[recommendation['consensus']]}
    
    This recommendation is based on your specific requirements for the {scenario} use case.
    The decision path that led to this recommendation:
    {' -> '.join(decision_path)}
    
    The combination of {recommendation['dlt']} with {recommendation['consensus']} provides an optimal solution that addresses your requirements, offering a balance of security, efficiency, and performance tailored to your healthcare application needs.
    """
    
    recommendation['explanation'] = detailed_explanation
    return recommendation
