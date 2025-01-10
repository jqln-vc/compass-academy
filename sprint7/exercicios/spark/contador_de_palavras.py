"""
Sprint 7 - Lab Spark: contador de palavras de arquivo.

Autoria: Jaquelinha Costa
Data: Jan/2025
contador_de_palavras.py: script que realiza u
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
    .flatMap(limpeza_caracteres)            # Split linhas into words
    .map(lambda word: (word, 1))         # Map each word to (word, 1)
    .reduceByKey(lambda a, b: a + b)     # Reduce by key to count occurrences
)

# Collect and display results
for palavra, contagem in contagem_palavras\
    .sortBy(lambda x: x[1], ascending=False)\
    .collect():
    print(f"{word}: {count}")
