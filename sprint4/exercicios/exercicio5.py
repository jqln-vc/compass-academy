"""
Exercício 5: cálculo de média de estudantes por arquivo csv.

Script que trata dados de arquivo csv,
seleciona as 3 maiores notas de cada aluno,
e calcula a média dessas 3 notas, retornada em 2 casas decimais.

-> Nome: <nome estudante> Notas: [n1, n2, n3] Média: <média>
"""

with open('estudantes.csv', 'r') as csv:

    # Extrai dos dados do csv, e ordena os alunos em ordem alfabética
    alunos = sorted([linha.strip().split(',')
                    for linha in csv.readlines()],
                    key=lambda aluno: aluno[0])

    # Extrai e converte as notas de cada aluno, ordena decrescentemente
    notas = list(map(
        lambda notas: sorted(
                            [int(nota)
                                for nota in notas
                                if nota.isnumeric()],
                            reverse=True),
        alunos))

    # Calcula a média das 3 maiores notas, e arrendonda com 2 casas
    medias = list(map(
        lambda notas: round(sum(notas[:3])/3, 2),
        notas))

    # Imprime valores respectivos das 3 listas
    for aluno, notas, medias in zip(alunos, notas, medias):
        print(f"Nome: {aluno[0]} Notas: {notas[0:3]} Média: {medias}")
