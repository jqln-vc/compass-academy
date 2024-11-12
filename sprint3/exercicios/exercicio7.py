"""
Exercício 7: a partir de uma lista, gerar outra com números ímpares.

list a: lista com números

-> list impares: lista de números ímpares gerada a partir de "a".
"""

a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

impares = [num for num in a if (num % 2 != 0)]

print(impares)
