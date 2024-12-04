"""
Exercício 7: função de generator de números pares.

Args:
    n (int): valor máximo para o generator.

Returns:
    gerador (callable): generator de valores no intervalo [2, n].
"""


def pares_ate(n: int) -> callable:
    """Função generator de números pares.

    Args:
        n (int): valor máximo para o generator.

    Returns:
        gerador (function): generator de valores no intervalo [2, n].
    """
    return (par for par in range(2, n+1) if par % 2 == 0)
