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
    try:
        total = sum(classes.values())
        if total == 0:
            return 0.0
        gini = 1.0 - sum((float(count) / float(total)) ** 2 for count in classes.values())
        return float(gini)
    except Exception as e:
        print(f"Erro ao calcular índice Gini: {str(e)}")
        return 0.0

def calcular_entropia(classes):
    """
    Calcula a entropia de Shannon para um conjunto de classes.
    A entropia mede a aleatoriedade ou imprevisibilidade em um conjunto de dados.
    
    Fórmula: Entropia = -Σ(pi * log2(pi)), onde pi é a proporção de cada classe
    Interpretação:
    - Valor baixo: Indica maior certeza na decisão
    - Valor alto: Indica maior incerteza na decisão
    """
    try:
        total = sum(classes.values())
        if total == 0:
            return 0.0
        entropia = -sum((float(count) / float(total)) * math.log2(float(count) / float(total)) 
                       for count in classes.values() if count != 0)
        return float(entropia)
    except Exception as e:
        print(f"Erro ao calcular entropia: {str(e)}")
        return 0.0

def calcular_profundidade_decisoria(decisoes):
    """
    Calcula a profundidade média da árvore de decisão.
    Uma profundidade menor indica um modelo mais simples e interpretável.
    
    Fórmula: Profundidade Média = Σ(profundidades) / número de decisões
    Interpretação:
    - Valor baixo: Indica processo decisório mais direto
    - Valor alto: Indica processo decisório mais complexo
    """
    try:
        if not decisoes:
            return 0.0
        profundidade_total = float(sum(decisoes))
        return profundidade_total / float(len(decisoes))
    except Exception as e:
        print(f"Erro ao calcular profundidade decisória: {str(e)}")
        return 0.0

def calcular_pruning(total_nos, nos_podados):
    """
    Calcula o pruning ratio (proporção de nós podados).
    Indica a eficácia da simplificação do modelo.
    
    Fórmula: Pruning Ratio = (total_nós - nós_podados) / total_nós
    Interpretação:
    - Valor próximo a 0: Pouca simplificação
    - Valor próximo a 1: Alta simplificação
    """
    try:
        if total_nos == 0:
            return 0.0
        pruning_ratio = float(total_nos - nos_podados) / float(total_nos)
        return pruning_ratio
    except Exception as e:
        print(f"Erro ao calcular taxa de poda: {str(e)}")
        return 0.0

def calcular_confiabilidade_recomendacao(scores, threshold=0.7):
    """
    Calcula a confiabilidade da recomendação baseada nos scores.
    
    Fórmula: Confiabilidade = (max_score - mean_score) / max_score
    Interpretação:
    - Valor > threshold: Alta confiabilidade
    - Valor ≤ threshold: Média confiabilidade
    """
    try:
        if not scores:
            return 0.0
        scores = [float(s) for s in scores]  # Ensure all scores are float
        max_score = max(scores)
        if max_score == 0:
            return 0.0
        mean_score = sum(scores) / len(scores)
        confiabilidade = (max_score - mean_score) / max_score
        return float(confiabilidade)
    except Exception as e:
        print(f"Erro ao calcular confiabilidade: {str(e)}")
        return 0.0

def get_metric_interpretation(metric_name, value):
    """
    Retorna uma explicação detalhada para uma métrica específica.
    
    Parâmetros:
    - metric_name: Nome da métrica
    - value: Valor calculado
    
    Retorna:
    - Explicação em texto da interpretação do valor
    """
    try:
        value = float(value)  # Ensure value is float
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
            },
            "pruning": {
                "title": "Taxa de Poda",
                "description": "Eficácia da simplificação do modelo",
                "interpretation": lambda v: "Alta simplificação" if v > 0.7 else 
                                "Simplificação moderada" if v > 0.4 else 
                                "Baixa simplificação"
            },
            "confidence": {
                "title": "Confiabilidade",
                "description": "Nível de confiança na recomendação",
                "interpretation": lambda v: "Alta confiabilidade" if v > 0.7 else 
                                "Confiabilidade moderada" if v > 0.4 else 
                                "Baixa confiabilidade"
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
    except Exception as e:
        print(f"Erro ao interpretar métrica: {str(e)}")
        return None
