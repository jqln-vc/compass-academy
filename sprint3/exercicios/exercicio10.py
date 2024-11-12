"""
Exercício 10: remoção de valores duplicados de uma lista.

Implementação a partir de função remocao_duplicacao.

list lista: lista a ser tratada

-> list nova_lista: lista sem valores duplicados.
"""


def remocao_duplicacao(lista: list) -> list:
    """Remoção de valores duplicados de uma lista.

    Args:
        lista (list): lista com valores a serem tratados.

    Returns:
        list: nova lista sem valores duplicados.
    """
    return list(set(lista))


lista = ['abc', 'abc', 'abc', '123', 'abc', '123', '123']

print(remocao_duplicacao(lista))
