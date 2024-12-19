"""
"""

##############################################################################
# IMPORTAÇÕES DE MÓDULOS E BIBLIOTECAS
#

import pandas as pd
import glob
import boto3
import os
import subprocess
import runpy as rp

##############################################################################
# VARIÁVEIS
#

aws_access_key_id = os.environ['COMPASS_AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['COMPASS_AWS_SECRET_ACCESS_KEY']
aws_session_token = os.environ['COMPASS_AWS_SESSION_TOKEN']

s3 = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

diretorio_raw = "./dados_raw"
raw_csvs = glob.glob(os.path.join(diretorio_raw, "*.csv"))
output_csv = "dataset.csv"
nome_balde = "compass-sprint5-desafio-ancine-4"
analise = "analise.csv"


##############################################################################
# FUNÇÕES
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
        
        if not arqs_csv:
            print("Não existem arquivos CSV no diretório indicado.")
            return False
            
        # Criar uma lista vazia para armazenar os DataFrames individualmente
        dfs = []
        
        # Ler cada arquivo CSV e adicionar à lista
        for file in arqs_csv:
            print(f"Processando: {file}")
            try:
                df = pd.read_csv(
                    file,
                    delimiter=delimitador,
                    encoding=encoding,
                    quotechar='"',
                    na_values=['', 'NA', 'NULL'],  # Tratar campos vazios
                    keep_default_na=True
                )
                
                # Remover quaisquer linhas vazias
                df = df.dropna(how='all')
                
                dfs.append(df)
                print(f"Arquivo {file} processado com sucesso.")
                
            except Exception as e:
                print(f"Erro ao processar o arquivo {file}: {str(e)}")
                break
            
        if not dfs:
            print("Sem DataFrames válidos para concatenar.")
            return False
            
        # Concatenar todos os DataFrames
        final_df = pd.concat(dfs, ignore_index=True)
        
        # Exportar o DataFrame concatenado para um arquivo CSV
        # Manter as mesmas configurações
        final_df.to_csv(
            arquivo_output,
            index=False,
            sep=delimitador,
            quotechar='"',
            na_rep=''  # Representa valores NA como strings vazias
        )
        
        print(f"{len(arqs_csv)} arquivos concatenados em {arquivo_output}.")
        print(f"Quantidade de linhas no arquivo final: {len(final_df)}")
        
        return arquivo_output
        
    except Exception as e:
        print(f"Um erro ocorreu: {str(e)}")
        return False


##############################################################################
# PIPELINE DE EXECUÇÃO
#

if __name__ == '__main__':
    
    print(f"Criando o bucket: {nome_balde}")
    balde = s3.create_bucket(Bucket=nome_balde)
    
    print(f"Fazendo upload de arquivos raw no diretorio: {diretorio_raw}")
    for arquivo_raw in raw_csvs:
        print(arquivo_raw)
        nome_arq = os.path.basename(arquivo_raw)
        balde.upload_file(Filename=arquivo_raw, Key=f'raw/{nome_arq}')
    
    print(f"Iniciando concatenação dos arquivos raw em um único dataset")
    dataset = concatenador_csv(diretorio_raw,
                               output_csv,
                               delimitador=';',
                               encoding='utf-8')
    
    print(f"Realizando upload do dataset concatenado no bucket")
    balde.upload_file(Filename=dataset,
                      Key=f'{dataset}')
    
    print(f"Iniciando deleção do dataset após upload no bucket")
    subprocess.call(['rm', f'{dataset}'], text=True)
    print(f"Deleção do dataset concluída.")
    
    print(f"Iniciando download do dataset para início da etapa de análise")
    balde.download_file(Key=f'{dataset}', Filename=dataset)
    
    print(f"Realizando análise do dataset...")
    namespace = rp.run_path(f'analise.py')
    print(f"Análise concluída. Prévia das primeiras linhas:\n{namespace['df'].head()}")
    
    print(f"Iniciando upload da análise para o bucket...")
    balde.upload_file(Filename=analise,
                      Key=f'{analise}')
    print(f"Upload da análise concluído!\nPipeline executado com sucesso!")
    