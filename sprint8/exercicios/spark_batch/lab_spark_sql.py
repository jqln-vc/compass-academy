"""
"""

#####################################################################
# IMPORTAÇÕES

from pyspark.sql import SparkSession, functions as F

#####################################################################
# VARIÁVEIS

# Etapa 1 - Criação da Sessão e do DataFrame

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("Lab Spark SQL") \
    .getOrCreate()

caminho_arquivo = input("Este é o Lab Spark SQL!\n\
Informe o caminho do arquivo a ser processado: ")

print("Etapa 1: Amostra do arquivo ...")
df_nomes = spark.read.csv(caminho_arquivo, header=False)
df_nomes.show(5)

# Etapa 2 - Renomeação da Coluna para "Nomes" e Verificação do Schema

print("Etapa 2: Renomeando coluna Nomes e Verificando Schema ...")
df_nomes = df_nomes.withColumnRenamed("_c0", "Nomes")
df_nomes.printSchema()
df_nomes.show(10)


# Etapa 3 - Adição da Coluna "Escolaridade"

print("Etapa 3: Criando coluna Escolaridade ...")
escolaridades = ["Fundamental", "Medio", "Superior"]

df_nomes = df_nomes.withColumn("Escolaridade", 
    F.expr(f"element_at(shuffle(array{tuple(escolaridades)}),\
           int(rand() * {len(escolaridades)}) + 1)")
)

df_nomes.show(10)

# Etapa 4 - Adição da Coluna "País"

print("Etapa 4: Criando coluna País ...")

paises = [
    "Argentina",
    "Bolívia",
    "Brasil",
    "Chile",
    "Colômbia",
    "Equador",
    "Guiana",
    "Paraguai",
    "Peru",
    "Suriname",
    "Uruguai",
    "Venezuela"
]

df_nomes = df_nomes.withColumn("Pais", 
    F.expr(f"element_at(shuffle(array{tuple(paises)}),\
           int(rand() * {len(paises)}) + 1)")
)

df_nomes.show(10)

# Etapa 5 - Adição da Coluna "AnoNascimento" (anos 1945 a 2010)

print("Etapa 5: Criando coluna AnoNascimento ...")

df_nomes = df_nomes.withColumn("AnoNascimento",
    F.expr("element_at(shuffle(sequence(1945, 2010)),\
           int(rand() * (2010 - 1945 + 1)) + 1)")
)

df_nomes.show(20)

# Etapa 6 - Select de Pessoas Nascidas Neste Século

print("Etapa 6: Select de Pessoas Nascidas Neste Século ...")

df_select = df_nomes.where(F.col("AnoNascimento") >= 2001).select("*")
df_select.show(10)

# Etapa 7 - Select da Etapa Anterior com Spark SQL

print("Etapa 7: Select de Pessoas Nascidas Neste Século com Spark SQL ...")

df_nomes.createOrReplaceTempView("pessoas")
spark.sql("SELECT * FROM pessoas WHERE AnoNascimento >= 2001").show()

# Etapa 8 - Contagem de Millennials (1980 a 1994) com Filter

print("Etapa 8: Contagem de Millennials com Filter ...")

qtd_millennials = df_nomes.filter(F.col("AnoNascimento").between(1980, 1994)).count()
print(f"Quantidade de millennials: {qtd_millennials}")

# Etapa 9 - Contagem da Etapa Anterior com Spark SQL

print("Etapa 9: Contagem de Millennials com Spark SQL ...")

spark.sql("""
          SELECT count(Nomes) as Qtd_Millennials
          FROM pessoas
          WHERE AnoNascimento >= 1980 AND AnoNascimento <= 1994
          """).show()

# Etapa 10 - Quantidade de Pessoas por Geração por País

print("Etapa 10: Contagem de Pessoas por País e Geração com Spark SQL ...")

df_geracoes = spark.sql("""
    SELECT Pais,
        CASE 
            WHEN AnoNascimento BETWEEN 1944 AND 1964 THEN 'Baby Boomer'
            WHEN AnoNascimento BETWEEN 1965 AND 1979 THEN 'Geração X'
            WHEN AnoNascimento BETWEEN 1980 AND 1994 THEN 'Millennial'
            WHEN AnoNascimento BETWEEN 1995 AND 2015 THEN 'Geração Z'
            ELSE 'Desconhecido'
        END AS Geracao,
        COUNT(*) AS Quantidade
    FROM pessoas
    GROUP BY Pais, Geracao
    ORDER BY Pais, Geracao, Quantidade
    """)

df_geracoes.show()
