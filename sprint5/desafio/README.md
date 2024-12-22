#

||
|---|
|![Banner](/assets/banner-sprint5-desafio.png)|
||

## SEÇÕES

## INTRODUÇÃO AO DATASET: OBRAS NÃO PUBLICITÁRIAS REGISTRADAS

O dataset utilizado neste projeto, pertencente ao banco de dados da ANCINE (Agência Nacional do Cinema), refere às obras não publicitárias com CPB (Certificado de Produto Brasileiro) emitidos no período de  2002 a 2024.

O **CPB** é um registro gratuito concedido pela ANCINE a obras audivisuais não publicitárias, obrigatório para todas as obras que visarem à exportação ou a sua comunicação pública, em território brasileiro, nos segmentos de mercado regulados pela ANCINE. Sendo também um requisito para a obtenção do CRT (Certificado de Registro de Título) das obras audiovisuais não publicitárias brasileiras.

A seguir a listagem e descrição dos campos:

|||
|:---|:---|
|**Título Original**|Nome que descreve o título original da obra não publicitária.|
|**CPB**|Número do Certificado de Produto Brasileiro.|
|**Data de Emissão do CPB**|Data de emissão do registro do CPB.|
|**Situação da Obra**|Situação do registro da obra.|
|**Tipo da Obra**|Informa o tipo da obra, indicando seu gênero de produção. *Exemplos: Animação, Documentário, Ficção, entre outros.*|
|**Subtipo da Obra**|Informa o subtipo da obra. *Exemplos: Vídeoaula, Registro de Eventos, entre outros.*|
|**Classificação da Obra**|Informa a categoria da obra. *Exemplos: Comum, Brasileira Constituinte de Espaço Qualificado, entre outras.*|
|**Organização Temporal**|Informa a organização temporal da obra. *Exemplos: Não Seriada, Seriada em Temporada Única, entre outras.*|
|**Duração Total (Minutos)**|Duração, em minutos, do tempo de exibição da obra. Caso obra seriada, somatório total dos episódios.|
|**Quantidade de Episódios**|Para obras seriadas, indica a quantidade de episódios.|
|**Ano de Produção Inicial**|Informa o ano de produção da obra. Caso obra seriada, o ano inicial de produção.|
|**Ano de Produção Final**|Caso obra seriada, informa o último ano de produção da obra.|
|**Segmento de Destinação**|Informa o segmento de mercado de veiculação da obra. *Exemplos: Salas de exibição, Mídias Móveis, entre outros.*|
|**Coprodução Internacional**|Indica se a obra é coproduzida por requerentes estrangeiros.|
|**Requerente**|Nome do requerente do registro da obra.|
|**CNPJ do Requerente**|Registro de CNPJ do requerente do registro da obra.|
|**UF do Requerente**|Sigla da unidade federativa referente ao endereço do requerente.|
|**Município do Requerente**|Município referente ao endereço do requerente.|
|||

Com exceção das colunas de `Quantidade de Episódios`, `Ano de Produção Inicial` e `Ano de Produção Final`, todas as demais colunas possuem originalmente o tipo `object`. E, mesmo as colunas citadas, possuem o tipo `float64`, inadequado para o tipo de valor que contêm.

![DataFrame Info](../evidencias/desafio/1-colunas-dataypes.png)

### ANÁLISE: PRODUÇÃO AUDIOVISUAL DURANTE A PANDEMIA

A partir dos dados coletados, após a concatenação dos datasets referentes às produções anuais, foi realizada uma análise da produção audiovisual brasileira no período de pandemia do COVID-19, abarcando as obras de longa metragens (a partir de 60 minutos de duração) com CPB emitido entre 2020 e 2022, no qual foram agrupados os totais da coluna `Qtd de Filmes` por:

* **Tipo da Obra**
* **Subtipo da Obra**
* **Segmento de  Destinação**

Deste modo, busca-se interpretar quais os tipos e subtipos de obras mais produzidas no período crítico de quarentena, e quais os segmentos de destinação mais utilizados.

## INTRODUÇÃO AO AWS S3: SIMPLE STORAGE SERVICE

### ARMAZENAGEM DE OBJETOS

### PREFIXOS

> *Você pode utilizar prefixos para organizar os dados armazenados em buckets Amazon S3. Um prefixo é uma string de caracteres no início do nome-chave (**key name**) de um objeto. Um prefixo pode ter qualquer tamanho, sujeito ao tamanho máximo do key name do objeto (1024 bytes). Você pode interpretar os prefixos como uma maneira de organizar seus dados em uma maneira similar aos diretórios. No entanto, prefixos não são diretórios.* (AWS, p. 358)

## INTRODUÇÃO À API BOTO

