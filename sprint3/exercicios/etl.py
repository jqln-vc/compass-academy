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

# INPUT_ACTORS = r'./actors.csv'
INPUT_ACTORS = r'actors.csv'

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
            # coluna_atual += caractere
            continue
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
        raise ValueError("Dados ou tipos vazios.")
    elif len(dados[0]) != len(tipos):
        raise ValueError("A quantidade de tipos deve ser equivalente às colunas.")
    else:
        return [tuple(tipo(coluna) for tipo, coluna in zip(tipos, linha)) for linha in dados]

# Função: Maior Valor de uma Coluna

def max_coluna(dados: list[tuple], coluna: int) -> tuple:
    """
        Máximo de uma Coluna: retorna a linha com maior valor de uma coluna.

        Args:
            dados (list[tuple]): lista de tuplas.
            coluna (int): índice da coluna.

        Returns:
            tuple: tupla correspondente à linha com o maior valor na coluna.

        Raises:
            ValueError:
                - se dados vazio.
                - se coluna inválida.
    """

    if not(len(dados)):
        raise ValueError("Dados vazios.")
    elif coluna < 0 or coluna >= len(dados[0]):
        raise ValueError("Coluna inválida.")
    else:
        return max(dados, key=lambda linha: linha[coluna])

# Função: Média de uma Coluna

def media_coluna(dados: list[tuple], coluna: int) -> tuple[int, float]:
    """
        Média de uma Coluna: retorna a média dos valores de uma coluna.

        Args:
            dados (list[tuple]): lista de tuplas.
            coluna (int): índice da coluna.

        Returns:
            tuple[int, float]: tupla contendo o índice da coluna e o valor médio.

        Raises:
            ValueError:
                - se dados vazio.
                - se coluna inválida.
    """

    if not(len(dados)):
        raise ValueError("Dados vazios.")
    elif coluna < 0 or coluna >= len(dados[0]):
        raise ValueError("Coluna inválida.")
    else:
        return (coluna, sum(linha[coluna] for linha in dados) / len(dados))

# Função: Frequência de Coluna

def frequencia_coluna(dados: list[tuple], coluna: int) -> dict:
    """
        Frequência de Coluna: contagem de ocorrências de cada valor na coluna.

        Args:
            dados (list[tuple]): lista de tuplas.
            coluna (int): índice da coluna.

        Returns:
            dict: dicionário com a contagem de ocorrências de cada valor na coluna.

        Raises:
            ValueError:
                - se dados vazio.
                - se coluna inválida.
    """

    if not(len(dados)):
        raise ValueError("Dados vazios.")
    elif coluna < 0 or coluna >= len(dados[0]):
        raise ValueError("Coluna inválida.")
    else:
        contagem = {}
        for linha in dados:
            valor = linha[coluna]
            contagem[valor] = contagem.get(valor, 0) + 1
        
        contagem_ordenada = dict(sorted(contagem.items(), key=lambda item: (-item[1], item[0])))
        return contagem_ordenada

# Função: Coluna Decrescente

def coluna_decrescente(dados: list[tuple], coluna: int) -> list[tuple]:
    """
        Coluna Decrescente: retorna os dados ordenados pela coluna em ordem decrescente.

        Args:
            dados (list[tuple]): lista de tuplas.
            coluna (int): índice da coluna.

        Returns:
            list[tuple]: lista de tuplas ordenada pela coluna em ordem decrescente.

        Raises:
            ValueError:
                - se dados vazio.
                - se coluna inválida.
    """

    if not(len(dados)):
        raise ValueError("Dados vazios.")
    elif coluna < 0 or coluna >= len(dados[0]):
        raise ValueError("Coluna inválida.")
    else:
        return sorted(dados, key=lambda linha: linha[coluna], reverse=True)

# Função: Escrever Dados

