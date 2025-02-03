"""
Sprint 8 - Desafio Final - Etapa 3a: ingressão de dados na Trusted Zone (Local).

Conversão de dados para formato Parquet, e ingestão na camada
Trusted do data lake, a partir de Job no AWS Glue.

Autoria: Jaqueline Costa
Data: Jan/25
job_trusted_local.py: script com pipeline de transformação de datasets da 
Raw Zone Local do data lake, transformação para Parquet e reingestão 
na Trusted Zone Local.

    Outputs / Uploads:
        - Arquivos Parquet na Trusted Zone:
            - filmes_local: dataset com filmes locais e colunas de interesse
        - log-transformacao-{ano}{mes}{dia}.txt: log de execuções do script
"""

################################################################################
# IMPORTAÇÕES

import sys
import boto3
from datetime import datetime

from pyspark.context import SparkContext
from pyspark.sql.functions import when, col
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
     "S3_LOCAL_INPUT_PATH",
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
ano, mes, dia = datetime.now().year,\
    f"{datetime.now().month:02}", f"{datetime.now().day:02}"

# Caminho de Input
s3_local_input = args["S3_LOCAL_INPUT_PATH"]

# Informações de Output
nome_bucket = args["S3_BUCKET"]
s3_local_output = f"s3://{nome_bucket}/Trusted/Local/Parquet/Movies/"
log = f"log-transform-trusted-local-{ano}{mes}{dia}"

# Integração AWS
s3 = boto3.resource("s3")
bucket = s3.Bucket(nome_bucket)

# Reconfiguração do stdout
sys.stdout.reconfigure(encoding="utf-8")
logger = LogPrinter(log)

################################################################################
# CRIAÇÃO DO SPARK DATAFRAME

# DataFrame Filmes Local
filmes_local_df = spark.read \
    .option("header", "true") \
    .option("delimiter", "|") \
    .csv(f"{s3_local_input}/movies.csv")

################################################################################
# TRANSFORMAÇÕES

# FILMES LOCAL _________________________________________________________________

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
    col("id").cast(StringType()).alias("imdb_id"),
    col("tituloPincipal").cast(StringType()).alias("titulo_comercial"),
    col("tituloOriginal").cast(StringType()).alias("titulo_original"),
    col("anoLancamento").cast(IntegerType()).alias("ano_lancamento"),
    col("notaMedia").cast(DoubleType()).alias("media_avaliacao"),
    col("numeroVotos").cast(IntegerType()).alias("qtd_avaliacoes")
)

################################################################################
# INGRESSÃO NA CAMADA TRUSTED DO BUCKET

# FILMES LOCAL _________________________________________________________________

romances_local_df.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(s3_local_output)
    
print(f"Listagem de objetos no bucket {nome_bucket}")
[print(objeto) for objeto in bucket.objects.all()]

print("Transformação e ingressão na Trusted Zone Local realizada com sucesso")
logger.close()
bucket.upload_file(Filename=f"{log}", Key=f"Logs/{log}")

job.commit()
