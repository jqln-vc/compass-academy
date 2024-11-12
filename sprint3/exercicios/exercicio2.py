"""
Exercício 2: criação de lista de números e validação de pares e ímpares.

list numeros: recebe 3 números da função range()

-> print: Par: valor da lista | Ímpar: valor da lista.
"""

num_min, num_max, step = 3, 12, 3

numeros = [num for num in range(num_min, num_max, step)]

for num in numeros:
    # valor_True if condição else valor_False
    print(f"Par: {num}") if (num % 2 == 0) else print(f"Ímpar: {num}")