def escrever_dados(
        arquivo_saida: str,
        dados: list[tuple],
        funcao: callable,
        funcao_params: tuple = None,
        padrao_saida: str = None,
        padrao_params: tuple = None,
        indexacao: bool = False
    ) -> None:
    """
    Escrever Dados: escreve os dados em um arquivo de saída.
        Recebe uma função para processar os dados antes de escrever.
        Recebe um padrão de saída para cada linha (opcional).

    Args:
        arquivo_saida (str): caminho/nome do arquivo de saída.
        dados (list[tuple]): lista de tuplas.
        funcao (callable): função para processar os dados.
        funcao_params (tuple, optional): parâmetros adicionais da função.
           - None (default): não há parâmetros, serão passados os dados.
           - tuple: parâmetros da função.
        padrao_saida (str, optional): padrão de saída para cada linha.
           - None (default): não há padrão de saída.
           - str: padrão de saída para cada linha.
        padrao_params (tuple, optional): indexes para selecionar o conteúdo do padrão de saída.
        indexacao (bool, optional): indica se deve ser incluído um índice no arquivo de output.
           - False (default): não incluir índice.
           - True: incluir índice.

    Returns:
        None

    Raises:
        ValueError:
            - se dados vazio.
            - se função inválida.
    """
    if not dados or not callable(funcao):
        raise ValueError("Dados ou função inválidos.")
    
    # Processando os dados com a função passada como parâmetro
    dados_processados = (
        funcao(dados, *funcao_params) if funcao_params else funcao(dados)
    )

    with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
        
        # Garantindo que dados_processados é iterável
        if isinstance(dados_processados, tuple) and not isinstance(dados_processados[0], tuple):
            dados_processados = [dados_processados]
            
        dados_processados = (
            dados_processados.items() 
            if isinstance(dados_processados, dict) 
            else dados_processados
        )
        
        for index, linha in enumerate(dados_processados):
            if padrao_saida and padrao_params:
                # Acessando o valor dos indexes passados como parâmetros para o padrão de saída
                valores = tuple(linha[idx] for idx in padrao_params)
                linha_formatada = (
                    padrao_saida.format(index + 1, *valores)
                    if indexacao
                    else padrao_saida.format(*valores)
                )
            else:
                linha_formatada = f"{index + 1} - {str(linha)}"
        
            arquivo.write(linha_formatada + "\n")

    print(f"Dados escritos em {arquivo_saida}")


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
# PROCESSAMENTO DOS DADOS E OUTPUT DE ANÁLISES
#
# Etapa 1: 
# Apresentar o ator/atriz com maior número de filmes e a respectiva quantidade. 
# A quantidade de filmes encontra-se na coluna 'Number of Movies'.

padrao_saida_output1 = 'Ator/Atriz: {0} - Top "Number of Movies": {1}'
escrever_dados(OUTPUT1, actors, max_coluna, (2,), padrao_saida_output1, (0, 2))

# Etapa 2: 
# Apresentar a média de receita (coluna 'Gross') de bilheteria bruta dos 
# principais filmes, considerando todos os atores.

padrao_saida_output2 = 'Média de receita dos principais filmes: {0}'
escrever_dados(OUTPUT2, actors, media_coluna, (5, ), padrao_saida_output2, (1, ))

# Etapa 3: 
# Apresentar o ator/atriz com a maior média de receita de bilheteria bruta 
# por filme do conjunto de dados. Considerar a coluna 'Average per Movie'.

padrao_saida_output3 = 'Ator/Atriz: {0} - Top "Average per Movie": {1}'
escrever_dados(OUTPUT3, actors, max_coluna, (3,), padrao_saida_output3, (0, 3))

# Etapa 4: 
# A coluna '#1 Movie' contém o filme de maior bilheteria em que o ator atuou. 
# Realizar a contagem de aparições destes filmes no dataset, listando-os ordenados 
# pela quantidade de vezes em que estão presentes. 
# Considerar a ordem decrescente e, em segundo nível, o nome do filme. 
#
# Ao escrever no arquivo, considerar o padrão de saída 
# '(sequencia) - O filme (nome) aparece (quantidade) vez(es) no dataset', 
# adicionando um resultado por linha.

padrao_saida_output4 = '{0} - O filme {1} aparece {2} vez(es) no dataset'
escrever_dados(OUTPUT4, actors, frequencia_coluna, (4, ), padrao_saida_output4, (0, 1), indexacao=True)

# Etapa 5: 
# Apresentar a lista dos atores ordenada pela receita bruta de bilheteria 
# de seus filmes (coluna 'Total Gross'), em ordem decrescente. 
#
# Ao escrever no arquivo,  considerar o padrão de saída
# '(nome do ator) - (receita total bruta)', adicionando um resultado por linha.

padrao_saida_output5 = '{0} - {1}'
escrever_dados(OUTPUT5, actors, coluna_decrescente, (1,), padrao_saida_output5, (0, 1))