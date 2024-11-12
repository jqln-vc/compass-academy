"""
Exercício 6: imprimir interseção de duas listas.

Implementação feita com a utilização de sets.

list lista1
list lista2

-> print: list interseção.

"""

a = [1, 1, 2, 3, 5, 8, 14, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

intersecao = list(set(a).intersection(set(b)))

print(intersecao)
