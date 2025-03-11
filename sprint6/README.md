#

||
|---|
|![Banner](/assets/banner-sprint6.png)|
||

## EXERCÍCIOS

Todos os códigos dos exercícios foram implementados seguindo os Python Enhancement Proposal, especificamente as recomendações de estilo do PEP8 e convenções de docstrings do PEP257, indicados na seção [Bibliografia](#bibliografia), com validação no [*CodeWOF: Python 3 Style Checker*](https://www.codewof.co.nz/style/python3/) online.

Na pasta `evidencias/exercicios`, estão localizadas as imagens com a validação de cada exercício.

* **Hospedagem S3** : criação e hospedagem de website em bucket S3 por meio do console.
  * [**/bucket-app**](./exercicios/bucket-app/) : contém os arquivos HTML de index e erro do app de teste.
  * [**/dados**](./exercicios/dados/) : contém o arquivo CSV do app de teste.
  * Conteúdo do bucket:
    * [**index.html**](./exercicios/bucket-app/index.html)
    * [**404.html**](./exercicios/bucket-app/404.html)
    * [**dados/nomes.csv**](./exercicios/dados/nomes.csv)
  * Link para o website [֍](http://compass-sprint5-lab.s3-website-us-east-1.amazonaws.com/)
* **Análise com Athena** : análise de dados *serverless* em um bucket S3 utilizando Athena.
  * [**/sql**](./exercicios/sql/) : contém os arquivos SQL com os comandos utilizados.
    * [**create_db_table.sql**](./exercicios/sql/create_db_table.sql) comandos DDL para criação de banco de dados e tabela consumida a partir de conexão com S3.
    * [**analise.sql**](./exercicios/sql/analise.sql) comando DQL utilizado para a pesquisa dos 3 nomes mais utilizados em cada década, a partir desta, é gerado o arquivo CSV a seguir.
  * [**analise_athena.csv**](./exercicios/analise_athena.csv) arquivo gerado com os resultados da query.
* **Função Serverless com Lambda** : execução de uma função Lambda em Python que calcula a quantidade de linhas de um arquivo csv armazenado em um bucket S3. A função utiliza uma camada com a biblioteca Pandas. Detalhes sobre a execução na seção [**AWS Lab Lambda**](#aws-lab-lambda).

## DESAFIO

O projeto final desenvolve um fluxo de processamento e análise de dados, a partir de uma arquitetura data lake. Para a primeira etapa, é implementada a camada raw, onde os arquivos originais são armazenados e organizados de acordo com a origem e data de processamento. A execução do script de ingestão de dados ao bucket S3 é realizada isolada em um container.

* [**./dados_raw**](./desafio/dados_raw/) : diretório com os arquivos originais.
  * [**movies.csv**](./desafio/dados_raw/movies.csv)
  * [**series.csv**](./desafio/dados_raw/series.csv)
* [**Dockerfile**](./desafio/Dockerfile) : arquivo de imagem Docker.
* [**ingestão.py**](./desafio/ingestao.py) : script de execução da etapa de criação do bucket S3 e camada raw, seguida da ingestão dos arquivos originais.
  * [**log-ingestao-20250106.txt**](./desafio/log-ingestao-20250106.txt) : arquivo de log gerado pela execução do script de ingestão.
  
Após a familiarização inicial com os datasets, as motivações para a pesquisa proposta para a análise final foram desenvolvidas na seção [Análise Final: Contra-hegemonia Cinematográfica na Era Pós-streaming](./desafio/README.md#análise-final-contra-hegemonia-cinematográfica-na-era-pós-streaming).

## EVIDÊNCIAS

Na pasta `evidencias`, encontram-se prints referentes a momentos de execução, exemplificando abordagens adotadas para o desenvolvimento dos exercícios e do desafio.  
No passo a passo explicativo, encontrado na pasta `desafio`, serão comentados outros prints de pontos específicos.

### AWS LAB S3 BUCKET: HOSPEDAGEM DE SITE ESTÁTICO

Hospedagem de site estático em um bucket, utilizando o AWS S3.

#### EXECUÇÃO NO MANAGEMENT CONSOLE

![Execução Hospedagem Console](./evidencias/exercicios/1-lab-hospedagem.gif)

### AWS LAB ATHENA & S3: ANÁLISE DE DADOS SERVERLESS

Análise de dados *serverless*, consumindo dados de um bucket S3, utilizando Athena.

#### ETAPA 1: CRIAÇÃO DO BANCO DE DADOS E TABELA DO S3

![Athena Criação de Banco e Tabela](./evidencias/exercicios/2-athena-criacao-banco.gif)

#### ETAPA 2: ANÁLISE DE DADOS

![Athena Análise de Dados](./evidencias/exercicios/3-athena-create-table-analise.gif)

### AWS LAB LAMBDA

#### ETAPA 1: DEPLOY DA FUNÇÃO

![Etapa 1 Lambda Deploy](./evidencias/exercicios/4-lambda-deploy.gif)

#### ETAPA 2: ERRO NO TESTE

![Etapa 2 Erro](./evidencias/exercicios/5-lambda-error.gif)

#### ETAPA 3: CRIAÇÃO DA LAYER EM UM DOCKER CONTAINER

![Etapa 3 Layer em Container](./evidencias/exercicios/6-lambda-build-layer-pandas.gif)

#### ETAPA 4: UPLOAD DA LAYER NO BUCKET S3

![Etapa 4 Upload da Layer no Bucket](./evidencias/exercicios/7-lambda-upload-zip-bucket.png)

#### ETAPA 5: CRIAÇÃO DA LAYER COM PANDAS

![Etapa 5 Criação de Layer](./evidencias/exercicios/8-lambda-criacao-pandas-layer.png)

#### ETAPA 6: ADIÇÃO DA LAYER NA FUNÇÃO LAMBDA

![Etapa 6 Adição da Layer na Função](./evidencias/exercicios/9-lambda-add-layer.png)

#### ETAPA 7: TESTE DA FUNÇÃO REALIZADO COM SUCESSO

![Etapa 7 Teste Realizado com Sucesso](./evidencias/exercicios/10-lambda-successful-test.png)

## BIBLIOGRAFIA

AMAZON WEB SERVICES. **Boto Documentation**. Última atualização: 2024. Disponível em: <[boto3.amazonaws.com/v1/documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)>.

AMAZON WEB SERVICES. **AWS Prescriptive Guidance: Defining S3 Bucket and Path Names for
Data Lake Layers on the AWS Cloud**. Última atualização: 2024. Disponível em: <[docs.aws.amazon.com/pdfs/prescriptive-guidance](https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/defining-bucket-names-data-lakes/definiing-bucket-names-data-lakes.pdf#raw-data-layer-naming-structure)>.

EAGAR, Gareth. **Data Engineering with AWS**. Birmingham: Packt Publishing, 2021.

REIS, Joe; HOUSLEY, Matt. **Fundamentals of Data Engineering: Plan and Build Robust Data Systems**. Sebastopol: O’Reilly, 2022.

SERRA, James. **Deciphering Data Architectures: Choosing Between a Modern Data Warehouse, Data Fabric, Data Lakehouse, and Data Mesh**. Sebastopol: O'Reilly, 2024.

VAN ROSSUM, Guido; WARSAW, Barry; COGHLAN, Alyssa. **PEP 8 – Style Guide for Python Code**. Última atualização: 2013. Disponível em: <[peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)>.  

VAN ROSSUM, Guido; GOODGER, David. **PEP 257 – Docstring Conventions**. Última atualização: 2001. Disponível em: <[peps.python.org/pep-0257/](https://peps.python.org/pep-0257/)>.
