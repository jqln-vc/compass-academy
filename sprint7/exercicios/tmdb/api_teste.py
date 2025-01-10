
#################################################################
# IMPORTAÇÕES

import os
import requests
import pandas as pd
from IPython.display import display

#################################################################
# VARIÁVEIS

# Chave de Acesso
api_key = os.getenv("TMDB_API_KEY")

# Caminho da URL com Query
base_url = "https://api.themoviedb.org/3"
endpoint = "/movie/top_rated"
url = f"{base_url}{endpoint}"

# Parâmetros da Query
params = {
    "api_key": api_key,
    "language": "pt-BR",
    "page": 2
}

#################################################################
# REQUISIÇÃO E TRATAMENTO DE RESPOSTA DA API

resposta = requests.get(url, params=params)

filmes = []

# Verificando o status da resposta
if resposta.status_code == 200:
    for filme in resposta.json()["results"]:
        df = {
            'Título': filme['title'],
            'Data de Lançamento': filme['release_date'],
            'Sinopse': filme['overview'],
            'Quantidade de Avaliações': filme['vote_count'],
            'Nota Média': filme['vote_average']
        }

        filmes.append(df)
    df = pd.DataFrame(filmes)
    display(df)
    print(resposta.json()["results"][0])

# Caso não tenha obtido sucesso na requisição
else:
    print(f"Erro: {resposta.status_code}, {resposta.text}")
