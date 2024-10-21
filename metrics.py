import math

def calcular_gini(classes):
    """Calcula a impureza de Gini."""
    total = sum(classes.values())
    gini = 1 - sum((count / total) ** 2 for count in classes.values())
    return gini

def calcular_entropia(classes):
    """Calcula a entropia."""
    total = sum(classes.values())
    entropia = -sum((count / total) * math.log2(count / total) for count in classes.values() if count != 0)
    return entropia

def calcular_profundidade_decisoria(decisoes):
    """Calcula a profundidade média da árvore de decisão."""
    if not decisoes:
        return 0
    profundidade_total = sum(decisoes)
    return profundidade_total / len(decisoes)

def calcular_pruning(total_nos, nos_podados):
    """Calcula o pruning ratio (proporção de nós podados)."""
    if total_nos == 0:
        return 0
    pruning_ratio = (total_nos - nos_podados) / total_nos
    return pruning_ratio
