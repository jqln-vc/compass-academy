"""
Exercício 18: lista de valores distintos de um dicionário.

Implementação da função valores_nao_dup.

dict speed: dicionário com valores duplicados.
-> list: valores distintos do dicionário.
"""


def valores_nao_dup(dicio: dict) -> list:
    """Lista de valores distintos de um dicionário.

    Args:
        dicio (dict): dicionário com valores duplicados.

    Returns:
        list: lista com valores distintos.
    """
    return list(set([valor for valor in dicio.values()]))


speed = {
    'jan': 47,
    'feb': 52,
    'march': 47,
    'April': 44,
    'May': 52,
    'June': 53,
    'july': 54,
    'Aug': 44,
    'Sept': 54
}
print(valores_nao_dup(speed))
