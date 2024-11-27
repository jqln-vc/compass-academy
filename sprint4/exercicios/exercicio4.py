"""
Exercício 4: função calcular_valor_maximo.

Args:
    operadores (string): lista com operadores + - * / + %
    operandos (list(tuple(int))): lista de tuplas com 2 valores.

Returns:
    int: maior valor após operações mapeando ambos argumentos.
"""


def calcular_valor_maximo(
        operadores: list[str],
        operandos: list[tuple[int]]
        ) -> float:
    """Função de mapeamento de operações.

    Args:
        operadores (string): lista com operadores + - * / + %
        operandos (list(tuple(int))): lista de tuplas com 2 valores.

    Returns:
        int: maior valor após operações mapeando ambos argumentos.

    """
    ops_dict = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '//': lambda a, b: a // b,
        '/': lambda a, b: a / b,
        '%': lambda a, b: a % b
    }

    operacoes = zip(operadores, operandos)

    resultados = list(map(
        lambda num: ops_dict[num[0]](*num[1]),
        operacoes
        ))

    return max(resultados)
