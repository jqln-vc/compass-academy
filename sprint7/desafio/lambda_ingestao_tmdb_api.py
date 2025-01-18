"""Sprint 7 - Desafio Final - Etapa 2: ingestão de dados via API do TMDB.

Autoria: Jaqueline Costa
Data: Jan/25
ingestao_tmdb_api.py: script com pipeline de requisição de dados via API
e ingestão na camada raw do data lake.

    Outputs / Uploads:
        - filmes_attr_batch_{batch_n}.json: arquivos de dados obtidos
        via API do TMDB.
        - log-ingestao-{ano}{mes}{dia}.txt: arquivo de logs de execução.

"""

###########################################################################
# IMPORTAÇÕES

import json
import csv
import boto3
import requests
import os
import sys
from datetime import datetime
from math import ceil

###########################################################################
# CLASSES E FUNÇÕES

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


def processador_api_batch(filmes_id: list[str],
                          headers: dict,
                          paises_excluidos: list[str],
                          atributos: list[str],
                          s3_bucket: str,
                          tam_batch: int = 100,
                          caminho_output: str = "./api_data"
                          ) -> None:
    """
    Processador de requisição de filmes por ID em batch, output em JSON.
    Upload de arquivos em bucket AWS S3.

    Args:
        filmes_id (list[str]): IDs de filmes para processar
        headers (dict): header com chaves para request na API
        paises_excluidos (list[str]): países para exclusão
        atributos (list[str]): atributos a salvar no arquivo JSON
        s3_bucket (str): nome do AWS S3 bucket
        tam_batch (int): número de IDs processados por batch
            default: 100
        caminho_output (str): saída para os arquivos JSON
            default: ./api_data
    """
    # Calcula o número total de batches
    total_batches = ceil(len(filmes_id) / tam_batch)
        
    for batch_n in range(total_batches):
        inicio = batch_n * tam_batch
        fim = min(inicio + tam_batch, len(filmes_id))
        batch_n += 1
            
        # Processa o batch atual
        dados = []
        batch_atual = filmes_id[inicio:fim]
            
        print(f"Processando batch {batch_n}/{total_batches}"
              f"(IDs {inicio} to {fim})")
            
        for _id in batch_atual:
            try:
                url = f"https://api.themoviedb.org/3/movie/{_id}?language=en-US"
                resposta = requests.get(url, headers=headers)

                if resposta.status_code == 200:
                    dados_tmdb = resposta.json()

                    # Verifica condições de exclusão
                    if (dados_tmdb["origin_country"][0]
                        not in paises_excluidos
                        and dados_tmdb["original_language"] != "en"):

                        print(f"Adicionado id: {_id}")
                        dados.append(dados_tmdb)
                else:
                    print(f"Erro em obter o filme de id: {_id}"
                          f".Status: {resposta.status_code}")

            except Exception as e:
                print(f"Erro ao processar filme de id {_id}: {str(e)}."
                      f"Status: {resposta.status_code}")
                continue
            
        # Filtrar atributos de interesse e salvar o batch em json
        if dados:
            dados_filtrados = [{chave: item[chave] 
                                for chave in atributos} 
                               for item in dados]
            try:
                s3_bucket.put_object(
                    Key=f"{caminho_output}/filmes_attr_batch_{batch_n}.json",
                    Body=json.dumps(dados_filtrados,
                                    indent=4,
                                    ensure_ascii=False).encode("utf-8")
                    )

                print(f"Batch {batch_n} salvo em {arq_output}")

            except Exception as e:
                print(f"Erro ao salvar o batch {batch_n}: {str(e)}")
                    
        else:
            print(f"Erro: não existem filmes válidos no batch {batch_n}")


###########################################################################
# VARIÁVEIS

# Chaves de Acesso
tmdb_api_token = os.environ.get("TMDB_READ_TOKEN")

# Data Atual
ano, mes, dia = datetime.now().year,\
    f"{datetime.now().month:02}", f"{datetime.now().day:02}"

# Caminhos e Nomes de Arquivos
nome_balde = os.environ.get("BUCKET")
#nome_balde = "compass-desafio-final-dramance"
dataset_base = os.environ.get("BASE_DATASET")
#dataset_base = "./csv/dataset_base_com_elenco.csv"
caminho_output = f"Raw/TMDB/JSON/{ano}/{mes}/{dia}"
log = f"log-ingestao-{ano}{mes}{dia}.txt"

s3 = boto3.resource("s3")
balde = s3.Bucket(nome_balde)

# ID de Filmes: somente IDs distintos
with open(dataset_base, "r", encoding="latin1") as arq:
    reader = csv.reader(arq)
    filmes_id = list({linha[0] for linha in list(reader)[1:]})
    
# Header das Requisições
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_api_token}"
}

# Filtros de Dados
paises_excluidos = [
    "AD",  # Andorra
    "BE",  # Bélgica
    "CA",  # Canadá
    "CH",  # Suiça
    "DE",  # Alemanha
    "DK",  # Dinamarca
    "ES",  # Espanha
    "FI",  # Finlândia
    "FR",  # França
    "GB",  # Reino Unido
    "IE",  # Irlanda
    "IT",  # Itália
    "LU",  # Luxemburgo
    "MC",  # Mônaco
    "NL",  # Países Baixos
    "NO",  # Noruega
    "PT",  # Portugal
    "SE",  # Suécia
    "US",  # Estados Unidos
    "VA",  # Vaticano
    "XI"   # Irlanda do Norte
]

atributos = [
    "imdb_id",
    "original_title",
    "origin_country",
    "original_language",
    "spoken_languages",
    "overview"]

# Reconfiguração do stdout
sys.stdout.reconfigure(encoding="utf-8")
logger = LogPrinter(f"/tmp/{log}")

###########################################################################
# EXECUÇÃO LAMBDA


def lambda_handler(event, context):

    print("Início da sequência de execução de ingestão via API")
    print(f"Iniciando requisições de dados do TMDB")
    processador_api_batch(
        filmes_id=filmes_id,
        headers=headers,
        paises_excluidos=paises_excluidos,
        atributos=atributos,
        s3_bucket=balde,
        tam_batch=100,
        caminho_output=caminho_output
    )

    print(f"Listagem de objetos no bucket {nome_balde}")
    [print(objeto) for objeto in balde.objects.all()]
        
    print("Ingestão realizada com sucesso")
    logger.close()
    balde.upload_file(Filename=f"/tmp/{log}", Key=f"Logs/{log}")
    
    return {
        "statusCode": 200,
        "body": "Processamento e ingestão concluídos."
    }
