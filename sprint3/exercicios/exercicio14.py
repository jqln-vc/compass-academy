"""
Exercício 14: impressão de parâmetros não nomeados e parâmetros nomeados.

Implementação de função parametros, que recebe um número variável de
parâmetros nomeados e não nomeados e imprime seus valores.

-> print: valores dos parâmetros da função.
"""


def parametros(*args, **kwargs) -> None:
    """Impressão de valores de parâmetros variáveis.

    Args:
        args: parâmetros não nomeados.
        kwargs: parâmetros nomeados.

    Returns:
        None: imprime os valores dos parâmetros passados.
    """
    for param in args:
        print(param)
    for param in kwargs.values():
        print(param)


parametros(1, 3, 4, 'hello', parametro_nomeado='alguma coisa', x=20)
