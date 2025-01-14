"""
Sprint 7 - Lab Spark: contador de palavras de arquivo.

Autoria: Jaqueline Costa
Data: Jan/2025
contador_de_palavras.py: script que realiza contagem de
frequência de palavras de arquivo.
"""

##################################################################
# IMPORTAÇÕES

from pyspark.sql import SparkSession
import re

##################################################################
# VARIÁVEIS

# Inicialização de Spark Session
spark = SparkSession.builder \
    .appName("Contador de Palavras") \
    .getOrCreate()

# Leitura do arquivo e geração de RDD
caminho_arquivo = input("Este é o Contador de Palavras!\n\
    Informe o caminho do arquivo a ser processado: ")
texto_rdd = spark.sparkContext.textFile(caminho_arquivo)

##################################################################
# FUNÇÕES


def limpeza_caracteres(linha: str) -> list[str]:
    """Função de limpeza de caracteres especiais.

    Args:
        linha (str): texto com caracteres especiais.
    Returns:
        list[str]: lista com strings de palavras.
    """
    # Remove caracteres especiais
    palavras = re.split(r'[^\w]+', linha)
    return [palavra
            for palavra
            in palavras
            if palavra]  # Filtra strings vazias


##################################################################
# EXECUÇÃO MAPREDUCE


# Execução da contagem de palavras
contagem_palavras = (
    texto_rdd
    .flatMap(limpeza_caracteres)        # Limpa caracteres / split
    .map(lambda palavra: (palavra, 1))  # Mapeia em (palavra, 1)
    .reduceByKey(lambda a, b: a + b)    # Soma chaves iguais
)

# Ordenação decrescente e visualização da contagem
for palavra, contagem in contagem_palavras\
        .sortBy(lambda x: x[1], ascending=False)\
        .collect():
    print(f"{palavra}: {contagem}")
