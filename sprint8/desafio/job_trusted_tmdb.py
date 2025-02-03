"""
Sprint 8 - Desafio Final - Etapa 3b: transformação na Trusted Zone (TMDB).

Conversão de dados para formato Parquet, e ingestão na camada
Trusted do data lake, a partir de Job no AWS Glue.

Autoria: Jaqueline Costa
Data: Jan/25
job_trusted_tmdb.py: script com pipeline de transformação de datasets da 
Raw Zone TMDB do data lake, transformação para Parquet e reingestão 
na Trusted Zone TMDB.

    Outputs / Uploads:
        - Arquivos Parquet na Trusted Zone
            - filmes_tmdb: dataset com filmes do TMDB e colunas de interesse
            - paises_tmdb dataset de países e respectivos códigos
            - linguas_tmdb: dataset de línguas e respectivos códigos
        - log-transformacao-{ano}{mes}{dia}.txt: log de execuções do script
"""

################################################################################
# IMPORTAÇÕES

import sys
import re
import boto3
from datetime import datetime

from pyspark.context import SparkContext
from pyspark.sql.functions import when, col, explode, year, to_date, array, size
from pyspark.sql.types import IntegerType, DoubleType, StringType

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.job import Job

###########################################################################
# CLASSE AUXILIAR


class LogPrinter:
    """Classe de redirecionamento do stdout para log."""

    def __init__(self, nome_arquivo: str):
        """Construtor: obtém o arquivo log e conecta-se ao stdout."""
        self.arq_log = open(nome_arquivo, "a")
        self.stdout = sys.stdout
        sys.stdout = self

    def write(self, dados: str):
        """Escrita de dados com timestamp no stdout e log."""
        if dados.strip():
            timestamp = datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
            registro = f"{timestamp} {dados.strip()}\n"
            self.arq_log.write(registro)
            self.stdout.write(registro)

    def flush(self):
        """Escrita imediata com flush do buffer."""
        self.arq_log.flush()
        self.stdout.flush()

    def close(self):
        """Fechamento do arquivo log."""
        if not self.arq_log.closed:
            self.arq_log.close()
            sys.stdout = self.stdout


################################################################################
# VARIÁVEIS

# Argumentos do Sistema
args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME",
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

# Data Atual
ano_hj, mes_hj, dia_hj = datetime.now().year,\
    f"{datetime.now().month:02}", f"{datetime.now().day:02}"

# Caminho de Input
s3_tmdb_input = args["S3_TMDB_INPUT_PATH"]

# Datas dos Registros da Ingestão no Input
match = re.search(
    r"/(\d{4})/(\d{2})/(\d{2})",
    s3_tmdb_input)
if match:
    ano, mes, dia = map(int, match.groups())

# Caminhos de Output
nome_bucket = args["S3_BUCKET"]
s3_tmdb_output = f"s3://{nome_bucket}/Trusted/TMDB/Parquet/Movies/{ano}/{mes}/{dia}/"
log = f"log-transform-trusted-tmdb-{ano_hj}{mes_hj}{dia_hj}"

# Integração AWS
s3 = boto3.resource("s3")
bucket = s3.Bucket(nome_bucket)

# Reconfiguração do stdout
sys.stdout.reconfigure(encoding="utf-8")
logger = LogPrinter(log)

################################################################################
# CRIAÇÃO DOS SPARK DATAFRAMES

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

# FILMES TMDB __________________________________________________________________

## Conversão de Tipos, Padronização e Seleção de Colunas

filmes_tmdb_df = filmes_tmdb_df.select(
    # Renomeação de Colunas
    col("id").cast(IntegerType()).alias("tmdb_id"),
    col("imdb_id").cast(StringType()),
    col("title").cast(StringType()).alias("titulo_comercial"),
    col("original_title").cast(StringType()).alias("titulo_original"),
    col("original_language").cast(StringType()).alias("lingua_original"),
    col("popularity").cast(DoubleType()).alias("popularidade"),
    col("vote_average").cast(DoubleType()).alias("media_avaliacao"),
    col("vote_count").cast(IntegerType()).alias("qtd_avaliacoes"),
    col("overview").cast(StringType()).alias("sinopse"),
    # Extração do Ano de Lançamento
    year(to_date(col("release_date"))).cast(IntegerType()).alias("ano_lancamento"),

    # Tratativas Pré-Explode: Casos Sem Listas Aninhadas
    when(col("origin_country").isNull(), array())
    .when(size(col("origin_country")) == 0, array())
    .otherwise(col("origin_country")).alias("paises_origem"),

    # Tratativas Pré-Explode: Casos Sem Dicionários Aninhados
    when(col("spoken_languages.iso_639_1").isNull(), array())
    .when(size(col("spoken_languages.iso_639_1")) == 0, array())
    .otherwise(col("spoken_languages.iso_639_1")).alias("linguas_faladas_total")
).select(  # Tratativa Explode: Desaninhamento de Coleções em Linhas
    "*",
    explode(col("paises_origem")).alias("pais_origem"),
    explode(col("linguas_faladas_total")).alias("linguas_faladas")
).drop("paises_origem", "linguas_faladas_total")

# LÍNGUAS TMDB _________________________________________________________________

## Conversão de Tipos, Padronização e Seleção de Colunas

linguas_tmdb_df = linguas_tmdb_df.select(
    col("iso_639_1").cast(StringType()).alias("iso_cod"),
    col("english_name").cast(StringType()).alias("lingua")
)

# PAÍSES TMDB __________________________________________________________________

## Conversão de Tipos, Padronização e Seleção de Colunas

paises_tmdb_df = paises_tmdb_df.select(
    col("iso_3166_1").cast(StringType()).alias("iso_cod"),
    col("english_name").cast(StringType()).alias("pais")
)

################################################################################
# INGRESSÃO NA CAMADA TRUSTED DO BUCKET

# FILMES TMDB __________________________________________________________________

filmes_tmdb_df.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_tmdb_output}/titulos/")

# LÍNGUAS TMDB _________________________________________________________________

linguas_tmdb_df.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_tmdb_output}/linguas/")

# PAÍSES TMDB __________________________________________________________________

paises_tmdb_df.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_tmdb_output}/paises/")
    
print(f"Listagem de objetos no bucket {nome_bucket}")
[print(objeto) for objeto in bucket.objects.all()]

print("Transformação e ingressão na Trusted Zone TMDB realizada com sucesso")
logger.close()
bucket.upload_file(Filename=f"{log}", Key=f"Logs/{log}")

job.commit()


