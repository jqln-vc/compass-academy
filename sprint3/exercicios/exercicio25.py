"""
Exercício 25: criação de classe Avião.

Atributos:
    modelo (string)
    velocidade_maxima (float)
    cor (string): Azul
    capacidade (int)
"""


class Aviao(object):
    """Classe para Avião, todas as instâncias herdam cor."""

    def __init__(self, mod: str, v_max: float, cap: int):
        """Construtor com atributo estático cor."""
        self.modelo = mod
        self.velocidade_maxima = v_max
        self.capacidade = cap
        self.__cor = "Azul"

    @property
    def cor(self):
        """Getter do atributo cor."""
        return self.__cor


aviao1 = Aviao("BOIENG456", 1500, 400)
aviao2 = Aviao("Embraer Praetor 600", 863, 14)
aviao3 = Aviao("Antonov An-2", 258, 12)
avioes = [aviao1, aviao2, aviao3]

for aviao in avioes:
    print(f"""O avião de modelo {aviao.modelo} possui
    uma velocidade máxima de {aviao.velocidade_maxima} Km/h,
    capacidade para {aviao.capacidade} passageiros
    e é da cor {aviao.cor}""")