A integração com os serviços AWS via Python é realizada com a API Boto, as informações para sua utilização foram consultadas na [documentação](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

Existem 4 tipos de chamadas aos recursos:

* **Client**
  * Interface de baixo nível, com métodos que são mapeados quase diretamente aos serviços AWS.
  * Parâmetros devem ser passados como argumentos nomeados (*keywords*), não funcionam se forem passados como arumentos posicionais.
  * Respostas são retornadas como dicionários.

```python
    s3 = boto3.client('s3')
```

* **Resources**
  * Interface de alto nível, orientada a objetos
  * Permite tratar os recursos AWS como objetos Python, com atributos e métodos

```python
    s3 = boto3.resource('s3')
    bucket = s3.create_bucket(Bucket='novo-bucket')
```

* **Paginators**
  * Resultados paginados

```python
    s3 = boto3.resource('s3')
    bucket = s3.create_bucket(Bucket='novo-bucket')
```

* **Waiters**
  * Utiliza a execução de um serviço de cliente para consultar (*polling*) a conclusão de estados específicos em um serviço AWS.
  * Suspende a execução do programa até obter o estado desejado ou alguma falha durante o *polling*.

```python
    s3 = boto3.client('s3')

    # Caso um cliente não possua nenhum waiter, o comando abaixo retorna uma lista vazia.
    print("s3 waiters:")
    s3.waiter_names

    # Armazena uma instância de waiter que irá aguardar até que determinado bucket exista.
    s3_bucket_exists_waiter = s3.get_waiter('bucket_exists')

    # Comando para iniciar a espera de existência do bucket.
    s3_bucket_exists_waiter.wait(Bucket='amzn-s3-demo-bucket')
```

## SEQUÊNCIA DE MANIPULAÇÕES NO DATASET

Nas próximas subseções, serão descritas as etapas de manipulação de dados solicitadas, na ordem em que foram realizadas. E abaixo encontra-se o fluxo de execução das funções no script, concatenadas para a obtenção de uma única análise.

Esta sequência foi executada a partir do script `analise.py`, utilizando a biblioteca Pandas.

### TRATAMENTO DE STRINGS

Primeiramente, é realizado o tratamento do nome das colunas que, originalmente, constam todas em maiúsculas. Além de facilitar a memorização, auxilia na leitura do dataset final da análise.

```python
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
    
    df.columns = colunas
```

Em seguida, as colunas de interesse, que constarão no dataset da análise final, têm seus valores de string tratados com o método `title()`, deixando cada palavra com maiúscula inicial seguida de minúsculas.

```python
    df['Tipo da Obra'] = df['Tipo da Obra'].str.title()
    df['Subtipo da Obra'] = df['Subtipo da Obra'].str.title()
    df['Segmento de Destinação'] = df['Segmento de Destinação'].str.title()
```

### MANIPULAÇÃO DE DATA

Na coluna `Data de Emissão do CPB`, utilizada para filtrar o período concernente à pandemia do COVID-19, é preciso fazer o tratamento da data, originalmente no formato DD/MM/YYYY, com o método `to_datetime()`.

```python
    df['Data de Emissão do CPB'] = pd.to_datetime(
        df['Data de Emissão do CPB'], 
        dayfirst=True,  # Considera o formato DD/MM/YYYY
        errors='coerce')
```

### CONVERSÃO ADICIONAL PARA FLOAT

Para filtrar a coluna de `Duração Total (Minutos)`, originalmente do tipo `object`, é necessário substituir as vírgulas por pontos, adequando o formato antes da conversão para `float`.

```python
    df['Duração Total (Minutos)'] = df['Duração Total (Minutos)'].str.replace(',', '.').astype(float)
```

### FILTRO COM ATRIBUTOS DE DATA, CONDICIONAIS & OPERADORES LÓGICOS

A seguir, são concatenados 3 operadores lógicos AND (&)

```python
df = df[(df['Data de Emissão do CPB'].dt.year >= 2020) & 
        (df['Data de Emissão do CPB'].dt.year <= 2022) & 
        (df['Organização Temporal'] == 'NÃO SERIADA') &
        (df['Duração Total (Minutos)'] >= 60)]
```

### FUNÇÕES DE AGREGAÇÃO: GROUP BY, COUNT & MAX

```python
    df = df.groupby([
        'Tipo da Obra',
        'Subtipo da Obra',
        'Segmento de Destinação'
    ])['CPB']\
        .count()\
        .reset_index(name='Qtd de Filmes')\
        .sort_values(by='Qtd de Filmes', ascending=False)

    df = df.loc[df['Qtd de Filmes'] == df['Qtd de Filmes'].max()]
```

## SEQUÊNCIA ETL

O script `etl.py`, comentado a seguir, executa a concatenação dos arquivos `csv` raw (anuais) em um único dataset, faz a integração com o AWS S3 via API Boto, e executa o script `analise.py` gerando o dataset final.

![Script ETL]()

### DATASET COM ANÁLISE FINAL

Após a execução do script `analise.py`, obtemos uma única linha com o `Tipo de Obra`, `Subtipo de Obra` e `Segmento de Destinação` que mais teve longa metragens produzidos no período entre 2020 e 2022, caracterizado pelas medidas de isolamento social.

![Dataset Final](../evidencias/desafio/2-analise-final.png)

### DEMONSTRAÇÃO DE EXECUÇÃO DO SCRIPT

![Execução Final ETL](../evidencias/desafio/4-execucao-desafio.gif)

## IMPLEMENTAÇÃO DE MELHORIAS ADICIONAIS

## CONSIDERAÇÕES FINAIS

## REFERÊNCIAS
