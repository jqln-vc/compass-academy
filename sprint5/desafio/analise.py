"""
"""

##############################################################################
# IMPORTAÇÕES DE MÓDULOS E BIBLIOTECAS
#

import pandas as pd

##############################################################################
# VARIÁVEIS
#

dataset = 'dataset.csv'
df = pd.read_csv(dataset, delimiter=';', encoding='utf-8')
colunas = ['Título Original',
           'CPB',
           'Data de Emissão do CPB',
           'Situação da Obra',
           'Tipo da Obra',
           'Subtipo da Obra',
           'Classificação da Obra',
           'Organização Temporal',
           'Duração Total (Minutos)',
           'Quantidade de Episódios',
           'Ano de Produção Inicial',
           'Ano de Produção Final',
           'Segmento de Destinação',
           'Coprodução Internacional',
           'Requerente',
           'CNPJ do Requerente',
           'UF do Requerente',
           'Município do Requerente']

##############################################################################
# SEQUÊNCIA DE ANÁLISES
#

# TRATAMENTO DE STRINGS E CONVERSÕES DE DATA, INT E FLOAT
df.columns = colunas

df['Tipo da Obra'] = df['Tipo da Obra'].str.title()
df['Subtipo da Obra'] = df['Subtipo da Obra'].str.title()
df['Segmento de Destinação'] = df['Segmento de Destinação'].str.title()


df['Data de Emissão do CPB'] = pd.to_datetime(
    df['Data de Emissão do CPB'], 
    dayfirst=True, 
    errors='coerce')

df['Ano de Produção Inicial'] = df['Ano de Produção Inicial'].fillna(0).astype(int)
df['Ano de Produção Final'] = df['Ano de Produção Final'].fillna(0).astype(int)
df['Duração Total (Minutos)'] = df['Duração Total (Minutos)'].str.replace(',', '.').astype(float)


# FILTRO COM ATRIBUTOS DE DATA, CONDICIONAIS E OPERADORES LÓGICOS

df = df[(df['Data de Emissão do CPB'].dt.year >= 2020) & 
        (df['Data de Emissão do CPB'].dt.year <= 2022) & 
        (df['Organização Temporal'] == 'NÃO SERIADA')]

# AGREGAÇÕES COM GROUPBY, COUNT E ORDENAÇÃO DESCENDENTE

df = df.groupby([
    'Tipo da Obra',
    'Subtipo da Obra',
    'Segmento de Destinação'
])['CPB']\
    .count()\
    .reset_index(name='Qtd de Filmes')\
    .sort_values(by='Qtd de Filmes', ascending=False)

# EXPORTAÇÃO DA ANÁLISE EM CSV
df.to_csv('analise.csv', sep=',', index=False, encoding='utf-8')
