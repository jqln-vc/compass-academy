"""
Exercício 3: impressão de números pares de 0 a 20.

list pares: recebe pares de 0 a 20 retornados com a função range()

-> print: pares.
"""

pares = [par for par in range(0, 21, 2)]

[print(par) for par in pares]
