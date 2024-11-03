import math
import numpy as np
import plotly.graph_objects as go

def calcular_gini(classes):
    """
    Calcula a impureza de Gini para um conjunto de classes.
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
    """
    if not decisoes:
        return 0
    profundidade_total = sum(decisoes)
    return profundidade_total / len(decisoes)

def calcular_pruning(total_nos, nos_podados):
    """
    Calcula o pruning ratio e métricas relacionadas.
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

def calcular_peso_caracteristica(caracteristica, pesos_base, respostas):
    """
    Calcula o peso ajustado de uma característica específica com base nas respostas.
    
    Args:
        caracteristica: Nome da característica
        pesos_base: Dicionário com os pesos base das características
        respostas: Dicionário com as respostas do usuário
    
    Returns:
        Dict com peso_ajustado, impacto_respostas e confianca
    """
    if not pesos_base or caracteristica not in pesos_base:
        return {
            'peso_ajustado': 0,
            'impacto_respostas': 0,
            'confianca': 0
        }
    
    # Peso base normalizado
    total_pesos = sum(pesos_base.values())
    peso_base = pesos_base[caracteristica] / total_pesos if total_pesos > 0 else 0
    
    # Mapeamento de características para perguntas relacionadas
    relacionadas = {
        'security': ['privacy', 'network_security'],
        'scalability': ['data_volume', 'integration'],
        'energy_efficiency': ['energy_efficiency'],
        'governance': ['governance_flexibility', 'interoperability']
    }
    
    # Calcula o impacto das respostas relacionadas
    respostas_relacionadas = [
        resp for q_id, resp in respostas.items()
        if q_id in relacionadas.get(caracteristica, [])
    ]
    
    num_respostas_positivas = sum(1 for resp in respostas_relacionadas if resp == "Sim")
    total_perguntas_relacionadas = len(relacionadas.get(caracteristica, []))
    
    impacto_respostas = num_respostas_positivas / total_perguntas_relacionadas if total_perguntas_relacionadas > 0 else 0
    
    # Ajusta o peso baseado no impacto das respostas
    peso_ajustado = peso_base * (1 + impacto_respostas * 0.5)
    
    # Calcula o nível de confiança baseado na quantidade de respostas relacionadas
    confianca = len(respostas_relacionadas) / total_perguntas_relacionadas if total_perguntas_relacionadas > 0 else 0
    
    return {
        'peso_ajustado': peso_ajustado,
        'impacto_respostas': impacto_respostas,
        'confianca': confianca
    }

def create_metrics_radar_chart(metrics_data):
    """
    Creates a radar chart for visualizing metrics.
    """
    fig = go.Figure()
    
    categories = list(metrics_data.keys())
    values = list(metrics_data.values())
    
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # Add first value at end to close the polygon
        theta=categories + [categories[0]],  # Add first category at end to close the polygon
        fill='toself',
        name='Métricas Atuais'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        title="Visão Geral das Métricas"
    )
    return fig

def create_characteristic_weights_chart(weights_data):
    """
    Creates a radar chart for visualizing characteristic weights.
    """
    fig = go.Figure()
    
    categories = list(weights_data.keys())
    values = [weights_data[cat]['peso_ajustado'] for cat in categories]
    
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # Add first value at end to close the polygon
        theta=categories + [categories[0]],  # Add first category at end to close the polygon
        fill='toself',
        name='Pesos das Características'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        title="Distribuição dos Pesos das Características"
    )
    return fig

def get_metric_explanation(metric_name, value):
    """
    Returns a detailed explanation for a specific metric.
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
