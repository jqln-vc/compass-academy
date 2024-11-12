"""
Exercício 15: implementação da classe Lampada.

Inclusão de métodos para ligar/desligar a luz.
"""


class Lampada:
    """Classe Lâmpada, possui função de ligar e desligar.

    Métodos:
        liga(): liga a lâmpada.
        desliga(): desliga a lâmpada.
        esta_ligada: retorna True se lâmpada estiver ligada.
    """

    def __init__(self, ligada=False):
        """Construtor de lâmpada, instanciada desligada."""
        self.ligada = ligada

    def esta_ligada(self):
        """Retorna True se estiver ligada."""
        if self.ligada:
            return True
        else:
            return False

    def liga(self):
        """Método para ligar a lâmpada."""
        self.ligada = True

    def desliga(self):
        """Método para desligar a lâmpada."""
        self.ligada = False


lampada = Lampada()
lampada.liga()
print(f"A lâmpada está ligada? {lampada.esta_ligada}")
lampada.desliga()
print(f"A lâmpada ainda está ligada? {lampada.esta_ligada}")
