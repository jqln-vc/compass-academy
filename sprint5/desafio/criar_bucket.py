"""
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
"""


import boto3
import json
from botocore.exceptions import ClientError

def criar_bucket(caminho_template: str) -> dict:
    """
    Cria um bucket S3 a partir de um template JSON.
    
    Args:
    caminho_template (str): Caminho para o arquivo template JSON.
    
    Returns:
    dict: Resposta contendo o status de conclusão e detalhes do bucket.
    """
    try:
        # Read the template file
        with open(caminho_template: str, 'r') as arquivo_template:
            config = json.load(arquivo_template)
        
        # Inicializa um cliente S3
        cliente_s3 = boto3.client('s3')
        
        # Extrai informações de configuração do bucket
        nome = config['bucketName']
        regiao = config.get('region', 'us-east-1')
        
        # Cria o bucket com restrições de região
            # us-east-1 é a região default
            # para demais regiões utilizar LocationConstraint
        if regiao == 'us-east-1':
            resposta = cliente_s3.create_bucket(
                Bucket=nome
            )
        else:
            resposta = cliente_s3.create_bucket(
                Bucket=nome,
                CreateBucketConfiguration={
                    'LocationConstraint': regiao
                }
            )
        
        # Aplica o tipo de versionamento, se especificado
        if 'versioning' in config:
            cliente_s3.put_bucket_versioning(
                Bucket=nome,
                VersioningConfiguration={
                    'Status': config['versioning']}  # 'Enabled' ou 'Suspended'
            )

        # Aplica encriptação se especificado
        if config.get('encryption', False):
            cliente_s3.put_bucket_encryption(
                Bucket=nome,
                ServerSideEncryptionConfiguration={
                    'Rules': [
                        {
                            'ApplyServerSideEncryptionByDefault': {
                                'SSEAlgorithm': 'AES256'
                            }
                        }
                    ]
                }
            )
        
        # Aplica acesso público se especificado
        if config.get('blockPublicAccess', True):
            cliente_s3.put_public_access_block(
                Bucket=nome,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
        
        return {
            'status': 'Sucesso',
            'mensagem': f'Bucket {nome} criado com sucesso!',
            'nome': nome,
            'regiao': regiao
        }
    
    except ClientError as e:
        return {
            'status': 'Erro',
            'mensagem': str(e),
            'codigo_erro': e.resposta['Error']['Code']
        }
    except Exception as e:
        return {
            'status': 'Erro',
            'mensagem': str(e)
        }


if __name__ == "__main__":
    result = criar_bucket('bucket_template.json')
    print(json.dumps(result, indent=2))