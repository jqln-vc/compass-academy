"""
Exercício 17: função que divide uma lista em 3 de tamanho igual.

list lista: lista de tamanho divisível por 3.

-> list lista1, lista2, lista3: sublistas de tamanho igual.
"""


def tres_listas(lista: list) -> tuple:
    """Separa a lista em 3 listas de tamanho igual.

    Args:
        lista (list): lista com tamanho divisível por 3.

    Returns:
        lista1, lista2, lista3 (list): partes da lista original.
    """
    if (len(lista) % 3 == 0):
        tam = len(lista) // 3
        lista1 = lista[0:tam]
        lista2 = lista[tam:tam*2]
        lista3 = lista[tam*2:]
    else:
        print("A lista não é divisível por 3.")

    return lista1, lista2, lista3


lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

lista1, lista2, lista3 = tres_listas(lista)
print(lista1, lista2, lista3)
