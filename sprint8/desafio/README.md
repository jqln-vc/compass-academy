#

||
|---|
|![Banner](/assets/banner-sprint7-desafio.png)|
||

## SEÇÕES

* **Primeiras Explorações no Dataset** [֍](#primeiras-explorações-no-dataset)
  * **Recapitulando a Análise Inicial** [֍](#recapitulando-a-análise-inicial)
  * **Filtros Iniciais no Dataset Original** [֍](#filtros-iniciais-no-dataset-original)
    * **Filtro 1: Gênero** [֍](#filtro-1-gênero)
    * **Filtro 2: Data de Lançamento** [֍](#filtro-2-data-de-lançamento)
    * **Filtro 3: IDs Distintos** [֍](#filtro-3-ids-distintos)
    * **Filtro 4 (Descartado): Títulos Originais em Inglês** [֍](#filtro-4-descartado-títulos-originais-em-inglês)
  * **Reformulação da Análise Final** [֍](#reformulação-da-análise-final)
* **Data Lake e Ingestão de Dados: Fontes Distintas** [֍](#data-lake-e-ingestão-de-dados-fontes-distintas)
  * **Processamento de Dados no Data Lake: Etapa de Ingestão Pt.2** [֍](#processamento-de-dados-no-data-lake-etapa-de-ingestão-pt-2)
  * **API TMDB: Seleção de Dados** [֍](#api-tmdb-seleção-de-dados)
  * **Criação de Arquivo ZIP para Layer** [֍](#criação-de-arquivo-zip-para-layer)
  * **Criação e Configuração da Lambda e Layer** [֍](#criação-e-configuração-da-lambda-e-layer)
  * **Variáveis de Ambiente** [֍](#variáveis-de-ambiente)
  * **Criação do IAM Role** [֍](#criação-do-iam-role)
  * **Análise do Script Lambda** [֍](#análise-do-script-lambda)
    * **Cabeçalho e Importações** [֍](#cabeçalho-e-importações)
    * **Classe LogPrinter** [֍](#classe-logprinter)
    * **Função Processador API Batch** [֍](#função-processador-api-batch)
    * **Variáveis** [֍](#variáveis)
    * **Execução Lambda** [֍](#execução-lambda)
  * **Execução da Ingestão no Data Lake** [֍](#execução-da-ingestão-no-data-lake)
    * **Arquivos JSON Consumidos Após a Ingestão** [֍](#arquivos-json-consumidos-após-a-ingestão)
    * **Arquivo de Log Gerado** [֍](#arquivo-de-log-gerado)
* **Considerações Finais** [֍](#considerações-finais)
* **Referências** [֍](#referências)

## PRIMEIRAS EXPLORAÇÕES NO DATASET

*Voltar para **Seções*** [֍](#seções)

Inicialmente, esta etapa busca afunilar os dados originais, obtidos na sprint anterior, utilizando filtros referentes à análise final. Deste modo, é gerado um arquivo CSV de referência, a ser complementado com os dados obtidos via TMDB.

### RECAPITULANDO A ANÁLISE INICIAL

*Voltar para **Seções*** [֍](#seções)

Antes de detalhar os filtros utilizados, faz-se necessário retomar as questões iniciais, elaboradas para a análise final em torno do tema **Contra-hegemonia Cinematográfica na Era Pós-streaming**.

* ***Qual a quantidade de filmes lançados anualmente, por região?***
* ***Quais as atrizes/atores com maior atuação e em qual(is) língua(s)?***
* ***Quais diretoras/diretores com maior quantidade de títulos, em quais línguas?***
* ***Dentre os 100 títulos melhores votados, quais as nacionalidades das produções?***

### FILTROS INICIAIS NO DATASET ORIGINAL

*Voltar para **Seções*** [֍](#seções)

Inicialmente, a análise buscava considerar tanto filmes de **drama** quanto **romance**, porém ao fim da etapa do [filtro 3](#filtro-3-ids-distintos), o dataset recortado ainda possuía mais de 16000 linhas.

Para o próximo **recorte linguístico e regional**, seria necessário diminuir o tamanho desse dataset a partir dos dados obtidos pela API do TMDB. Para isso, seriam necessárias mais de 16000 requisições, aumentando o overhead de execução na AWS Lambda (a qual possui *max timeout* de 900 segundos). Logo, foi decidido um novo recorte, mantendo-se somente o gênero **romance**.

#### FILTRO 1: GÊNERO

*Voltar para **Seções*** [֍](#seções)

Primeiro filtro, utilizando expressão regular, para filmes exclusivamente do gênero **romance**. Nesta etapa, o dataset foi reduzido para 11919 linhas.

* `^` indica início da string
* `$` indica o fim da string

```python
    df1 = df[df['genero'].str.contains(r'^Romance$', regex=True)]
```

![Filtro 1](../evidencias/desafio/1-filtro-genero.png)

#### FILTRO 2: DATA DE LANÇAMENTO

*Voltar para **Seções*** [֍](#seções)

Neste filtro, é realizado o recorte temporal do período entre 2013 e dias atuais. Primeiramente, foram tratados possíveis valores nulos caracterizados por caracteres não-numéricos, identificados com expressão regular.

* `[a-zA-Z]+` 1 ou mais caracteres alfabéticos, considerando minúsculas e maiúsculas

```python
    # Tratamento de dados nulos com 0
    df1.loc[df1['anoLancamento'].str.contains(r'^[a-zA-Z]+$', regex=True), 'anoLancamento'] = 0
    # Conversão da coluna para integer
    df1['anoLancamento'] = df1['anoLancamento'].astype(int)
```

Após o tratamento do tipo da coluna, é realizado o filtro temporal. O dataset resultante nesta etapa ficou com 3975 linhas.

```python
    df2 = df1[df1['anoLancamento'] >= 2013]
```

![Filtro 2](../evidencias/desafio/2-filtro-temporal.png)

Este dataset contém mais de uma linha para cada filme, devido às colunas referentes aos artistas do elenco. Como este dataset já possui os dados-base para a análise final, a serem complementados com os dados do TMDB, o mesmo foi salvo no arquivo [dataset_base_com_elenco.csv](../desafio/csv/dataset_base_com_elenco.csv).

#### FILTRO 3: IDS DISTINTOS

*Voltar para **Seções*** [֍](#seções)

Nesta etapa, são mantidas somente 1 linha para cada filme, assim gerando posteriormente uma lista de IDs distintos para a iteração de requisições de dados via API. Nesta etapa, o dataset possui 920 linhas.

```python
    df3 = df2.drop_duplicates(subset=['id'], keep='last')
```

![Etapa 3](../evidencias/desafio/3-filtro-ids-distintos.png)

#### FILTRO 4 (DESCARTADO): TÍTULOS ORIGINAIS EM INGLÊS

*Voltar para **Seções*** [֍](#seções)

Considerando que filmes com idioma original inglês não serão considerados na análise final, nesta etapa buscou-se reduzir ainda mais a quantidade de IDs utilizados na etapa de requisição de dados via API.

Utilizando a biblioteca de transformers do Hugging Face, foi escolhido um modelo de língua específico para identificação de língua, o `papluca/xlm-roberta-base-language-detection` , para classificar os valores presentes na coluna `tituloOriginal` , caso estivessem em inglês, com `True` ou `False`. Assim, ao final, seriam mantidos somente as linhas com classificação `False`.

![Classificação Modelo de Língua](../evidencias/desafio/14-filtro-ingles-modelo-llm.png)

O modelo obteve um ótimo resultado, uma amostra foi mantida no arquivo [ids_distintos_attr_em_ingles.csv](../desafio/csv/ids_distintos_attr_em_ingles.csv).

No entanto, foram identificadas inconsistências nos valores da coluna: existiam casos com título original em inglês, que não correspondiam aos títulos corretos, em línguas de interesse para a análise. Como é o caso do exemplo a seguir, do id `tt0120589` que possui título original em português:

![Linha Título Divergente](../evidencias/desafio/5-imdb-linha-com-divergencia.png)

> ❗ Esta verificação foi feita antes do recorte exclusivo para o gênero **romance**, no entanto, uma única inconsistência já pode ser generalizada para outras possíveis ocorrências que impactariam a análise final.

Abaixo a verificação do ID no IMDB, atestando a divergência entre a coluna título original e valores reais.

![Divergência Títulos Originais](../evidencias/desafio/4-imdb-divergencia-titulo-original.png)

### REFORMULAÇÃO DA ANÁLISE FINAL

*Voltar para **Seções*** [֍](#seções)

Considerando os fatores comentados acima, o fato de que para os dados de **direção** existiam muitos desfalques de ids sem essa informação, bem como novas perspectivas, as perguntas foram reformuladas em:

* ***Qual a quantidade de filmes lançados anualmente, por região?***
* ***Quais os 5 países com maior quantidade de filmes lançados? Desses países, quais línguas são mais utilizadas***
* ***Quais as atrizes/atores com maior atuação e em qual(is) língua(s)?***
* ***Quais as 5 línguas com maior quantidade de títulos?***
* ***Dentre os 100 títulos melhores votados, quais as nacionalidades das produções?***
* ***Quais os tópicos mais recorrentes nas narrativas dos títulos selecionados?***

Com isso, também será reformulado o tema central da análise, enfocando somente o gênero romance: **Contra-hegemonia no Cinema: Novas Perspectivas Afetivas na Era Pós-streaming**.

## DATA LAKE E INGESTÃO DE DADOS: FONTES DISTINTAS

*Voltar para **Seções*** [֍](#seções)

Nesta etapa do projeto, a camada **raw** do data lake é enriquecida com dados provenientes de fontes externas, um processo corriqueiro porém nada trivial, pois engloba o estudo das especificidades de fonte, formato, tempo, volume e utilização dos dados.

> *Ingestão de dados é o processo de mover dados de um lugar para outro. A ingestão de dados implica na movimentação de dados de sistemas-fonte para o armazenamento no ciclo de vida de engenharia de dados, sendo a ingestão um passo intermediário.* [^1]

### PROCESSAMENTO DE DADOS NO DATA LAKE: ETAPA DE INGESTÃO PT. 2

*Voltar para **Seções*** [֍](#seções)

No ciclo de vida da engenharia de dados, a etapa de ingestão precisa considerar alguns fatores para otimização do processo de coleta de dados, incluindo finalidade, fonte dos dados, quantidade e frequência, entre outros. A seguir, alguns pontos a nortearem o planejamento da ingestão [^2]:

* *Qual a utilidade dos dados que estou ingerindo?*
* *Posso reutilizar esses dados e evitar a ingestão de múltiplas versões do mesmo dataset?*
* *Para onde esses dados estão indo? Qual o destino?*
* *Com que frequência os dados da fonte precisam ser atualizados?*
* *Qual o volume de dados esperado?*
* *Qual o formato que os dados estão? As etapas seguintes de armazenamento e transformação conseguirão aceitar esse formato?*
• *A fonte dos dados está em boa forma para consumo imediato nas etapas seguintes? Isto é, os dados têm boa qualidade? Qual é o pós-processamento necessário para distribuição? Quais são os riscos de qualidade (ex. o tráfego de bots em um website poderia contaminar os dados)?*
* *Os dados necessitam de processamento "em trânsito" para ingestão caso os dados sejam provenientes de uma fonte em **streaming**?*

### API TMDB: SELEÇÃO DE DADOS

*Voltar para **Seções*** [֍](#seções)

Para a complementação dos dados existentes no dataset `movies.csv`, foi necessário obter os seguintes dados do TMDB via requisição GET, utilizando a URL abaixo:

```python
    f"https://api.themoviedb.org/3/movie/{imdb_id}?language=en-US"
```

* `imdb_id` : código externo referente ao id no IMDB, e utilizado como "chave estrangeira" para alinhar com os filmes no dataset em CSV
* `original_title` : título na língua original
* `origin_country` : sigla do país de origem
* `original_language` : língua original, no formato ISO 639-1
* `spoken_languages` : lista de línguas adicionais faladas no filme, no formato ISO 639-1
* `overview` : sinopse do filme em inglês, utilizado para obter os tópicos das narrativas

A partir da [documentação](https://developer.themoviedb.org/docs/getting-started) foi estudada a maneira mais objetiva de obter todos os dados necessários acima, esta é uma etapa importante para otimizar o tempo de execução, ao minimizar a quantidade de requisições necessárias, assim reduzindo custos (se considerarmos largas escalas).

> *APIs são um tipo de fonte de dados que continua a crescer em importância e popularidade. Uma organização comum pode ter centenas de fontes de dados externas, tais como plataformas SaaS e outras empresas parceiras. A dura realidade é que não existe um padrão real para troca de dados via APIs. Engenheiros de dados podem passar um tempo significativo lendo documentações, comunicando-se com proprietários de dados externos, e escrevendo e mantendo códigos de conexão com APIs.* [^3]

Além disso, foram obtidos, diretamente no site do TMDB, a lista de códigos de países e línguas utilizadas na base de dados. Abaixo uma amostra desses dados, localizados nos arquivos [linguas.json](./api_data/linguas.json) e [paises.json](./api_data/paises.json) :

![Lingua JSON](../evidencias/desafio/17-amostra-json-linguas.png)

![Países JSON](../evidencias/desafio/18-amostra-json-paises.png)

### CRIAÇÃO DE ARQUIVO ZIP PARA LAYER

*Voltar para **Seções*** [֍](#seções)

Para utilizar tanto a biblioteca `requests` e o arquivo `csv`, utilizado para obter os ids de filmes para as requisições do TMDB, foi criada uma ***layer*** para carregar o ambiente necessário para a execução da Lambda.

Abaixo os comandos utilizados no terminal para a criação do arquivo zipado `requests_layer.zip` localizado no diretório [lambda_layer/](./lambda_layer):

![Criação Zip Layer 1](../evidencias/desafio/6-zip-layer-requests.png)

![Criação Zip Layer 2](../evidencias/desafio/7-zip-layer-csv.png)

### CRIAÇÃO E CONFIGURAÇÃO DA LAMBDA E LAYER

*Voltar para **Seções*** [֍](#seções)

Para que não ocorresse erro por Timeout, foi configurado o limite máximo de execução, e acrescentada uma quantidade maior de memória para a Lambda.

![Lambda Configuração](../evidencias/desafio/9-lambda-config.png)

A ***layer*** é criada com o arquivo `zip` e configurada na Lambda desta etapa:

![Lambda Layer](../evidencias/desafio/10-lambda-layer.png)

![Lambda Layer Config](../evidencias/desafio/11-lambda-layer-config.png)

### VARIÁVEIS DE AMBIENTE

*Voltar para **Seções*** [֍](#seções)

Foi necessário configurar algumas variáveis de ambiente, seja pela praticidade de acessar caminhos ou pela segurança de restringir o acesso a chaves de acesso. O arquivo `CSV` incluído na ***layer*** é acessado por meio do diretório `/opt` . A seguir as variáveis utilizadas:

![Lambda Variáveis de Ambiente](../evidencias/desafio/8-lambda-env-variables.png)

### CRIAÇÃO DO IAM ROLE

*Voltar para **Seções*** [֍](#seções)

Para as permissões da Lambda, foi reutilizado um IAM Role criado para o Lab da sprint 6, acrescentando a permissão de escrita e leitura dos arquivos no S3.

![Lambda IAM Role](../evidencias/desafio/15-lambda-role.png)

### ANÁLISE DO SCRIPT LAMBDA

*Voltar para **Seções*** [֍](#seções)

A seguir um detalhamento de cada seção do script de ingestão implementado na AWS Lambda.

#### CABEÇALHO E IMPORTAÇÕES

*Voltar para **Seções*** [֍](#seções)

O script é iniciado com documentação em ***docstrings***, detalhando autoria, data, propósito e arquivos gerados.

![Script: Cabeçalho e Importações](../evidencias/desafio/19-script-cabeçalho-importações.png)

Dentre as bibliotecas utilizadas, somente a `requests` teve de ser instalada externamente e configurada na ***layer*** da Lambda.

* `json` tratamento dos arquivos de saída
* `csv` processamento do dataset base para obtenção dos ids de filmes utilizados nas requisições
* `boto3` integração com serviços AWS
* `requests` execução das requisições GET dos dados do TMDB
* `os` acesso às variáveis de ambiente
* `sys` acesso ao stdout para a configuração da classe LogPrinter
* `datetime` acesso ao horário do sistema, para registros nos logs e nos diretórios da camada raw
* `math` utilização da função `ceil` para arredondamento superior no cálculo de batches necessários para execução.

#### CLASSE LOGPRINTER

*Voltar para **Seções*** [֍](#seções)

Implementação de classe LogPrinter já utilizada e detalhada anteriormente, a qual reconfigura o `stdout`, gerando registros de logs de execução a cada chamada da função `print()` e, posteriormente, geração de arquivo de texto.

![Script: Classe LogPrinter](../evidencias/desafio/20-script-logprinter.png)

#### FUNÇÃO PROCESSADOR API BATCH

*Voltar para **Seções*** [֍](#seções)

Função principal do script, faz o particionamento dos dados em batches, as requisições à API do TMDB, filtro de dados obtidos, geração de arquivo JSON e upload do mesmo no bucket S3.

A função possui os seguintes parâmetros:

![Script: Função Processador Parâmetros](../evidencias/desafio/21-script-funcao-processador-api-parametros.png)

* `filmes_id` lista com os ids de filmes obtidos a partir do arquivo CSV resultante da exploração e filtros iniciais comentados na seção [Filtros Iniciais no Dataset Original](#filtros-iniciais-no-dataset-original), localizado em [dataset_base_com_elenco.csv](./csv/dataset_base_com_elenco.csv).
* `headers` dicionário com chave de leitura da API, utilizada na requisição GET.
* `paises_excluidos` lista com siglas de países excluídos no recorte regional da análise final.
* `atributos` lista com os atributos/colunas/chaves a serem obtidos do TMDB para complementação dos dados da análise.
* `s3_bucket` nome do bucket de destino da ingestão.
* `tam_batch` quantidade de requisições a serem realizadas por batch, valor default de 100.
* `caminho_output` caminho de saída para armazenamento dos arquivos JSON gerados, valor default "./api_data".

Primeiramente, a quantidade de batches necessária é calculada a partir da quantidade de ids a serem buscados nas requisições. Neste caso, a quantidade de ids distintos é 920, o valor é dividido pelo tamanho do batch (100) e arrendondado "para cima", resultando em 10 batches.

Em seguida, um laço de repetição itera os (10) batches, selecionando o índice de ínicio e término da lista de (920) ids, selecionando 100 ids a cada iteração, salvos na variável `batch_atual` .

![Script: Função Processador Quantidade de Batches](../evidencias/desafio/22-script-funcao-processador-api-qtd-batches.png)

Então, um novo laço interno itera cada um dos 100 ids do batch atual, fazendo a requisição dos dados partir do id.

Havendo confirmação de obtenção dos dados com o status 200 (alguns ids não foram localizados na base de dados, resultando em status 404), é aplicado um filtro condicional de exclusão de filmes com base no país de origem e língua original.

Caso o registro obtido passe nesse filtro, este é adicionado a uma lista referente aos ids obtidos neste batch.

![Script: Função Processador Requisições](../evidencias/desafio/23-script-funcao-processador-api-requisicoes-por-id.png)

Terminadas as requisições do batch, caso a lista `dados` não esteja vazia, somente os dados de interesse na lista `atributos` são coletados e salvos em `dados_filtrados`, e a geração do arquivo JSON é feita diretamente no bucket, na estrutura de diretórios declarada em `caminho_output` .

![Script: Função Processador JSON Dumps no S3](../evidencias/desafio/24-script-funcao-processador-json-dumps-s3.png)

#### VARIÁVEIS

*Voltar para **Seções*** [֍](#seções)

Declaração das variáveis utilizadas no script:

![Script: Variáveis](../evidencias/desafio/25-script-funcao-processador-variaveis.png)

* **Chaves de acesso à API TMDB**
* **Obtenção de horário atual do sistema para registros na camada raw e logs de execução**
* Caminhos e nomes de arquivos**
* **Conexão via ***resource*** com o AWS S3**
* **Processamento do arquivo CSV e obtenção dos ids distintos na primeira coluna, salvos na variável `filmes_id`**
* **Preparação do header de requisição com a chave de acesso**

Para as variáveis referentes aos filtros de dados, será interessante um melhor detalhamento devido à relevância para a análise final:

* **Países excluídos**: localizados na Europa Ocidental e América do Norte, ou com histórico de colonização, não incorporados no recorte regional.

```python
    paises_excluidos = [
    "AD",  # Andorra
    "BE",  # Bélgica
    "CA",  # Canadá
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
```

* **Atributos**: dados de interesse a serem obtidos para complementar o dataset.

```python
    atributos = [
    "imdb_id",              # ID utilizado como "chave estrangeira"
    "original_title",       # Título na língua original
    "origin_country",       # Sigla do país de origem
    "original_language",    # Sigla da língua original
    "spoken_languages",     # Línguas adicionais, se houverem
    "overview"              # Sinopse do filme (em inglês)
    ]
```

#### EXECUÇÃO LAMBDA

*Voltar para **Seções*** [֍](#seções)

A seguir a função `lamda_handler`, que faz a integração com a execução baseada em eventos da Lambda. Nesta seção, é executada a sequência dos processos pontuada pelas gerações de logs, com as funções de `print()` a cada conclusão de etapa. O conteúdo do bucket é listado somente para fins de registro no arquivo de logs. Por fim, o arquivo `logger` é fechado e enviado ao bucket, a funçaõ retorna com um código de sucesso.

![Script: Execução Lambda](../evidencias/desafio/26-script-funcao-processador-execucao-lambda.png)

### EXECUÇÃO DA INGESTÃO NO DATA LAKE

*Voltar para **Seções*** [֍](#seções)

A seguir uma amostra da execução da Lambda e os arquivos ingeridos no S3, na camada ***raw***.

![Execução Lambda e Ingestão](../evidencias/desafio/16-execucao-lambda-desafio.gif)

#### ARQUIVOS JSON CONSUMIDOS APÓS A INGESTÃO

*Voltar para **Seções*** [֍](#seções)

Abaixo a estrutura dos arquivos armazenados no bucket S3:

![Bucket S3 Arquivos JSON](../evidencias/desafio/12-lambda-jsons.png)

E uma amostra dos registros obtidos, com a seleção dos atributos de interesse para a complementação dos dados de análise:

![Amostra JSON TMDB](../evidencias/desafio/27-amostra-json-tmdb.png)

#### ARQUIVO DE LOG GERADO

*Voltar para **Seções*** [֍](#seções)

![Bucket S3 Arquivo Log](../evidencias/desafio/13-lambda-logs-s3.png)

## CONSIDERAÇÕES FINAIS

*Voltar para **Seções*** [֍](#seções)

O fluxo de engenharia de dados engloba as diversas etapas pelas quais um dado, ou um grupo deles, passa desde sua geração nos sistemas-fonte até seu consumo em análises e inferências. Neste momento, ainda na etapa de ingestão, são obtidos dados provenientes de fontes externas, neste caso, via requisições a APIs.

O planejamento desta etapa, considerando principalmente a finalidade, o volume e o formato dos dados a serem ingeridos, é essencial para a otimização da performance. É preciso buscar a redução de ingestão de dados desnecessários ou já existentes, economizando em vários aspectos, desde tempo de computação a espaço de armazenagem.

Portanto, o controle do ciclo de vida dos dados é fundamental para o controle e a governança, e sua negligência pode resultar em aumentos de custos, brechas de segurança e a transformação do data lake no temido ***data swamp***.

## REFERÊNCIAS

*Voltar para **Seções*** [֍](#seções)

[^1]: REIS & HOUSLEY, 2022, p. 234
[^2]: Ibid., p. 235
[^3]: Ibid., p. 254
