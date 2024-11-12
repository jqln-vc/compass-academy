"""
Exercício 1: aniversário de 100 anos.

str nome : recebe o nome da pessoa
int idade : recebe a idade da pessoa
int ano_atual : recebe o ano ano_atual
int aniversario_cem_anos : recebe o ano de aniversário de 100 anos

-> print: ano de aniversário de 100 anos.
"""

from datetime import datetime

ano_atual = datetime.now().year
nome = "Zola"
idade = 12

aniversario_cem_anos = ano_atual + (100 - idade)

print(f"{aniversario_cem_anos}")
