"""
Exercício 16: implementação de função que soma valores em uma string.

str valores: string de valores separados por vírgula.

-> int total: soma de valores da string.
"""


def soma_string(valores: str) -> int:
    """Soma de valores numéricos em uma string.

    Args:
        valores (string): string com valores numéricos separados por vírgula.

    Returns:
        int: soma dos valores da string.
    """
    valores = [int(num) for num in valores.split(",")]
    return sum(valores)


lista_valores = "1,3,4,6,10,76"
print(soma_string(lista_valores))
