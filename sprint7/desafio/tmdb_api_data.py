""""""


#########################################################################
# IMPORTAÇÕES

import json
import csv
import requests
import os
import time
import boto3
from math import ceil

#########################################################################
# CLASSES E FUNÇÕES

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


def processador_api_batch(filmes_id: list[str],
                          headers: dict,
                          paises_excluidos: list[str],
                          atributos: list[str],
                          tam_batch: int = 100,
                          caminho_output: str = './api_data'
                          ) -> None:
    """
    Processador de requisição de filmes por ID em batch, output em JSON.
        
    Args:
        filmes_id (list[str]): IDs de filmes para processar
        headers (dict): headers do request da API
        paises_excluidos (list[str]): países para exclusão
        atributos (list[str]): atributos a salvar no arquivo JSON
        tam_batch (int): número de IDs processados por batch
            default: 100
        caminho_output (str): diretório de saída para os arquivos JSON
            default: ./api_data
    """
    # Calcula o número total de batches
    total_batches = ceil(len(filmes_id) / tam_batch)
        
    for batch_num in range(total_batches):
        inicio = batch_num * tam_batch
        fim = min(inicio + tam_batch, len(filmes_id))
            
        # Processa o batch atual
        dados = []
        batch_atual = filmes_id[inicio:fim]
            
        print(f"Processando batch {batch_num + 1}/{total_batches} (IDs {inicio} to {fim})")
            
        for _id in batch_atual:
            try:
                url = f"https://api.themoviedb.org/3/movie/{_id}?language=en-US"
                resposta = requests.get(url, headers=headers)
                    
                if resposta.status_code == 200:
                    dados_tmdb = resposta.json()
                        
                    # Verifica condições de exclusão
                    if (dados_tmdb['origin_country'][0] not in paises_excluidos and 
                        dados_tmdb['original_language'] != 'en'):
                            
                        print(f"Adicionado id: {_id}")
                        dados.append(dados_tmdb)
                else:
                    print(f"Falha em obter o filme de id: {_id}. Status: {resposta.status_code}")
                    
                # Temporizador de espera, entre requests
                time.sleep(1)
                    
            except Exception as e:
                print(f"Erro ao processar filme de id {_id}: {str(e)}")
                continue
            
        # Filtrar atributos e salvar o batch em json
        if dados:
            dados_filtrados = [{chave: item[chave] for chave in atributos} for item in dados]
                
            arq_output = f'{caminho_output}/filmes_attr_batch_{batch_num + 1}.json'
            try:
                with open(arq_output, 'w', encoding='utf-8') as arqjson:
                    json.dump(dados_filtrados, arqjson, indent=4, ensure_ascii=False)
                print(f"Batch {batch_num + 1} salvo em {arq_output}")
            except Exception as e:
                print(f"Erro ao salvar o batch {batch_num + 1}: {str(e)}")
                    
        else:
            print(f"Não existem filmes válidos no batch {batch_num + 1}")


#########################################################################
# VARIÁVEIS

# Chaves de Acesso
tmdb_api_token = os.environ.get('TMDB_READ_TOKEN')

# Data Atual
ano, mes, dia = datetime.now().year,\
    f"{datetime.now().month:02}", f"{datetime.now().day:02}"

# ID de Filmes
with open('filmes_attr_is_english.csv', 'r', encoding='latin1') as arq:
    reader = csv.reader(arq)
    filmes_id = [row[0] for row in list(reader)[1:200]]
    
# Header das Requisições
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_api_token}"
}

# Filtros de Dados 
paises_excluidos = [
    "BE",
    "CH",
    "DE",
    "DK",
    "ES",
    "FI",
    "FR",
    "GB",
    "IE",
    "IT",
    "LU",
    "MC",
    "MT",
    "NL",
    "NO",
    "PT",
    "SE",
    "US"
]

atributos = ["imdb_id",
             "origin_country",
             "original_language",
             "original_title",
             "overview",
             "spoken_languages"]

# Caminhos e Nomes de Arquivos
nome_balde = "compass-desafio-final-dramance"
log = f'log-ingestao-{ano}{mes}{dia}.txt'

# Reconfiguração do stdout
logger = LogPrinter(log)

###############################################################
# EXECUÇÃO


processador_api_batch(
    filmes_id=filmes_id,
    headers=headers,
    paises_excluidos=paises_excluidos,
    atributos=atributos,
    tam_batch=100,
    caminho_output='./api_data'
)
