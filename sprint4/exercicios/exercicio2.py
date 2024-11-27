"""
Exercício 2: função conta_vogais.

Utilizar high order functions.

Args:
    string: arquivo de leitura.
Returns:
    int: total de vogais da string.
"""


def conta_vogais(texto: str) -> int:
    """Filtra vogais de uma string e retorna total.

    Args:
        texto(string): string de caracteres.

    Returns:
        int: total de vogais em texto.
    """
    vogais_dict = [
        'a', 'e', 'i', 'o', 'u',
        'á', 'à', 'â', 'ã',
        'é', 'è', 'ê',
        'í', 'ì', 'î',
        'ó', 'ò', 'ô', 'õ',
        'ú', 'ù', 'û']

    vogais = list(filter(lambda vogal: vogal.lower() in vogais_dict, texto))

    return len(vogais)
