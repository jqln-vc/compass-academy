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

instance = ec2.create_instances(
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
instance_id = instance[0].id

# Obtendo os detalhes da instância criada
response = client.describe_instances(InstanceIds=[instance_id])

# Acessando os detalhes da instância
instance_details = response['Reservations'][0]['Instances'][0]

# # Extraindo dados relevantes
instance_state = instance_details['State']['Name']
instance_type = instance_details['InstanceType']

tags = instance_details.get('Tags', [])
tags_dict = {tag['Key']: tag['Value'] for tag in tags}

print(f"""Instância criada com o ID: {instance_id}
      Estado da instância: {instance_state}
      Tipo da instância: {instance_type}
      Tags da instância: {tags_dict}""")
