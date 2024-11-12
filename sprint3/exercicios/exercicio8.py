"""
Exercício 8: verificação de palíndromo.

Utilização da função palíndromo que recebe uma string
e verifica se é igual ao seu reverso.

list lista: lista de palavras.

-> print: A palavra: lista[i] é/não é um palíndromo.
"""


def palindromo(palavra: str) -> bool:
    """Função para verificação de palíndromos.

    Args:
        palavra (str): palavra a ser verificada.

    Returns:
        bool: True se palíndromo.
    """
    if (palavra == palavra[::-1]):
        return True
    else:
        return False


lista = ['maça', 'arara', 'audio', 'radio', 'radar', 'moto']

for palavra in lista:
    if palindromo(palavra):
        print(f"A palavra: {palavra} é um palíndromo")
    else:
        print(f"A palavra: {palavra} não é um palíndromo")
