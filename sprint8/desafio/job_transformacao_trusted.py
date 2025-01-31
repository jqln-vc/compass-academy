"""
Sprint 8 - Desafio Final - Etapa 3: transformação na Trusted Zone.

Conversão de dados para formato Parquet, e ingestão na camada
Trusted do data lake, a partir de Job no AWS Glue.

Autoria: Jaqueline Costa
Data: Jan/25
job_transformacao_trusted.py: script com pipeline de seleção de
atributos de interesse provenientes da camada Raw do data lake, 
transformação para Parquet e reingestão na camada Trusted.

    Outputs / Uploads:
        -

"""

#################################################################
# IMPORTAÇÕES

import sys
import re
from pyspark.context import SparkContext
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, DoubleType, StringType, ArrayType
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.job import Job

#################################################################
# VARIÁVEIS

# Argumentos do Sistema
args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME",
     "S3_LOCAL_INPUT_PATH",
     "S3_TMDB_INPUT_PATH",
     "S3_LOCAL_TARGET_PATH",  #s3://bucket/Trusted/Local/Parquet/movies/movies.parquet
     "S3_TMDB_TARGET_PATH"    #s3://bucket/Trusted/TMDB/Parquet/movies/2025/01/30/linguas.parquet
    ]
)

# Ambiente Spark & Glue
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

# Caminhos de Input e Output
s3_local_input = args["S3_LOCAL_INPUT_PATH"]
s3_tmdb_input = args["S3_TMDB_INPUT_PATH"]
s3_local_output = args["S3_LOCAL_TARGET_PATH"]
s3_tmdb_output = args["S3_TMDB_TARGET_PATH"]

# Datas dos Registros da Ingestão
match = re.search(
    r"/(\d{4})/(\d{2})/(\d{2})",
    s3_tmdb_input)

if match:
    ano, mes, dia = map(int, match.groups())
    if re.search(
        r"/(\d{4})/(\d{2})/(\d{2})",
        s3_tmdb_input)

# Colunas: Filmes Local
colunas_filmes_local = [
    "tmdb_id",             # id
    "titulo_comercial",    # tituloPincipal
    "titulo_original",     # tituloOriginal
    "ano_lancamento",      # anoLancamento
    "media_avaliacao",     # notaMedia
    "qtd_avaliacoes"       # numeroVotos
]

# Colunas: Filmes TMDB
colunas_filmes_tmdb = [
    "tmdb_id",             # id
    "imdb_id",
    "titulo_comercial",    # title
    "titulo_original",     # original_title
    "pais_origem",         # origin_country
    "lingua_original",     # original_language
    "linguas_faladas",     # spoken_languages
    "ano_lancamento",      # release_date
    "popularidade",        # popularity
    "media_avaliacao",     # vote_average
    "qtd_avaliacoes",      # vote_count
    "sinopse"              # overview
]

# Colunas: Línguas TMDB
colunas_linguas_tmdb = [
    "iso_cod",             # iso_639_1
    "nome_lingua"          # english_name
]

# Colunas: Países TMDB
colunas_paises_tmdb = [
    "iso_cod",             # iso_3166_1
    "pais"                 # english_name
]

#################################################################
# CRIAÇÃO DOS SPARK DATAFRAMES

# DataFrame Filmes Local
filmes_local_df = spark.read \
    .option("header", "true") \
    .option("delimiter", "|") \
    .csv(f"{s3_local_input}/movies.csv")

# DataFrame Filmes TMDB
filmes_tmdb_df = spark.read \
    .option("multiline", "true") \
    .option("mode", "PERMISSIVE") \
    .json(f"{s3_tmdb_input}/filmes*.json")
    
# DataFrame Países TMDB
paises_tmdb_df = spark.read \
    .option("multiline", "true") \
    .option("mode", "PERMISSIVE") \
    .json(f"{s3_tmdb_input}/paises.json")

# DataFrame Línguas TMDB
linguas_tmdb_df = spark.read \
    .option("multiline", "true") \
    .option("mode", "PERMISSIVE") \
    .json(f"{s3_tmdb_input}/linguas.json")

#################################################################
# TRANSFORMAÇÕES

# FILMES LOCAL ___________________________________________

# Recorte Gênero: (Somente) Romance
romances_local_df = filmes_local_df.where(
    col("genero") \
    .rlike(r"^Romance$"))

# Recorte Temporal: Ano de Lançamento a Partir de 2013
## Substituição de Valores Nulos (0)
romances_local_df = romances_local_df.withColumn(
    "anoLancamento",
    when(col("anoLancamento") \
        .rlike(r"^[a-zA-Z]+$"), 0) \
        .otherwise(col("anoLancamento")))

## Conversão da Coluna: Integer
romances_local_df = romances_local_df.withColumn(
    "anoLancamento",
    col("anoLancamento") \
    .cast("int"))

## Seleção de Valores do Recorte
romances_local_df = romances_local_df.where(
    col("anoLancamento") >= 2013)

# Eliminação de Duplicações de Filmes

romances_local_df = romances_local_df.drop_duplicates(["id"])

# Conversão de Tipos, Padronização e Seleção de Colunas

romances_local_df = romances_local_df.select(
    col("id").cast(StringType()).alias("tmdb_id"),
    col("tituloPincipal").cast(StringType()).alias("titulo_comercial"),
    col("tituloOriginal").cast(StringType()).alias("titulo_original"),
    col("anoLancamento").cast(IntegerType()).alias("ano_lancamento"),
    col("notaMedia").cast(DoubleType()).alias("media_avaliacao"),
    col("numeroVotos").cast(IntegerType()).alias("qtd_avaliacoes")
)

# FILMES TMDB ____________________________________________

# Conversão de Tipos, Padronização e Seleção de Colunas

# Colunas: Filmes TMDB
colunas_filmes_tmdb = [
    "tmdb_id",             # id
    "imdb_id",
    "titulo_comercial",    # title
    "titulo_original",     # original_title
    "pais_origem",         # origin_country
    "lingua_original",     # original_language
    "linguas_faladas",     # spoken_languages
    "ano_lancamento",      # release_date
    "popularidade",        # popularity
    "media_avaliacao",     # vote_average
    "qtd_avaliacoes",      # vote_count
    "sinopse"              # overview
]


filmes_tmdb_df = filmes_tmdb_df.where(
    col("id").cast(IntegerType()).alias("tmdb_id"),
    col("imdb_id").cast(StringType()),
    col("title").cast(StringType()).alias("titulo_comercial"),
    col("original_title").cast(StringType()).alias("titulo_original"),
    col("origin_country").cast()
)

# LÍNGUAS TMDB ___________________________________________

# Conversão de Tipos, Padronização e Seleção de Colunas

# PAÍSES TMDB ____________________________________________

# Conversão de Tipos, Padronização e Seleção de Colunas


#################################################################
# INGRESSÃO NA CAMADA TRUSTED DO BUCKET

# FILMES LOCAL ___________________________________________


# FILMES TMDB ____________________________________________

# LÍNGUAS TMDB ___________________________________________

# PAÍSES TMDB ____________________________________________

df2.write.mode("write") \
    .format("parquet") \
    .save(bucket)

job.commit()
