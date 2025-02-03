"""Sprint 8 - Desafio Final - Etapa 2: (re)ingestão de dados de API do TMDB.

Autoria: Jaqueline Costa
Data: Jan/25
tmdb_updated_csv_data.py: script com pipeline de requisição de dados
via API e ingestão na camada raw do data lake, novos dados adicionados.

    Outputs / Uploads:
        - filmes_batch_{batch_n}.json: arquivos de dados obtidos
        via API do TMDB, enviados em batches de 100 ao S3 Bucket.
        - tmdb_filmes_selecao_atributos.json: download local de arquivo
        com todos os dados obtidos consolidados.
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
import pandas as pd
import time

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


def tmdb_api_genero_por_anos(
        anos_lancamento: list[int],
        genero_id: int,
        exclusao_chave_valor: tuple[str, str]) -> list[dict]:
    """Função de extração de ids de filmes do TMDB, por gênero e ano(s) de lançamento.
    
        Args:
            - anos_lancamento (list[int]): lista de anos de lançamento para filtrar os filmes
            - genero_id (int): ID do gênero para filtrar os filmes
            - exclusao_chave_valor (tuple[str, str]): tupla com chave e valor para excluir filmes
                
        Returns:
            list[dict]: lista de dicionários contendo IDs e gêneros dos filmes filtrados
    """
    ids_filmes_genero_por_anos = []
    for ano in anos_lancamento:
        pag = 1
        total_pags = 1  # Atualiza-se com nº total de páginas

        while pag <= total_pags:
                try:
                    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&\
                        include_video=false&language=en-US&page={pag}&\
                        primary_release_year={ano}&with_genres={genero_id}"
                    resposta = requests.get(url, headers=headers)

                    if resposta.status_code == 200:
                        dados_tmdb = resposta.json()
                        total_pags = dados_tmdb["total_pages"]
                        print(f"Obtida página {pag} / {total_pags} de filmes de genero_id {genero_id}: ano {ano}.")
                        for filme in dados_tmdb["results"]:
                            if filme[exclusao_chave_valor[0]] != exclusao_chave_valor[1]:
                                ids_filmes_genero_por_anos.append({"id": filme["id"], 
                                                    "genre_ids": filme["genre_ids"]})
                        pag += 1
                    else:
                        print(f"Erro em obter os filmes de ano {ano}. "
                              f"Status: {resposta.status_code}.")
                        break

                except Exception as e:
                    print(f"Erro ao processar filmes: {str(e)}.")
                    continue

                time.sleep(0.25)
    
    print("Sequência de requisições por ano de lançamento e gênero concluída.")
    return ids_filmes_genero_por_anos


def tmdb_api_ids_pais_origem_exclusao(
        filmes_ids: list[int, str],
        paises_excluidos: list[str],
        exclusao_chave_valor: tuple[str, str]) -> list[dict]:
    """Função de filtragem de filmes do TMDB por país de origem.
    
        Args:
            - filmes_ids (list[int, str]): lista de IDs dos filmes a serem filtrados
            - paises_excluidos (list[str]): lista de países a serem excluídos
            - exclusao_chave_valor (tuple[str, str]): tupla com chave e valor para excluir filmes
                
        Returns:
            list[dict]: lista de dicionários contendo dados dos filmes filtrados
    """
    filmes_filtro_paises = []
    for _id in filmes_ids:
        try:
            url = f"https://api.themoviedb.org/3/movie/{_id}?language=en-US"
            resposta = requests.get(url, headers=headers)

            if resposta.status_code == 200:
                dados_tmdb = resposta.json()
                # Verifica condições de exclusão
                if (dados_tmdb["origin_country"][0] not in paises_excluidos
                    and dados_tmdb[exclusao_chave_valor[0]] != exclusao_chave_valor[1]):

                    print(f"Adicionado id: {_id}. "
                          f"Status: {resposta.status_code}.")
                    filmes_filtro_paises.append(dados_tmdb)
                else:
                    print(f"Filme de id {_id} barrado no filtro de países.")

        except Exception as e:
            print(f"Erro ao processar filme de id {_id}: {str(e)}.")
            continue

        time.sleep(0.25)
    
    print("Sequência de requisições por ids e filtro de países concluída.")
    return filmes_filtro_paises


def tmdb_selecao_atributos(
        dados_tmdb: list[dict],
        atributos: list[str]) -> list[dict]:
    """Função de seleção de atributos específicos dos filmes do TMDB.
    
        Args:
            - dados_tmdb (list[dict]): lista de dicionários com dados dos filmes
            - atributos (list[str]): lista de atributos a serem selecionados
                
        Returns:
            list[dict]: lista de dicionários contendo apenas os atributos selecionados
    """
    dados_atributos_final = [{chave: item[chave] 
                              for chave in atributos} for item in dados_tmdb]
    
    print("Seleção de atributos do dataset concluída.")
    return dados_atributos_final


def s3_ingestao_batch(
        filmes: list[dict],
        nome_bucket: str,
        s3_bucket: object,
        tam_batch: int = 100,
        caminho_output: str = "./api_data") -> None:
    """Upload em batch de registros em JSON em bucket AWS S3.

        Args:
            filmes (list[dict]): lista em formato JSON com dados de filmes
            s3_bucket (object): AWS S3 bucket, objeto Bucket
            tam_batch (int): número de IDs processados por batch
                default: 100
            caminho_output (str): saída para os arquivos JSON
                default: ./api_data
    """
    # Calcula o número total de batches
    total_batches = ceil(len(filmes) / tam_batch)

    for batch_n in range(total_batches):
        inicio = batch_n * tam_batch
        fim = min(inicio + tam_batch, len(filmes))
        batch_n += 1

        # Processa o batch atual
        batch_atual = filmes[inicio:fim]

        print(f"Processando batch {batch_n}/{total_batches} para upload no bucket {nome_bucket}"
              f"(IDs {inicio} até {fim}).")

        if batch_atual:
            try:
                s3_bucket.put_object(
                    Key=f"{caminho_output}/filmes_batch_{batch_n}.json",
                    Body=json.dumps(batch_atual,
                                    indent=4,
                                    ensure_ascii=False).encode("utf-8")
                    )

                print(f"Batch {batch_n} salvo no bucket \
                    {nome_bucket} em {caminho_output}.")

            except Exception as e:
                print(f"Erro ao salvar o batch {batch_n} no bucket {nome_bucket}: {str(e)}.")

        else:
            print(f"Erro: não existem filmes válidos no batch {batch_n}.")
    
    print("Ingestão em batch de arquivos JSON finalizada."
          f"Listagem de objetos no bucket {nome_bucket}: ")
    [print(objeto) for objeto in s3_bucket.objects.all()]


###########################################################################
# VARIÁVEIS

# Chaves de Acesso
tmdb_api_token = os.environ.get("TMDB_READ_TOKEN")
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.environ.get("AWS_SESSION_TOKEN")

# Data Atual
ano, mes, dia = datetime.now().year,\
    f"{datetime.now().month:02}", f"{datetime.now().day:02}"

# Caminhos e Nomes de Arquivos
# nome_balde = os.environ.get("BUCKET_NAME")
nome_balde = "compass-desafio-final-dramance"
# dataset_base = os.environ.get("DATASET_REF")
dataset_base = "../../sprint7/desafio/csv/ids_distintos_attr_em_ingles.csv"
caminho_output = f"Raw/TMDB/JSON/{ano}/{mes}/{dia}"
log = f"log-ingestao-{ano}{mes}{dia}.txt"

# Integração AWS
s3 = boto3.resource(#
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)
balde = s3.Bucket(nome_balde)

# ID de Filmes: somente IDs distintos
with open(dataset_base, "r", encoding="latin1") as arq:
    reader = csv.reader(arq)
    filmes_csv_ids = list({linha[0] for linha in list(reader)[1:]})

# Header das Requisições
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_api_token}"
}

# Filtros de Dados
paises_excluidos = [
    "AD",  # Andorra
    "BE",  # Bélgica
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
    "id",
    "imdb_id",
    "title",
    "original_title",
    "origin_country",
    "original_language",
    "spoken_languages",
    "release_date",
    "popularity",
    "vote_average",
    "vote_count",
    "overview"
    ]

anos_lancamento = (2023, 2024, 2025)
romance_id = 10749

# Reconfiguração do stdout
sys.stdout.reconfigure(encoding="utf-8")
logger = LogPrinter(f"{log}")

###########################################################################
# EXECUÇÃO REQUISIÇÕES


def lambda_handler(event, context):
    """Função de execução event-driven na Lambda."""

    print("Início da sequência de execução de ingestão via API")
    print("Iniciando requisições de dados do TMDB")

    print("Início da sequência de execução de ingestão via API.")
    print("Iniciando requisições de dados de filmes de anos atuais do TMDB.")

    filmes_atuais = tmdb_api_genero_por_anos(
        anos_lancamento=anos_lancamento,
        genero_id=romance_id,
        exclusao_chave_valor=("original_language", "en")
    )

    print("Requisições por gênero e anos de lançamento finalizadas.")
    print("Iniciando filtro de gênero único de Romance.")

    filmes_atuais_df = pd.DataFrame.from_dict(filmes_atuais)
    romances_atuais_df = filmes_atuais_df[filmes_atuais_df["genre_ids"]
                                          .apply(lambda x: len(x) == 1 and romance_id in x)]

    print("Removendo duplicações de filmes atuais.")
    
    romances_atuais_sem_dup_df = romances_atuais_df.drop_duplicates(subset="id")

    print(f"Dataset de filmes atuais de Romance com {romances_atuais_sem_dup_df.shape[0]} linhas.")

    romances_atuais_dados_totais = tmdb_api_ids_pais_origem_exclusao(
        filmes_ids=romances_atuais_sem_dup_df["id"],
        paises_excluidos=paises_excluidos,
        exclusao_chave_valor=("original_language", "en")
    )

    romances_atuais_final = tmdb_selecao_atributos(
        dados_tmdb=romances_atuais_dados_totais,
        atributos=atributos
    )

    romances_csv_dados_totais = tmdb_api_ids_pais_origem_exclusao(
        filmes_ids=filmes_csv_ids,
        paises_excluidos=paises_excluidos,
        exclusao_chave_valor=("original_language", "en")
    )

    romances_csv_final = tmdb_selecao_atributos(
        dados_tmdb=romances_csv_dados_totais,
        atributos=atributos
    )

    romances_final = romances_csv_final + romances_atuais_final
    pd.DataFrame(romances_final).to_json(
        "tmdb_filmes_selecao_atributos.json",
        orient="records",
        force_ascii=False,
        indent=4
    )

    print("Download local de arquivo consolidado em JSON.")

    s3_ingestao_batch(
        filmes=romances_final,
        nome_bucket=nome_balde,
        s3_bucket=balde,
        tam_batch=100,
        caminho_output=caminho_output
    )

    print("Ingestão de API TMDB para bucket S3 realizada com sucesso !")

    logger.close()
    balde.upload_file(Filename=f"{log}", Key=f"Logs/{log}")

    return {
        "statusCode": 200,
        "body": "Processamento e (re)ingestão na camada Raw TMDB concluídos."
    }
