"""
Exercício 11: leitura, parsing e impressão de arquivo json.

Implementação de função leitura_json, retorna um dicionário
com o conteúdo do arquivo passado como parâmetro.
"""


def leitura_json(arq_json: str) -> dict:
    """Leitura e parsing de arquivo em formato json.

    Args:
        arq_json (str): caminho do arquivo json.

    Returns:
        dados (dict): dicionário com conteúdo do arquivo json.
    """
    import json

    with open(arq_json, "r") as arquivo:
        dados = json.load(arquivo)
    return dados


print(leitura_json("person.json"))
