import json
import pandas
import boto3
 
 
def lambda_handler(event, context):
    s3_client = boto3.client('s3')
 
    nome_bucket = 'compass-sprint5-lab'
    nome_arquivo = 'dados/nomes.csv'
    objeto = s3_client.get_object(Bucket=nome_bucket, Key=nome_arquivo)
    df=pandas.read_csv(objeto['Body'], sep=',')
    linhas = len(df.axes[0])
 
    return {
        'statusCode': 200,
        'body': f"Este arquivo tem {linhas} linhas"
    }