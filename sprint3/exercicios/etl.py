"""
Actors ETL Pipeline: Script para processamento de dados do arquivo 'actors.csv'.
Autoria: Jaqueline Costa
Data: Nov / 2024
"""
#########################################################################################
#
# VARIÁVEIS GLOBAIS
#

# Arquivo dos Dados Input

INPUT_ACTORS = r'./actors.csv'

# Arquivos de Dados de Output por Etapa

OUTPUT1 = r'etl-etapa1.txt'
OUTPUT2 = r'etl-etapa2.txt'
OUTPUT3 = r'etl-etapa3.txt'
OUTPUT4 = r'etl-etapa4.txt'
OUTPUT5 = r'etl-etapa5.txt'

#########################################################################################
#
# FUNÇÕES
#

# Função: Parser de CSV

def parser_csv(linha: str) -> list[str]:
    """
        Parser CSV: trata uma linha de um arquivo CSV, 
        identificando e tratando valores com vírgulas.
        
        Args:
            linha (str): uma string correspondente a uma linha do arquivo CSV.
        
        Returns:
            list[str]: uma lista de strings com os valores de cada campo da linha.
            
        É necessário utilizar esta função dentro de um loop, invocando a função
        a cada linha do arquivo.
    """

    linha_processada = []
    coluna_atual = ""
    aspas_duplas = False

    for caractere in linha:
        if caractere == '"': 
            aspas_duplas = not aspas_duplas  # Indicador de aspas duplas (se True, ignora vírgulas)
            coluna_atual += caractere
        elif caractere == ',' and not aspas_duplas:  # Confere se vírgula está fora de aspas duplas
            linha_processada.append(coluna_atual.strip())  # Adiciona uma coluna da linha
            coluna_atual = ""
        else:
            coluna_atual += caractere  # Acumulador de caracteres de uma coluna

    linha_processada.append(coluna_atual.strip())  # Adiciona a última coluna
    
    return linha_processada


# Função: Extração de Dados

def extracao_dados(arquivo: str, 
                   parser: callable, 
                   schema: bool = True) -> tuple[list, list[list[str]]]:
    """
        Extração de Dados: lê um arquivo, faz o tratamento com um parser
        e retorna os dados, com o schema de colunas em uma lista separada.
        
        Args:
            arquivo (str): caminho do arquivo de entrada.
            parser (callable): função de parser para processar cada linha.
            schema (bool, optional): indica se o arquivo possui schema de colunas.
               - True (default): 1ª linha tratada como schema.
               - False: 1ª linha tratada como dados.

        Returns:
            Se schema=True:
            
                tuple[list, list[list[str]]]: uma tupla contendo
                    - lista com o schema de colunas
                    - lista de listas, cada qual contendo uma linha do arquivo
                    separada em colunas (strings).
                    
            Se schema=False:
            
                list[list[str]]: uma lista contendo
                    - listas, cada qual contendo uma linha do arquivo
                    separada em colunas (strings).            
    """
    
    with open(arquivo, 'r', encoding='utf-8') as arquivo:
        dados = [parser(linha) for linha in arquivo.read().splitlines()]
    
    return (dados.pop(0), dados) if schema else dados

# Função: Conversor de Tipos

def conversor_tipos(dados: list[list[str]], tipos: tuple[callable]) -> list[tuple]:
    """
        Conversor de Tipos: converte os tipos de dados de uma lista de listas de strings.
        
        Args:
            dados (list[list[str]]): lista de listas de strings.
            tipos (tuple[callable]): tupla de funções de conversão.

        Returns:
            list[tuple]: lista de tuplas com os dados convertidos.

        Raises:
            ValueError: 
                - se dados ou tipos vazios.
                - se a quantidade de tipos não for equivalente às colunas.
    """

    if not(len(dados) or len(tipos)):
        return ValueError("Dados ou tipos vazios.")
    elif len(dados[0]) != len(tipos):
        return ValueError("A quantidade de tipos deve ser equivalente às colunas.")
    else:
        return [tuple(tipo(coluna) for tipo, coluna in zip(tipos, linha)) for linha in dados]


#########################################################################################
#
# EXTRAÇÃO DE DADOS
#

colunas, actors = extracao_dados(INPUT_ACTORS, parser_csv)

#########################################################################################
#
# TRATAMENTO DE DADOS
#

tipos = (str,       # Actor
         float,     # Total Gross 
         int,       # Number of Movies
         float,     # Average per Movie
         str,       # #1 Movie
         float)     # Gross

actors = conversor_tipos(actors, tipos)

#########################################################################################
#
# PROCESSAMENTO DOS DADOS E GERAÇÃO DE ARQUIVOS DE OUTPUT
#

# Etapa 1: Apresentar o ator/atriz com maior número de filmes e a respectiva quantidade. 
# A quantidade de filmes encontra-se na coluna 'Number of Movies'.

# Etapa 2: Apresentar a média de receita (coluna 'Gross') de bilheteria bruta dos 
# principais filmes, considerando todos os atores.

# Etapa 3: Apresentar o ator/atriz com a maior média de receita de bilheteria bruta 
# por filme do conjunto de linha_processada. Considerar a coluna 'Average per Movie'.

# Etapa 4: A coluna '#1 Movie' contém o filme de maior bilheteria em que o ator atuou. 
# Realizar a contagem de aparições destes filmes no dataset, listando-os ordenados 
# pela quantidade de vezes em que estão presentes. 
# Considerar a ordem decrescente e, em segundo nível, o nome do filme. 
#
# Ao escrever no arquivo, considerar o padrão de saída 
# '(sequencia) - O filme (nome) aparece (quantidade) vez(es) no dataset', 
# adicionando um resultado por linha.

# Etapa 5: Apresentar a lista dos atores ordenada pela receita bruta de bilheteria 
# de seus filmes (coluna 'Total Gross'), em ordem decrescente. 
#
# Ao escrever no arquivo,  considerar o padrão de saída
# '(nome do ator) - (receita total bruta)', adicionando um resultado por linha.
