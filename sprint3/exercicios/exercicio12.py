"""
Exercício 12: implentação de função my_map.

A função recebe uma lista e aplica uma função em cada elemento.

-> list: nova lista com a função aplicada.
"""


def my_map(lista: list, funcao: callable) -> list:
    """Mapeia uma função a cada elemento da lista.

    Args:
        lista (lista): lista a ser tratada com a função.
        funcao (callable): função a ser aplicada na lista.

    Returns:
        list: nova lista após aplicação de funcao.
    """
    return [funcao(num) for num in lista]


lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(my_map(lista, lambda x: x**2))
