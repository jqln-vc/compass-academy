"""Sprint 6 - Desafio Final - Etapa 1: ingestão na camada raw do data lake.

Autoria: Jaqueline Costa
Data: Jan/25
ingestao.py: script com pipeline de criação de bucket S3 e ingestão de
datasets para a camada raw do data lake.

    Outputs / Uploads:
        - movies.csv: arquivo enviado para o bucket.
        - series.csv: análise final do dataset.
        - log-ingestao-{ano}{mes}{dia}.txt: arquivo de logs de execução.

"""
##############################################################################
# IMPORTAÇÕES DE MÓDULOS E BIBLIOTECAS
#

import os
import sys
import glob
import getpass
from datetime import datetime
import boto3

##############################################################################
# CLASSES E FUNÇÕES
#


class LogPrinter:
    """Classe de redirecionamento do stdout para log."""

    def __init__(self, nome_arquivo: str):
        """Construtor: obtém o arquivo log e conecta-se ao stdout."""
        self.arq_log = open(nome_arquivo, 'a')
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


##############################################################################
# VARIÁVEIS
#

# Chaves de Acesso
aws_access_key_id = getpass.getpass("Insira sua AWS Access Key ID: ")
aws_secret_access_key = getpass.getpass("Insira sua AWS Secret Access Key: ")
aws_session_token = getpass.getpass("Insira seu AWS Session Token: ")

# Recurso S3
s3 = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

# Data Atual
ano, mes, dia = datetime.now().year,\
    f"{datetime.now().month:02}", f"{datetime.now().day:02}"

# Caminhos e Arquivos
diretorio_raw = "./dados_raw"
raw_csvs = glob.glob(os.path.join(diretorio_raw, "*.csv"))
nome_balde = "compass-desafio-final-dramance"
log = f'log-ingestao-{ano}{mes}{dia}.txt'

# Reconfiguração do stdout
logger = LogPrinter(log)

##############################################################################
# PIPELINE DE EXECUÇÃO
#

if __name__ == '__main__':

    print("Início da sequência de execução de ingestão")
    balde = s3.create_bucket(Bucket=nome_balde)
    print(f"Criação do bucket no S3: {nome_balde}")

    print(f"Upload de dados originais do diretório: {diretorio_raw}")
    for arquivo_raw in raw_csvs:
        nome_arq = os.path.basename(arquivo_raw)
        fonte = 'Movies' if nome_arq == 'movies.csv' else 'Series'
        caminho_raw = f'Raw/Local/CSV/{fonte}/{ano}/{mes}/{dia}/{nome_arq}'
        balde.upload_file(Filename=arquivo_raw, Key=caminho_raw)
        print(f"Upload de dataset {nome_arq} no caminho {caminho_raw}")
    
    print("Listagem de objetos no bucket")
    [print(objeto) for objeto in balde.objects.all()]
    
    print("Ingestão realizada com sucesso")
    logger.close()
    balde.upload_file(Filename=log, Key=f'Logs/{log}')
