"""
Sprint 7 - AWS Glue Lab: script de resolução do exercício.

Autoria: Jaqueline Costa
Data: Jan/25
job_exercicio.py: 
"""

#################################################################
# IMPORTAÇÕES

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import upper, sum, desc
from awsglue.context import GlueContext
from awsglue.job import Job

#################################################################
# VARIÁVEIS

args = getResolvedOptions(
    sys.argv, 
    ['JOB_NAME', 
     'S3_INPUT_PATH', 
     'S3_TARGET_PATH'
    ]
)

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_file = args['S3_INPUT_PATH']
bucket = args['S3_TARGET_PATH']

df = glueContext.create_dynamic_frame.from_options(
    connection_type='s3',
    connection_options={'paths': [source_file]},
    format='csv',
    format_options={
        'withHeader': True,
        'separator': ','
    }
)

df = df.toDF()


#################################################################
# EXECUÇÃO DE ANÁLISES

print('Etapa 1: Esquema do DataFrame')
df.printSchema()

print('Etapa 2: Nomes em Maiúsculas')
df2 = df.withColumn('nome', upper(df['nome']))
df2.show(10)

print('Etapa 3: Contagem de Linhas')
print(f'{df.count()} linhas')

print('Etapa 4: Contagem de nomes agrupados por ano e sexo')
df4 = df2.select('nome', 'sexo', 'total', 'ano') \
    .groupBy('nome', 'ano', 'sexo') \
    .agg(sum('total').alias('soma_total')) \
    .orderBy(desc('ano'))
df4.show(10)

print('Etapa 5: Nome Feminino com Mais Ocorrências')
df5 = df2.filter(df.sexo == 'F') \
    .orderBy(desc('total')) \
    .select('nome', 'total', 'ano') \
    .limit(1)
df5.show()

print('Etapa 6: Nome Masculino com Mais Ocorrências')
df6 = df2.filter(df.sexo == 'M') \
    .orderBy(desc('total')) \
    .select('nome', 'total', 'ano') \
    .limit(1)
df6.show()

print('Etapa 7: Nome Masculino com Mais Ocorrências')
df7 = df2.groupBy('ano') \
    .agg(sum('total').alias('soma_total')) \
    .orderBy('ano')
df7.show(10)

print('Etapa 8: Salvando DataFrame no Bucket')
df2.write.mode("overwrite") \
    .format('json') \
    .partitionBy('sexo', 'ano') \
    .save(bucket)

job.commit()
