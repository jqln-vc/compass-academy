"""
Exercício 21: implementação de classes filhas a partir de classe mãe.

class Pato: herda e sobrescreve método emitir_som.
class Pardal: herda e sobrescreve método emitir_som.
class Passaro: métodos voar, emitir_som.
"""


class Passaro(object):
    """Implementação da classe mãe Pássaro."""

    def __init__(self, especie="Pássaro"):
        """Método construtor."""
        self.especie = especie

    def voar(self):
        """Método para voar."""
        print("Voando...")

    def emitir_som(self):
        """Método de canto específico da espécie."""
        pass


class Pato(Passaro):
    """Classe Pato herdeira da classe Pássaro."""

    def __init__(self, especie="Pato"):
        """Método construtor."""
        self.especie = especie

    def emitir_som(self):
        """Método de canto específico da espécie."""
        print(f"{self.especie} emitindo som...\nQuack Quack")


class Pardal(Passaro):
    """Classe Pardal herdeira da classe Pássaro."""

    def __init__(self, especie="Pardal"):
        """Método construtor."""
        self.especie = especie

    def emitir_som(self):
        """Método de canto específico da espécie."""
        print(f"{self.especie} emitindo som...\nPiu Piu")


pato = Pato()
pardal = Pardal()

print(pato.especie)
pato.voar()
pato.emitir_som()
print(pardal.especie)
pardal.voar()
pardal.emitir_som()
