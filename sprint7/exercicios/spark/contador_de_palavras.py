"""
Sprint 7 - Lab Spark: contador de palavras de arquivo.

Autoria: Jaquelinha Costa
Data: Jan/2025
contador_de_palavras.py: script que realiza contagem de frequência
de palavras de arquivo.
"""

from pyspark.sql import SparkSession
import re

# Inicialização de Spark Session
spark = SparkSession.builder \
    .appName("Contagem de Palavras") \
    .getOrCreate()

# Leitura do arquivo
caminho_arquivo = input("Este é o Contador de Palavras!\n\
    Informe o caminho do arquivo a ser processado: ")
texto_rdd = spark.sparkContext.textFile(caminho_arquivo)

# Função para limpeza de caracteres especiais
def limpeza_caracteres(linha):
    palavras = re.split(r'[^\w]+', linha)  # Faz o "split" em caracteres especiais
    return [palavra for palavra in palavras if palavra]  # Filtra strings vazias

# Execução da contagem de palavras
contagem_palavras = (
    texto_rdd
    .flatMap(limpeza_caracteres)         # Separa linhas em palavras
    .map(lambda palavra: (palavra, 1))         # Mapeia cada palavra em (palavra, 1)
    .reduceByKey(lambda a, b: a + b)     # Reduz pela chave, contando ocorrências
)

# Collect and display results
for palavra, contagem in contagem_palavras\
    .sortBy(lambda x: x[1], ascending=False)\
    .collect():
    print(f"{palavra}: {contagem}")
