from dlt_data import dlt_options, consensus_options

class DecisionNode:
    def __init__(self, question, yes_node, no_node, recommendation=None):
        self.question = question
        self.yes_node = yes_node
        self.no_node = no_node
        self.recommendation = recommendation

def build_decision_tree():
    leaf_permissioned = DecisionNode(None, None, None, {"dlt": "Blockchain Permissionado", "consensus": "Tolerância a Falhas Bizantinas Prática (PBFT)"})
    leaf_hybrid = DecisionNode(None, None, None, {"dlt": "Blockchain Híbrido", "consensus": "Prova de Autoridade (PoA)"})
    leaf_public = DecisionNode(None, None, None, {"dlt": "Blockchain Público", "consensus": "Prova de Participação (PoS)"})

    node_fast = DecisionNode("fast_transactions", leaf_permissioned, leaf_hybrid)
    node_scalability = DecisionNode("high_scalability", node_fast, leaf_hybrid)
    root = DecisionNode("privacy", node_scalability, leaf_public)

    return root

decision_tree = build_decision_tree()

def traverse_tree(node, answers):
    if node.recommendation:
        return node.recommendation
    
    answer = answers.get(node.question, "Não")
    if answer == "Sim":
        return traverse_tree(node.yes_node, answers)
    else:
        return traverse_tree(node.no_node, answers)

def get_recommendation(scenario, answers):
    recommendation = traverse_tree(decision_tree, answers)
    
    dlt_explanation = {
        "Blockchain Permissionado": f"Para o seu cenário de {scenario}, um Blockchain Permissionado é recomendado. Este tipo de DLT oferece acesso controlado, crucial para aplicações de saúde onde a privacidade e segurança dos dados são primordiais. Permite processamento de transações mais rápido e melhor escalabilidade em comparação com blockchains públicos, sendo adequado para lidar com grandes volumes de dados médicos sensíveis.",
        "Blockchain Híbrido": f"Considerando seus requisitos para o cenário de {scenario}, um Blockchain Híbrido é sugerido. Esta solução combina elementos de blockchains públicos e privados, oferecendo um equilíbrio entre transparência e privacidade. É particularmente útil em cenários de saúde onde alguns dados precisam ser publicamente acessíveis, mantendo informações sensíveis privadas.",
        "Blockchain Público": f"Com base em suas respostas para o cenário de {scenario}, um Blockchain Público pode ser adequado. Embora ofereça o mais alto nível de transparência e descentralização, é importante notar que em aplicações de saúde, medidas adicionais podem ser necessárias para garantir a privacidade dos dados e conformidade com regulamentações como a LGPD."
    }
    
    consensus_explanation = {
        "Tolerância a Falhas Bizantinas Prática (PBFT)": "PBFT é recomendado por sua capacidade de fornecer alto rendimento de transações com baixa latência, crucial em sistemas de saúde onde o acesso rápido à informação pode salvar vidas. Também é energeticamente eficiente e bem adequado para redes permissionadas, alinhando-se às necessidades de privacidade dos dados de saúde.",
        "Prova de Autoridade (PoA)": "PoA é sugerido por sua eficiência e escalabilidade. Em um contexto de saúde, permite processamento rápido de transações enquanto mantém um nível de confiança através de validadores autorizados. Isso pode ser particularmente útil em cenários onde a tomada de decisão rápida é crucial, como em situações médicas de emergência.",
        "Prova de Participação (PoS)": "PoS é recomendado por sua eficiência energética e velocidade de transação melhorada em comparação com a Prova de Trabalho. Em um ambiente de saúde, pode fornecer um bom equilíbrio entre segurança e desempenho, permitindo atualizações mais rápidas de registros médicos ou informações da cadeia de suprimentos, mantendo a integridade dos dados."
    }
    
    decision_path = []
    for question, answer in answers.items():
        decision_path.append(f"{question.replace('_', ' ').title()}: {answer}")
    
    detailed_explanation = f"""
    Recomendação de DLT: {recommendation['dlt']}
    {dlt_explanation[recommendation['dlt']]}
    
    Recomendação de Algoritmo de Consenso: {recommendation['consensus']}
    {consensus_explanation[recommendation['consensus']]}
    
    Esta recomendação é baseada em seus requisitos específicos para o cenário de {scenario}.
    O caminho de decisão que levou a esta recomendação:
    {' -> '.join(decision_path)}
    
    Impacto das suas escolhas:
    """
    
    for question, answer in answers.items():
        if question == "privacy" and answer == "Sim":
            detailed_explanation += "\n- Sua preocupação com privacidade levou à recomendação de uma solução mais controlada e segura."
        elif question == "high_scalability" and answer == "Sim":
            detailed_explanation += "\n- A necessidade de alta escalabilidade influenciou a escolha de uma solução capaz de lidar com um grande volume de transações."
        elif question == "fast_transactions" and answer == "Sim":
            detailed_explanation += "\n- Sua necessidade de transações rápidas direcionou a recomendação para um algoritmo de consenso mais eficiente."
    
    detailed_explanation += f"""
    
    A combinação de {recommendation['dlt']} com {recommendation['consensus']} fornece uma solução ideal que atende aos seus requisitos, oferecendo um equilíbrio de segurança, eficiência e desempenho adaptado às necessidades da sua aplicação de saúde.
    """
    
    recommendation['explanation'] = detailed_explanation
    return recommendation

def get_sunburst_data():
    def traverse(node, parent=""):
        data = []
        if node.question:
            data.append({"id": node.question, "parent": parent, "name": node.question})
            data.extend(traverse(node.yes_node, node.question))
            data.extend(traverse(node.no_node, node.question))
        elif node.recommendation:
            data.append({
                "id": f"{parent}_{node.recommendation['dlt']}",
                "parent": parent,
                "name": node.recommendation['dlt'],
                "consensus": node.recommendation['consensus']
            })
        return data

    return traverse(decision_tree)
