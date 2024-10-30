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
    profundidade_total = sum(decisoes)
    return profundidade_total / len(decisoes)

def calcular_pruning(total_nos, nos_podados):
    """
    Calcula o pruning ratio (proporção de nós podados) e métricas relacionadas.
    
    Retorna:
    - pruning_ratio: Proporção de nós removidos
    - eficiencia_poda: Medida da eficiência da poda
    - impacto_complexidade: Impacto na complexidade do modelo
    """
    if total_nos == 0:
        return {
            'pruning_ratio': 0,
            'eficiencia_poda': 0,
            'impacto_complexidade': 0
        }
    
    pruning_ratio = (total_nos - nos_podados) / total_nos
    eficiencia_poda = 1 - (nos_podados / total_nos)
    impacto_complexidade = math.log2(total_nos / (total_nos - nos_podados + 1))
    
    return {
        'pruning_ratio': pruning_ratio,
        'eficiencia_poda': eficiencia_poda,
        'impacto_complexidade': impacto_complexidade
    }

def calcular_peso_caracteristica(caracteristica, pesos, respostas):
    """
    Calcula o peso normalizado e ajustado de uma característica específica.
    
    Parâmetros:
    - caracteristica: Nome da característica
    - pesos: Dicionário com os pesos base das características
    - respostas: Dicionário com as respostas do usuário
    
    Retorna:
    - peso_ajustado: Peso final após ajustes baseados nas respostas
    - impacto_respostas: Fator de impacto das respostas
    - confianca: Nível de confiança no peso calculado
    """
    if not pesos or caracteristica not in pesos:
        return {
            'peso_ajustado': 0,
            'impacto_respostas': 0,
            'confianca': 0
        }
    
    # Peso base normalizado
    total_pesos = sum(pesos.values())
    peso_base = pesos[caracteristica] / total_pesos if total_pesos > 0 else 0
    
    # Ajuste baseado nas respostas relacionadas
    relacionadas = {
        'security': ['privacy', 'network_security'],
        'scalability': ['data_volume', 'integration'],
        'energy_efficiency': ['energy_efficiency'],
        'governance': ['governance_flexibility', 'interoperability']
    }
    
    # Calcula o impacto das respostas
    respostas_relacionadas = [
        resp for q_id, resp in respostas.items()
        if q_id in relacionadas.get(caracteristica, [])
    ]
    
    impacto_respostas = sum(1 for resp in respostas_relacionadas if resp == "Sim") / \
                        len(relacionadas.get(caracteristica, [])) if relacionadas.get(caracteristica) else 0
    
    # Ajusta o peso baseado no impacto das respostas
    peso_ajustado = peso_base * (1 + impacto_respostas * 0.5)
    
    # Calcula o nível de confiança baseado na quantidade de respostas relacionadas
    confianca = len(respostas_relacionadas) / len(relacionadas.get(caracteristica, [1])) \
                if relacionadas.get(caracteristica) else 0
    
    return {
        'peso_ajustado': peso_ajustado,
        'impacto_respostas': impacto_respostas,
        'confianca': confianca
    }

def get_metric_explanation(metric_name, value):
    """
    Retorna uma explicação detalhada para uma métrica específica.
    """
    explanations = {
        "gini": {
            "title": "Índice de Gini",
            "description": "Mede a pureza da classificação",
            "formula": "Gini = 1 - Σ(pi²)",
            "interpretation": lambda v: "Boa separação entre classes" if v < 0.3 else 
                            "Separação moderada" if v < 0.6 else 
                            "Alta mistura entre classes"
        },
        "entropy": {
            "title": "Entropia",
            "description": "Mede a incerteza da decisão",
            "formula": "Entropia = -Σ(pi * log2(pi))",
            "interpretation": lambda v: "Alta certeza na decisão" if v < 1 else 
                            "Certeza moderada" if v < 2 else 
                            "Alta incerteza na decisão"
        },
        "pruning": {
            "title": "Métricas de Poda",
            "description": "Avalia a eficiência da simplificação do modelo",
            "formula": "Pruning Ratio = (total_nós - nós_podados) / total_nós",
            "interpretation": lambda v: "Poda eficiente" if v['pruning_ratio'] > 0.7 else 
                            "Poda moderada" if v['pruning_ratio'] > 0.4 else 
                            "Poda limitada"
        },
        "characteristic_weight": {
            "title": "Peso da Característica",
            "description": "Avalia a importância relativa da característica",
            "formula": "Peso Ajustado = peso_base * (1 + impacto_respostas * 0.5)",
            "interpretation": lambda v: "Alta importância" if v['peso_ajustado'] > 0.3 else 
                            "Importância moderada" if v['peso_ajustado'] > 0.15 else 
                            "Baixa importância"
        }
    }
    
    if metric_name in explanations:
        metric = explanations[metric_name]
        return {
            "title": metric["title"],
            "description": metric["description"],
            "formula": metric.get("formula", ""),
            "value": value,
            "interpretation": metric["interpretation"](value)
        }
    return None
