"""
Exercício 13: leitura e impressão de arquivo de texto.

Implementação de função leitura_texto.

-> str texto: conteúdo do arquivo de texto.
"""


def leitura_texto(arq_texto: str) -> str:
    """Leitura de arquivo de texto.

    Args:
        arq_texto (str): caminho do arquivo de texto.

    Returns:
        str: conteúdo do arquivo de texto.
    """
    with open(arq_texto, "r") as arquivo:
        texto = arquivo.read()

    return texto


print(leitura_texto("arquivo_texto.txt"), end="")
