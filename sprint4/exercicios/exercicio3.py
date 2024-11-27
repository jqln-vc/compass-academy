"""
Exercício 3: função calcula_saldo.

Args:
    lancamentos (list(tuple)): cada tupla é (valor, tipo).
        - valor (float): sempre positivo
        - tipo (str): C - crédito ou D - débito.
Returns:
    valor_final (float): soma de créditos, subtração de débitos.
"""


def calcula_saldo(lancamentos: list[tuple[float, str]]) -> float:
    """Calcula o saldo final de uma série de transações.

    Args:
        list(tuple(float, str)): lista de tuplas com valor e tipo.
            tupla: (valor(float), tipo(str))
            tipos: 'C' - crédito
                   'D' - débito

    Returns:
        valor_final (float): saldo final, considerando a soma de
        créditos e subtração de débitos.
    """
    from functools import reduce

    historico = map(
        lambda valor: -valor[0]
        if valor[1] == 'D'
        else valor[0],
        lancamentos
        )

    valor_final = float(reduce(
        lambda a, b: a + b,
        historico
        ))

    return valor_final
