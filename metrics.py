import math
import numpy as np

def calcular_gini(classes):
    """
    Calcula a impureza de Gini para um conjunto de classes.
    A impureza de Gini é uma medida de quão frequentemente um elemento seria 
    incorretamente classificado se fosse classificado aleatoriamente.
    
    Fórmula: Gini = 1 - Σ(pi²), onde pi é a proporção de cada classe
    """
    total = sum(classes.values())
    gini = 1 - sum((count / total) ** 2 for count in classes.values())
    return gini

def calcular_entropia(classes):
    """
    Calcula a entropia de Shannon para um conjunto de classes.
    A entropia mede a aleatoriedade ou imprevisibilidade em um conjunto de dados.
    
    Fórmula: Entropia = -Σ(pi * log2(pi)), onde pi é a proporção de cada classe
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
    """
    if not decisoes:
        return 0
    profundidade_total = sum(decisoes)
    return profundidade_total / len(decisoes)

def calcular_pruning(total_nos, nos_podados):
    """
    Calcula o pruning ratio (proporção de nós podados).
    Indica a eficácia da simplificação do modelo.
    
    Fórmula: Pruning Ratio = (total_nós - nós_podados) / total_nós
    """
    if total_nos == 0:
        return 0
    pruning_ratio = (total_nos - nos_podados) / total_nos
    return pruning_ratio

def calcular_peso_caracteristica(caracteristica, pesos):
    """
    Calcula o peso normalizado de uma característica específica.
    
    Fórmula: Peso Normalizado = peso_característica / Σ(todos os pesos)
    """
    total_pesos = sum(pesos.values())
    return pesos.get(caracteristica, 0) / total_pesos if total_pesos > 0 else 0

def calcular_jaccard_similarity(conjunto_a, conjunto_b):
    """
    Calcula o índice de similaridade de Jaccard entre dois conjuntos.
    
    Fórmula: J(A,B) = |A ∩ B| / |A ∪ B|
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
