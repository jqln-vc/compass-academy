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
        - Arquivos Parquet na Trusted Zone:
            - filmes_local
            - filmes_tmdb
            - paises_tmdb
            - linguas_tmdb

"""

################################################################################
# IMPORTAÇÕES

import sys
import re
from pyspark.context import SparkContext
from pyspark.sql.functions import when, col, explode, year, to_date, array, size
from pyspark.sql.types import IntegerType, DoubleType, StringType, ArrayType
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.job import Job

################################################################################
# VARIÁVEIS

# Argumentos do Sistema
args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME",
     "S3_LOCAL_INPUT_PATH",
     "S3_TMDB_INPUT_PATH",
     "S3_BUCKET"
    ]
)

# Ambiente Spark & Glue
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

# Caminhos de Input
s3_local_input = args["S3_LOCAL_INPUT_PATH"]
s3_tmdb_input = args["S3_TMDB_INPUT_PATH"]

# Datas dos Registros da Ingestão no Input
match = re.search(
    r"/(\d{4})/(\d{2})/(\d{2})",
    s3_tmdb_input)
if match:
    ano, mes, dia = map(int, match.groups())

# Caminhos de Output
bucket = args["S3_BUCKET"]
s3_local_output = f"s3://{bucket}/Trusted/Local/Parquet/Movies/"
s3_tmdb_output = f"s3://{bucket}/Trusted/TMDB/Parquet/Movies/{ano}/{mes}/{dia}/"

################################################################################
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

################################################################################
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

filmes_tmdb_df = filmes_tmdb_df.select(
    col("id").cast(IntegerType()).alias("tmdb_id"),
    col("imdb_id").cast(StringType()),
    col("title").cast(StringType()).alias("titulo_comercial"),
    col("original_title").cast(StringType()).alias("titulo_original"),
    col("original_language").cast(StringType()).alias("lingua_original"),
    col("popularity").cast(DoubleType()).alias("popularidade"),
    col("vote_average").cast(DoubleType()).alias("media_avaliacao"),
    col("vote_count").cast(IntegerType()).alias("qtd_avaliacoes"),
    col("overview").cast(StringType()).alias("sinopse"),
    year(to_date(col("release_date"))).cast(IntegerType()).alias("ano_lancamento"),
    # Handle origin countries
    when(col("origin_country").isNull(), array())
    .when(size(col("origin_country")) == 0, array())
    .otherwise(col("origin_country")).alias("paises_origem"),
    # Handle spoken languages
    when(col("spoken_languages.iso_639_1").isNull(), array())
    .when(size(col("spoken_languages.iso_639_1")) == 0, array())
    .otherwise(col("spoken_languages.iso_639_1")).alias("linguas_faladas_full")
).select(
    "*",
    explode(col("paises_origem")).alias("pais_origem"),
    explode(col("linguas_faladas_full")).alias("linguas_faladas")
).drop("paises_origem", "linguas_faladas_full")

# LÍNGUAS TMDB ___________________________________________

# Conversão de Tipos, Padronização e Seleção de Colunas

linguas_tmdb_df = linguas_tmdb_df.select(
    col("iso_639_1").cast(StringType()).alias("iso_cod"),
    col("english_name").cast(StringType()).alias("lingua")
)

# PAÍSES TMDB ____________________________________________

# Conversão de Tipos, Padronização e Seleção de Colunas

paises_tmdb_df = paises_tmdb_df.select(
    col("iso_3166_1").cast(StringType()).alias("iso_cod"),
    col("english_name").cast(StringType()).alias("pais")
)

################################################################################
# INGRESSÃO NA CAMADA TRUSTED DO BUCKET

# FILMES LOCAL ___________________________________________

filmes_local_df.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(s3_local_output)

# FILMES TMDB ____________________________________________

filmes_tmdb_df.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_tmdb_output}")

# LÍNGUAS TMDB ___________________________________________

linguas_tmdb_df.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_tmdb_output}/linguas/")

# PAÍSES TMDB ____________________________________________

paises_tmdb_df.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_tmdb_output}/paises/")

job.commit()
