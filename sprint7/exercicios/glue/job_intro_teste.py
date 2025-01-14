"""
Sprint 7 - AWS Glue Lab: script de introdução ao Glue.

Data: Jan/25
job_intro_teste.py: script de análise teste em Spark,
com integração entre Glue e S3, salvando output em parquet.
"""

#################################################################
# IMPORTAÇÕES

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

#################################################################
# VARIÁVEIS

args = getResolvedOptions(
    sys.argv,
    ['JOB_NAME',
     'S3_INPUT_PATH',
     'S3_TARGET_PATH']
    )

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args['JOB_NAME'], args)

source_file = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']

df = glue_context.create_dynamic_frame.from_options(
    connection_type='s3',
    connection_options={'paths': [source_file]},
    format='csv',
    format_options={
        'withHeader': True,
        'separator': ','
    }
)

#################################################################
# EXECUÇÃO DA ANÁLISE TESTE

# Filtro de linhas do dataset
only_1934 = df.filter(lambda row: row['ano'] == '1934')

# Envio do resultado para bucket, no formato parquet
glue_context.write_dynamic_frame.from_options(
    frame=only_1934,
    connection_type='s3',
    connection_options={'path': target_path},
    format='parquet')

job.commit()
