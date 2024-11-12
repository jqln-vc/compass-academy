"""
Exercício 9: impressão de valor e índice respectivo de uma lista.

Implementação utilizando a função zip para integrar as listas,
e enumerate para iterá-las obtendo o índice atual.

list nomes: lista de primeiros nomes (string)
list sobrenomes: lista de sobrenomes (string)
list idades: lista de idades (int)

-> print: "{índice} - {nome} {sobrenome} está com {idade} anos"
"""

nomes = ['Joao', 'Douglas', 'Lucas', 'José']
sobrenomes = ['Soares', 'Souza', 'Silveira', 'Pedreira']
idades = [19, 28, 25, 31]

for index, (n, s, i) in enumerate(zip(nomes, sobrenomes, idades)):
    print(f"{index} - {n} {s} está com {i} anos")
