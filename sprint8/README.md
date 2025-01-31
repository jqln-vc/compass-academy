#

||
|---|
|![Banner](/assets/banner-sprint8.png)|
||

## RELATOS DE APRENDIZADO

## EXERCÍCIOS

Todos os códigos dos exercícios foram implementados seguindo os Python Enhancement Proposal, especificamente as recomendações de estilo do PEP8 e convenções de docstrings do PEP257, indicados na seção [Bibliografia](#bibliografia), com validação no [*CodeWOF: Python 3 Style Checker*](https://www.codewof.co.nz/style/python3/) online.

Na pasta `evidencias/exercicios`, estão localizadas as imagens com a validação de cada exercício.

* **Gerador em Massa de Dados** : utilização de aleatoriedade para geração de dados em massa.
  * [**gerador_dados.py**](./exercicios/spark_batch/gerador_dados.py) : script que gera 2 arquivos de dados aleatórios de animais e nomes de pessoas.
    * [**nomes_animais.csv**](./exercicios/spark_batch/nomes_animais.csv) : arquivo CSV com nomes de animais ordenados em ordem alfabética.
    * [**nomes_aleatorios.txt**](./exercicios/spark_batch/nomes_aleatorios.txt) : arquivo TXT com quantidade massiva de nomes gerados aleatoriamente.

* **Lab Spark SQL** : utilização do framework PySpark para manipulação e análise de alto volume de dados, a partir do arquivo `nomes_aleatorios.txt` gerado no exercício acima.
  * [**lab_spark_sql.py**](./exercicios/spark_batch/lab_spark_sql.py) : script de execução das sequência de manipulações e análises solicitados.

* **API TMDB | Teste de Acesso** : obtenção de dados do database TMDB por meio de API.
  * [**api_teste.py**](./exercicios/tmdb/api_teste.py)

## DESAFIO

O projeto final desenvolve um fluxo de processamento e análise de dados, a partir de uma arquitetura data lake. Para a terceira etapa

## EVIDÊNCIAS

Na pasta `evidencias`, encontram-se prints referentes a momentos de execução, exemplificando abordagens adotadas para o desenvolvimento dos exercícios e do desafio.  
No passo a passo explicativo, encontrado na pasta `desafio`, serão comentados outros prints de pontos específicos.

### GERADOR EM MASSA DE DADOS

#### ETAPA 1: NÚMEROS ALEATÓRIOS

![Etapa 1](./evidencias/exercicios/2-gerador-etapa1.png)

#### ETAPA 2: LISTA DE ANIMAIS

![Etapa 2](./evidencias/exercicios/3-gerador-etapa2.png)

#### ETAPA 3: NOMES ALEATÓRIOS

![Etapa 3](./evidencias/exercicios/4-gerador-etapa3.png)

### APACHE SPARK

#### ETAPA 1: CRIAÇÃO DA SESSÃO E DO DATAFRAME

![Etapa 1](./evidencias/exercicios/5-lab-spark-etapa1.png)

#### ETAPA 2: RENOMEAÇÃO PARA COLUNA "NOMES" E VERIFICAÇÃO DO SCHEMA

![Etapa 2](./evidencias/exercicios/6-lab-spark-etapa2.png)

#### ETAPA 3: CRIAÇÃO DA COLUNA "ESCOLARIDADE"

![Etapa 3](./evidencias/exercicios/7-lab-spark-etapa3.png)

#### ETAPA 4: CRIAÇÃO DA COLUNA "PAÍS"

![Etapa 4](./evidencias/exercicios/8-lab-spark-etapa4.png)

#### ETAPA 5: CRIAÇÃO DA COLUNA "ANONASCIMENTO" (1946 ~ 2010)

![Etapa 5](./evidencias/exercicios/9-lab-spark-etapa5.png)

#### ETAPA 6: SELECT DE PESSOAS NASCIDAS NESTE SÉCULO

![Etapa 6](./evidencias/exercicios/10-lab-spark-etapa6.png)

#### ETAPA 7: SELECT DA ETAPA 6 COM SPARK SQL

![Etapa 7](./evidencias/exercicios/11-lab-spark-etapa7.png)

#### ETAPA 8: CONTAGEM DE MILLENNIALS (1980 ~ 1994) COM FILTER

![Etapa 8](./evidencias/exercicios/12-lab-spark-etapa8.png)

#### ETAPA 9: CONTAGEM DA ETAPA 8 COM SPARK SQL

![Etapa 9](./evidencias/exercicios/13-lab-spark-etapa9.png)

#### ETAPA 10: QUANTIDADE DE PESSOAS POR PAÍS E GERAÇÃO

![Etapa 10](./evidencias/exercicios/14-lab-spark-etapa10.png)

#### EXECUÇÃO COMPLETA DO SCRIPT

![Execução Lab Spark](./evidencias/exercicios/15-execucao-lab-spark-script.gif)

### API TMDB

![Script Dados API](./evidencias/exercicios/1-tmdb-filmes.png)

## CERTIFICADOS COMPLEMENTARES

Para absorver melhor o conteúdo desta sprint e me aprofundar em pontos de interesse, concluí em paralelo os cursos abaixo, externos à Udemy.

### AWS

| |
|---|
|![Certificado](./certificados/)|
||

## BIBLIOGRAFIA

AMAZON WEB SERVICES. **Boto Documentation**. Última atualização: 2024. Disponível em: <[boto3.amazonaws.com/v1/documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)>.

CHAMBERS, Bill; ZAHARIA, Matei. **Spark: The Definitive Guide**. Sebastopol: O'Reilly, 2018.

DEAN, Jeffrey; GHEMAWAT, Sanjay. **MapReduce: Simplified Data Processing on Large Clusters** In: Communications of the ACM, v. 51, n. 1. New York: Association for Computing Machinery, 2008.

REIS, Joe; HOUSLEY, Matt. **Fundamentals of Data Engineering: Plan and Build Robust Data Systems**. Sebastopol: O’Reilly, 2022.

VAN ROSSUM, Guido; WARSAW, Barry; COGHLAN, Alyssa. **PEP 8 – Style Guide for Python Code**. Última atualização: 2013. Disponível em: <[peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)>.  

VAN ROSSUM, Guido; GOODGER, David. **PEP 257 – Docstring Conventions**. Última atualização: 2001. Disponível em: <[peps.python.org/pep-0257/](https://peps.python.org/pep-0257/)>.
