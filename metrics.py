import math
import numpy as np

def calcular_gini(classes):
    """
    Calcula a impureza de Gini para um conjunto de classes.
    A impureza de Gini é uma medida de quão frequentemente um elemento seria 
    incorretamente classificado se fosse classificado aleatoriamente.
    
    Fórmula: Gini = 1 - Σ(pi²), onde pi é a proporção de cada classe
    Interpretação:
    - Valor próximo a 0: Indica boa separação entre as classes
    - Valor próximo a 1: Indica maior mistura entre as classes
    """
    total = sum(classes.values())
    gini = 1 - sum((count / total) ** 2 for count in classes.values())
    return gini

def calcular_entropia(classes):
    """
    Calcula a entropia de Shannon para um conjunto de classes.
    A entropia mede a aleatoriedade ou imprevisibilidade em um conjunto de dados.
    
    Fórmula: Entropia = -Σ(pi * log2(pi)), onde pi é a proporção de cada classe
    Interpretação:
    - Valor baixo: Indica maior certeza na decisão
    - Valor alto: Indica maior incerteza na decisão
    """
    total = sum(classes.values())
    entropia = -sum((count / total) * math.log2(count / total) 
                   for count in classes.values() if count != 0)
    return entropia

def calcular_profundidade_decisoria(decisoes):
    """
    Calcula a profundidade média da árvore de decisão.
    Uma profundidade menor indica um modelo mais simples e interpretável.
    
    Fórmula: Profundidade Média = Σ(profundidades) / número de decisões
    Interpretação:
    - Valor baixo: Indica processo decisório mais direto
    - Valor alto: Indica processo decisório mais complexo
    """
    if not decisoes:
        return 0
    try:
        # Convert all elements to integers and filter out non-numeric values
        decisoes_numericas = [int(i) for i in range(len(decisoes))]
        if not decisoes_numericas:
            return 0
        profundidade_total = sum(decisoes_numericas)
        return profundidade_total / len(decisoes_numericas)
    except (ValueError, TypeError):
        return 0

def calcular_pruning(total_nos, nos_podados):
    """
    Calcula o pruning ratio (proporção de nós podados).
    Indica a eficácia da simplificação do modelo.
    
    Fórmula: Pruning Ratio = (total_nós - nós_podados) / total_nós
    Interpretação:
    - Valor próximo a 0: Pouca simplificação
    - Valor próximo a 1: Alta simplificação
    """
    if total_nos == 0:
        return 0
    pruning_ratio = (total_nos - nos_podados) / total_nos
    return pruning_ratio

def calcular_peso_caracteristica(caracteristica, pesos):
    """
    Calcula o peso normalizado de uma característica específica.
    
    Fórmula: Peso Normalizado = peso_característica / Σ(todos os pesos)
    Interpretação:
    - Valor alto: Característica mais relevante
    - Valor baixo: Característica menos relevante
    """
    total_pesos = sum(pesos.values())
    return pesos.get(caracteristica, 0) / total_pesos if total_pesos > 0 else 0

def calcular_jaccard_similarity(conjunto_a, conjunto_b):
    """
    Calcula o índice de similaridade de Jaccard entre dois conjuntos.
    
    Fórmula: J(A,B) = |A ∩ B| / |A ∪ B|
    Interpretação:
    - Valor próximo a 1: Alta similaridade
    - Valor próximo a 0: Baixa similaridade
    """
    if not conjunto_a or not conjunto_b:
        return 0
    intersecao = len(set(conjunto_a) & set(conjunto_b))
    uniao = len(set(conjunto_a) | set(conjunto_b))
    return intersecao / uniao if uniao > 0 else 0

def calcular_confiabilidade_recomendacao(scores, threshold=0.7):
    """
    Calcula a confiabilidade da recomendação baseada nos scores.
    
    Fórmula: Confiabilidade = (max_score - mean_score) / max_score
    Interpretação:
    - Valor > threshold: Alta confiabilidade
    - Valor ≤ threshold: Média confiabilidade
    """
    if not scores:
        return 0
    max_score = max(scores)
    mean_score = sum(scores) / len(scores)
    confiabilidade = (max_score - mean_score) / max_score if max_score > 0 else 0
    return confiabilidade > threshold

def calcular_metricas_desempenho(historico_recomendacoes):
    """
    Calcula métricas de desempenho do sistema de recomendação.
    Retorna precisão, recall e F1-score.
    
    Interpretação:
    - Precisão: Proporção de recomendações corretas
    - Recall: Proporção de casos positivos identificados
    - F1-score: Média harmônica entre precisão e recall
    """
    if not historico_recomendacoes:
        return 0, 0, 0
    
    true_positives = sum(1 for rec in historico_recomendacoes if rec['acerto'])
    false_positives = sum(1 for rec in historico_recomendacoes if not rec['acerto'])
    total = len(historico_recomendacoes)
    
    precisao = true_positives / total if total > 0 else 0
    recall = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    f1 = 2 * (precisao * recall) / (precisao + recall) if (precisao + recall) > 0 else 0
    
    return precisao, recall, f1

def get_metric_explanation(metric_name, value):
    """
    Retorna uma explicação detalhada para uma métrica específica.
    
    Parâmetros:
    - metric_name: Nome da métrica
    - value: Valor calculado
    
    Retorna:
    - Explicação em texto da interpretação do valor
    """
    explanations = {
        "gini": {
            "title": "Índice de Gini",
            "description": "Mede a pureza da classificação",
            "interpretation": lambda v: "Boa separação entre classes" if v < 0.3 else 
                            "Separação moderada" if v < 0.6 else 
                            "Alta mistura entre classes"
        },
        "entropy": {
            "title": "Entropia",
            "description": "Mede a incerteza da decisão",
            "interpretation": lambda v: "Alta certeza na decisão" if v < 1 else 
                            "Certeza moderada" if v < 2 else 
                            "Alta incerteza na decisão"
        },
        "depth": {
            "title": "Profundidade Decisória",
            "description": "Complexidade do processo de decisão",
            "interpretation": lambda v: "Processo simples" if v < 3 else 
                            "Complexidade moderada" if v < 5 else 
                            "Processo complexo"
        }
    }
    
    if metric_name in explanations:
        metric = explanations[metric_name]
        return {
            "title": metric["title"],
            "description": metric["description"],
            "value": value,
            "interpretation": metric["interpretation"](value)
        }
    return None
