"""
Actors ETL Pipeline: Script para processamento de dados do arquivo 'actors.csv'.
Autoria: Jaqueline Costa
Data: Nov / 2024
"""

# Etapa 1: Apresentar o ator/atriz com maior número de filmes e a respectiva quantidade. 
# A quantidade de filmes encontra-se na coluna 'Number of Movies'.

# Etapa 2: Apresentar a média de receita (coluna 'Gross') de bilheteria bruta dos 
# principais filmes, considerando todos os atores.

# Etapa 3: Apresentar o ator/atriz com a maior média de receita de bilheteria bruta 
# por filme do conjunto de dados. Considerar a coluna 'Average per Movie'.

# Etapa 4: A coluna '#1 Movie' contém o filme de maior bilheteria em que o ator atuou. 
# Realizar a contagem de aparições destes filmes no dataset, listando-os ordenados 
# pela quantidade de vezes em que estão presentes. 
# Considerar a ordem decrescente e, em segundo nível, o nome do filme. 
#
# Ao escrever no arquivo, considerar o padrão de saída 
# '(sequencia) - O filme (nome) aparece (quantidade) vez(es) no dataset', 
# adicionando um resultado por linha.

# Etapa 5: Apresentar a lista dos atores ordenada pela receita bruta de bilheteria 
# de seus filmes (coluna 'Total Gross'), em ordem decrescente. 
#
# Ao escrever no arquivo,  considerar o padrão de saída
# '(nome do ator) - (receita total bruta)', adicionando um resultado por linha.
