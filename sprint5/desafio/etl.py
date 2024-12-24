"""Sprint 5 - Desafio Dados Gov: análise de dados integrada ao AWS S3.

Autoria: Jaqueline Costa
Data: Dez/24
etl.py: script com pipeline de extração/consolidação de dados,
execução de script de análise e integração com uploads para um bucket S3.

    Outputs / Uploads:
        - dataset.csv: dataset consolidado a partir de dados raw.
        - analise.csv: análise final do dataset.
        - output_log.txt: arquivo de logs de execução.

"""
##############################################################################
# IMPORTAÇÕES DE MÓDULOS E BIBLIOTECAS
#

import sys
import os
import subprocess
from datetime import datetime
import runpy as rp
import pandas as pd
import glob
import boto3

##############################################################################
# CLASSES E FUNÇÕES
#


def concatenador_csv(caminho_arquivos: str,
                     arquivo_output: str,
                     delimitador: str,
                     encoding: str) -> str:
    """
    Une diversos arquivos CSV com o mesmo schema em um único CSV.

    Args:
        caminho_arquivos (str): caminho para o diretório com os CSV de input.
        arquivo_output (str): caminho para o output do CSV final.
        delimitador (str): símbolo de delimitação de colunas.
        encoding (str): codificação de caracteres do arquivo.

    Returns:
        str: nome do arquivo de output.
        bool: False se ocorrer erro.
    """
    try:
        # Obter todos os arquivos CSV no diretório
        arqs_csv = glob.glob(os.path.join(caminho_arquivos, "*.csv"))

        # Armazenar os DataFrames individualmente
        dfs = []

        # Ler cada arquivo CSV e adicionar à lista
        for arquivo in arqs_csv:
            print(f"Processando: {arquivo}")
            try:
                df = pd.read_csv(
                    arquivo,
                    delimiter=delimitador,
                    encoding=encoding,
                    quotechar='"',
                    na_values=['', 'NA', 'NULL'],  # Tratar campos vazios
                    keep_default_na=True
                )

                # Remover quaisquer linhas vazias
                df = df.dropna(how='all')

                dfs.append(df)
                print(f"Arquivo {arquivo} processado com sucesso")

            except Exception as e:
                print(f"Erro ao processar o arquivo {arquivo}: {str(e)}")
                return False

        # Concatenar todos os DataFrames
        final_df = pd.concat(dfs, ignore_index=True)

        # Exportar o DataFrame concatenado para um arquivo CSV
        final_df.to_csv(
            arquivo_output,
            index=False,
            sep=delimitador,
            quotechar='"',
            na_rep=''  # Representa valores NA como strings vazias
        )

        print(f"{len(arqs_csv)} arquivos concatenados em {arquivo_output}")
        print(f"Quantidade de linhas no arquivo final: {len(final_df)}")

        return arquivo_output

    except Exception as e:
        print(f"Um erro ocorreu: {str(e)}")
        return False


class LogPrinter:
    """Classe de redirecionamento do stdout para log."""

    def __init__(self, nome_arquivo: str):
        """Construtor: obtém o arquivo log e conecta-se ao stdout."""
        self.arq_log = open(nome_arquivo, 'a')
        self.stdout = sys.stdout
        sys.stdout = self

    def write(self, dados: str):
        """Escrita de dados com timestamp no stdout e log."""
        if dados:
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
aws_access_key_id = os.environ['COMPASS_AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['COMPASS_AWS_SECRET_ACCESS_KEY']
aws_session_token = os.environ['COMPASS_AWS_SESSION_TOKEN']

# Recurso S3
s3 = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

# Caminhos e Arquivos
diretorio_raw = "./dados_raw"
raw_csvs = glob.glob(os.path.join(diretorio_raw, "*.csv"))
output_csv = "dataset.csv"
nome_balde = "compass-sprint5-desafio-ancine"
analise = "analise.csv"
log = 'output_log.txt'

# Reconfiguração do stdout
logger = LogPrinter(log)

##############################################################################
# PIPELINE DE EXECUÇÃO
#

if __name__ == '__main__':

    print("Início da sequência de execução")
    print(f"Criação do bucket no S3: {nome_balde}")
    balde = s3.create_bucket(Bucket=nome_balde)

    print(f"Upload de dados originais do diretorio: {diretorio_raw}")
    for arquivo_raw in raw_csvs:
        print(f"Upload de dataset: {arquivo_raw}")
        nome_arq = os.path.basename(arquivo_raw)
        balde.upload_file(Filename=arquivo_raw, Key=f'dados_raw/{nome_arq}')

    print("Concatenação de dados originais em um único dataset")
    dataset = concatenador_csv(diretorio_raw,
                               output_csv,
                               delimitador=';',
                               encoding='utf-8')

    print("Upload do dataset concatenado no bucket")
    balde.upload_file(Filename=dataset,
                      Key=f'{dataset}')

    print("Deleção do dataset concatenado após upload no bucket")
    subprocess.call(['rm', f'{dataset}'], text=True)

    print("Download do dataset para etapa de análise")
    balde.download_file(Key=f'{dataset}', Filename=dataset)

    print("Início do script de análise do dataset")
    namespace = rp.run_path('analise.py')
    print(f"Análise concluída, veja uma prévia:\n{namespace['df'].head()}")

    print("Upload do arquivo de análise para o bucket")
    balde.upload_file(Filename=analise, Key=f'{analise}')

    print("Fim da sequência de execução")
    logger.close()
    balde.upload_file(Filename=log, Key=f'{log}')
