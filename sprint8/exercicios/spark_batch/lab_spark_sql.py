"""
"""

#####################################################################
# IMPORTAÇÕES

from pyspark.sql import SparkSession
from pyspark import SparkContext, SQLContext

#####################################################################
# VARIÁVEIS

# Etapa 1 - Criação da Sessão e do DataFrame

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("Lab Spark SQL") \
    .getOrCreate()

df_nomes = spark.read.csv('../gerador_massa/nomes_aleatorios.txt', header=False)
df_nomes.show(5)

# Etapa 2 - Verificação do Schema e Renomeação da Coluna para "Nomes"

# Etapa 3 - Adição da Coluna "Escolaridade"

# Etapa 4 - Adição da Coluna "País"