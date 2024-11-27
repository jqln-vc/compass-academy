"""
Exercício 1: utilizando lambda e high order funcions.

Leitura de arquivo com 10000 números inteiros, um em cada linha.
Utilizar map, filter, sorted e sum.

-> lista dos 5 maiores números pares em ordem decrescente;
-> a soma destes valores.
"""

with open('number.txt', 'r') as arquivo:
    numeros = map(
        lambda num: int(num.strip()),
        arquivo.readlines()
        )
    pares = sorted(list(filter(
                lambda num: num % 2 == 0,
                numeros
                )),
                reverse=True)
    top5 = pares[:5]

    print(f"{top5}\n{sum(top5)}")
