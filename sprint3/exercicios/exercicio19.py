"""
Exercício 19: cálculo da mediana, média, mínimo e máximo de uma lista.

list random_list: lista com valores aleatórios.

-> mediana, media, valor_minimo, valor_maximo
"""

import random

random_list = random.sample(range(500), 50)
tam = len(random_list)
random_list.sort()

if (tam % 2 == 0):
    mediana = (random_list[tam//2-1] + random_list[tam//2]) / 2
else:
    mediana = random_list[tam//2]

media = sum(random_list) / tam
valor_minimo = min(random_list)
valor_maximo = max(random_list)

print(f"Media: {media}, Mediana: {mediana}, \
        Mínimo: {valor_minimo}, Máximo: {valor_maximo}")
