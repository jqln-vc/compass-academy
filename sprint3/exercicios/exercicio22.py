"""
Exercício 22: criação da classe Pessoa.

Implementação de atributos público:id e privado:nome,
métodos getter e setter.
"""


class Pessoa(object):
    """Classe Pessoa, possui nome e id."""

    def __init__(self, id, nome="Desconhecido"):
        """Construtor de Pessoa."""
        self.id = id
        self.__nome = nome

    @property
    def nome(self):
        """Getter do atributo privado nome."""
        return self.__nome

    @nome.setter
    def nome(self, nome):
        """Setter do atributo privado nome."""
        self.__nome = nome


pessoa = Pessoa(0)
pessoa.nome = "Fulano De Tal"
print(pessoa.nome)
