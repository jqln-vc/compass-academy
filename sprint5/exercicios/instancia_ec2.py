"""
Sprint 5 - Exercício Lab AWS: criação de instância EC2.

Autoria: Jaqueline Costa
Data: Dez/24

instancia_ec2.py: script para criação de instância EC2 com configuração
específica.
"""


import boto3
import os

aws_access_key_id = os.environ['COMPASS_AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['COMPASS_AWS_SECRET_ACCESS_KEY']
aws_session_token = os.environ['COMPASS_AWS_SESSION_TOKEN']

ec2 = boto3.resource(
    'ec2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

client = boto3.client(
    'ec2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

instancia = ec2.create_instances(
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    ImageId='ami-01816d07b1128cd2d',
    SecurityGroupIds=['sg-0d6ef352a55e76f70'],
    SubnetId='subnet-06f3b296bdca98a9f',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'compass-sprint5'},
                {'Key': 'Project', 'Value': 'Programa de Bolsas'},
                {'Key': 'CostCenter', 'Value': 'Data & Analytics'}
            ]
        },
        {
            'ResourceType': 'volume',
            'Tags': [
                {'Key': 'Name', 'Value': 'compass-sprint5'},
                {'Key': 'Project', 'Value': 'Programa de Bolsas'},
                {'Key': 'CostCenter', 'Value': 'Data & Analytics'}
            ]
        }
    ],
)


# Capturando o id da instância EC2 criada | instance é uma lista
id_instancia = instancia[0].id

# Obtendo os detalhes da instância criada
resposta = client.describe_instances(InstanceIds=[id_instancia])

# Acessando os detalhes da instância
config_instancia = resposta['Reservations'][0]['Instances'][0]

# # Extraindo dados relevantes
estado_instancia = config_instancia['State']['Name']
tipo_instancia = config_instancia['InstanceType']

tags = config_instancia.get('Tags', [])
tags_dict = {tag['Key']: tag['Value'] for tag in tags}

print(f"""Instância criada com o ID: {id_instancia}
      Estado da instância: {estado_instancia}
      Tipo da instância: {tipo_instancia}
      Tags da instância: {tags_dict}""")
