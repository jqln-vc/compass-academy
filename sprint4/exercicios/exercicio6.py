"""
Exercício 6: feature idenficação de produtos com preço acima da média.

Calcula a média dos preços de produtos do catálogo,
e retorna produtos com preço acima.

Args:
    conteudo (dict): catálogo de produtos.

Returns:
    caros (list): lista de tuplas com produto e preço.
"""


def maiores_que_media(conteudo: dict[str, float]) -> list[tuple[str, float]]:
    """Função que identifica produtos com preço acima da média.

    Args:
        conteudo (dict): produtos e preços.

    Returns:
        caros (list(tuple(str, float))):
            Lista de tuplas (produto, preço), para produtos com
            preço acima da média.
    """
    media = sum(conteudo.values()) / len(conteudo)

    caros = sorted(list(filter(
        lambda item: item[1] > media,
        conteudo.items())),
        key=lambda valor: valor[1])

    return caros
