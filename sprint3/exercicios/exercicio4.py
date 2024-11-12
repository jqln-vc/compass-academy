"""
Exercício 4: impressão de números primos de 1 a 100.

Validação a partir da função primo, sendo um número primo
aquele que possui apenas 2 divisores positivos e distintos, 1 e ele mesmo.

list primos: recebe primos de 1 a 100 retornados com a função range()

-> print: primos de 1 a 100.
"""


def primo(numero: int) -> bool:
    """Verifica a primalidade de um número.

    Args:
        num (int): número verificado

    Returns:
        bool: True se primo.
    """
    if numero <= 1:  # 1 e negativos não são primos
        return False
    # verifica, até a raiz quadrada do número, se existe algum divisor
    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            return False
    return True


primos = [num for num in range(1, 101) if primo(num)]

[print(num) for num in primos]
