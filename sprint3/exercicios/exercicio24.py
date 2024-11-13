"""
Exercício 24: criação de classe Ordenadora.

Atributos:
    listaBaguncada

Métodos:
    ordenacaoCrescente
    ordenacaoDescrescente
"""

# Os nomes solicitados para o atributo e os métodos não aderem ao PEP-8.


class Ordenadora(object):
    """Classe Ordenadora para organização de listas."""

    def __init__(self, lista: list):
        """Método construtor, recebe lista."""
        self.listaBaguncada = lista

    def ordenacaoCrescente(self):
        """Método de ordenação crescente da lista bagunçada."""
        self.listaBaguncada.sort()
        return self.listaBaguncada

    def ordenacaoDecrescente(self):
        """Método de ordenação decrescente da lista bagunçada."""
        self.listaBaguncada.sort()
        return self.listaBaguncada[::-1]


crescente = Ordenadora([3, 4, 2, 1, 5])
decrescente = Ordenadora([9, 7, 6, 8])
print(crescente.ordenacaoCrescente())
print(decrescente.ordenacaoDecrescente())
