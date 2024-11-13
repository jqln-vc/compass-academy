"""
Exercício 23: criação de classe Cálculo, com métodos de adição e subtração.

métodos:
    adição
    subtração
"""


class Calculo(object):
    """Classe Cálculo que soma e subtrai 2 valores."""

    def soma(self, x, y):
        """Método de soma de 2 valores."""
        return x + y

    def subtracao(self, x, y):
        """Método de subtração de 2 valores."""
        return x - y


x, y = 4, 5
calculadora = Calculo()
print(f"Somando: {x}+{y} = {calculadora.soma(x, y)}")
print(f"Subtraindo: {x}-{y} = {calculadora.subtracao(x, y)}")
