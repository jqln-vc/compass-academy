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

import polars as pl

##############################################################################
# VARIÁVEIS
#

dataset = 'dataset.csv'
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

# Leitura do CSV com as colunas especificadas
df = pl.read_csv(dataset, separator=';', encoding='utf-8')
df.columns = colunas

# Transformações usando expressões Polars
df = df.with_columns([
    # Tratamento de strings
    pl.col('Tipo da Obra').str.to_titlecase(),
    pl.col('Subtipo da Obra').str.to_titlecase(),
    pl.col('Segmento de Destinação').str.to_titlecase(),
    
    # Conversão da coluna de data
    pl.col('Data de Emissão do CPB').str.strptime(pl.Date, format='%d/%m/%Y'),
    
    # Conversão da duração para float
    pl.col('Duração Total (Minutos)').str.replace(',', '.').cast(pl.Float64)
])

# Aplicação dos filtros
df = df.filter(
    (pl.col('Data de Emissão do CPB').dt.year() >= 2020) &
    (pl.col('Data de Emissão do CPB').dt.year() <= 2022) &
    (pl.col('Organização Temporal') == 'NÃO SERIADA') &
    (pl.col('Duração Total (Minutos)') >= 60)
)

# Agregação e contagem
df = df.group_by([
    'Tipo da Obra',
    'Subtipo da Obra',
    'Segmento de Destinação'
]).agg([
    pl.col('CPB').count().alias('Qtd de Filmes')
]).sort('Qtd de Filmes', descending=True)

# Filtrar apenas a linha com o maior valor de 'Qtd de Filmes'
df = df.filter(pl.col('Qtd de Filmes') == pl.col('Qtd de Filmes').max())

# Exportação para CSV
df.write_csv(output, separator=',')



class LogPrinter:
    """Classe para direcionar o stdout para arquivo de log."""
    def __init__(self, nome_arquivo: str):
        """Construtor: acessa o arquivo e terminal."""
        self.arquivo = open(nome_arquivo, 'a')
        self.terminal = sys.__stdout__

    def write(self, dados):
        """Faz a escrita dos dados no terminal e arquivo."""
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        registro = f"[{timestamp}] {dados}"
        
        self.terminal.write(registro)
        self.arquivo.write(registro)

    def flush(self):
        """Força a escrita do buffer no terminal e arquivo."""
        self.terminal.flush()
        self.arquivo.flush()

    def close(self):
        """Fecha o arquivo após o uso."""
        self.arquivo.close()