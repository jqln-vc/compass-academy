"""Sprint 5 - Desafio Dados Gov: análise de dados integrada ao AWS S3.
Autoria: Jaqueline Costa
Data: Dez/24

analise.py: script de manipulação e análise de dados, é executado a partir
do script etl.py, recebendo o dataset consolidado após concatenação de
datasets anuais.

Os datasets utilizados foram disponibilizados pela ANCINE, referem-se à 
produção audiovisual não-publicitária com registro CPB (Certificado de 
Produto Brasileiro), em período anual. 
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
output = 'analise.csv'
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
# SEQUÊNCIA DE MANIPULAÇÕES E OUTPUT DE ANÁLISE FINAL
#

# TRATAMENTO DE STRINGS

# Renomeando colunas
df.columns = colunas

# Tratamento das strings das colunas de interesse
df['Tipo da Obra'] = df['Tipo da Obra'].str.title()
df['Subtipo da Obra'] = df['Subtipo da Obra'].str.title()
df['Segmento de Destinação'] = df['Segmento de Destinação'].str.title()


# TRATAMENTO DE DATA

# Conversão da coluna para datetime
df['Data de Emissão do CPB'] = pd.to_datetime(
    df['Data de Emissão do CPB'], 
    dayfirst=True,  # Indica o padrão original DD/MM/YYYY
    errors='coerce')


# CONVERSÃO PARA FLOAT

df['Duração Total (Minutos)'] = df['Duração Total (Minutos)'].str\
                                    .replace(',', '.').astype(float)


# FILTRO COM ATRIBUTOS DE DATA, CONDICIONAIS & OPERADORES LÓGICOS

# Condicionais de intervalo de tempo
# Dois operadores lógicos AND
# Condicional de exclusão de seriados e curta metragens
df = df[(df['Data de Emissão do CPB'].dt.year >= 2020) & 
        (df['Data de Emissão do CPB'].dt.year <= 2022) & 
        (df['Organização Temporal'] == 'NÃO SERIADA') &
        (df['Duração Total (Minutos)'] >= 60)]


# AGREGAÇÕES COM GROUPBY & COUNT

# Contagem por agrupamento de colunas
df = df.groupby([
    'Tipo da Obra',
    'Subtipo da Obra',
    'Segmento de Destinação'
])['CPB']\
    .count()\
    .reset_index(name='Qtd de Filmes')

df = df.loc[df['Qtd de Filmes'] == df['Qtd de Filmes'].max()]

# EXPORTAÇÃO DA ANÁLISE EM CSV

df.to_csv(output, sep=',', index=False, encoding='utf-8')
