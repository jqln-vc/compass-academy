#

||
|---|
|![Banner](/assets/banner-sprint5-desafio.png)|
||

## SEÇÕES

## INTRODUÇÃO AO AWS S3: SIMPLE STORAGE SERVICE

### PREFIXOS

You can use prefixes to organize the data that you store in Amazon S3 buckets. A prefix is a string
of characters at the beginning of the object key name. A prefix can be any length, subject to
the maximum length of the object key name (1,024 bytes). You can think of prefixes as a way to
organize your data in a similar way to directories. However, prefixes are not directories (AWS, p. 358)

## INTRODUÇÃO AO DATASET: CRT OBRAS NÃO PUBLICITÁRIAS REGISTRADAS

O dataset utilizado neste projeto, pertencente ao banco de dados da ANCINE (Agência Nacional do Cinema), refere às obras não publicitárias com CRT (Certificado de Registro de Título) emitidos no período de  2002 a 2024.

A seguir a listagem e descrição dos campos:

|||
|:---|:---|
|**TITULO_ORIGINAL**|Nome que descreve o título original da obra não publicitária.|
|**TITULO_BRASIL**|Nome que descreve o título, no Brasil, da obra não publicitária.|
|**CRT**|Número do Certificado de Registro de Título da obra.|
|**DATA_REQUERIMENTO_CRT**|Data de requerimento do Certificado de Registro de Título (CRT) da obra.|
|**DATA_EMISSAO_CRT**|Data de emissão do Certificado de Registro de Título (CRT) da obra.|
|**SITUACAO_CRT**|Situação do Certificado de Registro de Título (CRT) da obra.|
|**CPB_ROE**|Número do Certificado de Produto Brasileiro (CPB) quando obra não publicitária brasileira ou Registro de Obra Estrangeira (ROE) quando obra não publicitária estrangeira.|
|**TIPO_OBRA**|Informa o tipo da obra, indicando seu gênero de produção. *Exemplos: Animação, Documentário, Ficção, entre outros.*|
|**SUBTIPO_OBRA**|Informa o subtipo da obra. *Exemplos: Vídeoaula, Registro de Eventos, entre outros.*|
|**CLASSIFICACAO**|Informa a categoria da obra. *Exemplos: Comum, Brasileira Constituinte de Espaço Qualificado, entre outras.*|
|**PAIS**|Informa o país da obra.|
|**ORGANIZACAO_TEMPORAL**|Informa a organização temporal da obra. *Exemplos: Não Seriada, Seriada em Temporada Única, entre outras.*|
|**DURACAO_TOTAL_MINUTOS**|Duração, em minutos, do tempo de exibição da obra. Caso obra seriada, somatório total dos episódios.|
|**ANO_PRODUCAO_INICIAL**|Informa o ano de produção da obra. Caso obra seriada, o ano inicial de produção.|
|**ANO_PRODUCAO_FINAL**|Caso obra seriada, informa o último ano de produção da obra.|
|**SEGMENTO**|Informa o segmento de mercado de veiculação da obra. *Exemplos: Salas de exibição, Mídias Móveis, entre outros.*|
|**REDUCAO_ISENCAO**|Informa o tipo de redução que será utilizado para cálculo da CONDECINE da obra.|
|**REQUERENTE**|Nome do requerente do registro da obra.|
|**UF_REQUERENTE**|Sigla da unidade federativa referente ao endereço do requerente.|
|**MUNICIPIO_REQUERENTE**|Município referente ao endereço do requerente.|
|||

### ANÁLISE: PRODUÇÃO AUDIOVISUAL DURANTE A PANDEMIA

A partir dos dados coletados, após a concatenação dos datasets referentes às produções anuais com o script `ingestao.py`, foi realizada uma análise da produção audiovisual brasileira no período de pandemia do COVID-19, abarcando as obras com CRT emitido entre 2020 e 2022, no qual foram agrupados os totais anuais por:

- Ano de Produção Inicial
- Requerente
- Tipo de Obra
- Segmento

## CONCATENAÇÃO DE DATASETS

A partir do módulo `ingestao.py`, foi utilizada a função `concatenador_csv` 

## SEQUÊNCIA DE MANIPULAÇÕES

Nas próximas subseções, serão descritas as etapas de manipulação de dados solicitadas, na ordem em que foram realizadas. E abaixo encontra-se o fluxo de execução das funções no script, concatenadas para a obtenção de uma única análise.

```python
    # sequência de chamadas pandas
```

### CONVERSÕES

### MANIPULAÇÃO DE DATA

### FILTRO COM OPERADORES LÓGICOS

### FILTRO CONDICIONAL

### MANIPULAÇÃO DE STRING

### FUNÇÕES DE AGREGAÇÃO: COUNT & GROUP BY

## INTEGRAÇÃO COM S3 BUCKET

## SEQUÊNCIA DE EXECUÇÃO

O script `etl.py` executa a importação dos módulos necessários e a chamada das funções que realizam as etapas a seguir, em sequência:
