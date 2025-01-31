#

||
|---|
|![Banner](/assets/banner-sprint8-desafio.png)|
||

## SEÇÕES

* **Introdução à Computação Distribuída** [֍]()
  * **Visão Geral do Hadoop** [֍]()
  * **Visão Geral do Apache Spark** [֍]()
    * **Modelo de Processamento** [֍]()
* **Considerações Finais** [֍](#considerações-finais)
* **Referências** [֍](#referências)

## INTRODUÇÃO À COMPUTAÇÃO DISTRIBUÍDA

*Voltar para **Seções*** [֍](#seções)

Com a acessibilização de Big Data - dados em alto volume, variedade e velocidade de geração -, novas soluções de processamento em larga escala se tornaram necessários, e daí surgem tecnologias de computação distribuída.

> *Máquinas sozinhas não têm energia e recursos suficientes para executar computações em quantidades enormes de informação (ou o usuário provavelmente não tem o tempo necessário para que a computação termine). Um **cluster**, ou grupo, de computadores, rateiam os recursos de várias máquinas juntas, fornecendo a capacidade de utilização de todos os recursos acumulados, como se fossem um único computador. Agora, um grupo de máquinas per se não é poderoso, é necessário um framework para coordenar trabalhos entre elas.* [^1]

### VISÃO GERAL DO HADOOP

Hadoop surge, na Google, como um framework *open-source* de computação e armazenamento distribuídos, baseado em escalabilidade horizontal e paralelismo entre os nós de um **cluster**. Seus principais componentes são:

* **HDFS (Hadoop Distributed File System)** : armazenamento de arquivos distribuídos no *cluster*. É composto de :
  * **NN - Name Node**
  * **DN - Data Node**

* **YARN (Yet Another Resource Negotiator)**: é o sistema operacional que gerencia os recursos do *cluster*, para onde as submissões de aplicações são enviadas. É composto de :
  * **RM - Resource Manager**
  * **NM - Node Manager**
  * **AM - Application Master**

* **MapReduce** : um modelo de programação, que também é um framework, inspirado em programação funcional, que busca facilitar a computação paralela e que processa dados em batch.

> *Como  reação a essa complexidade, nós desenvolvemos uma nova abstração que nos permite expressar as computações simples que buscávamos executar, mas oculta os detalhes confusos da paralelização, tolerância a falhas, distribuição de dados e balanceamento de carga em uma biblioteca. [...] Nós percebemos que a maioria das nossas computações envolviam aplicar uma operação **map** a cada registro lógico de nosso input, de modo a computar uma série de pares chave-valor intermediários e, então, aplicar uma operação **reduce** em todos os valores que partilham a mesma chave, de maneira a combinar os dados derivados apropriadamente.* [^2]

### VISÃO GERAL DO APACHE SPARK

#### MODELO DE PROCESSAMENTO

* **Modos de Execução (Execution Modes)**
  * Cliente
  * Cluster

* **Cluster Managers (Gerenciadores de Cluster)**
  * local [n]: simulação local de uma arquitetura client-driver, em que `n` é o número de threads disponibilizadas para o processo.
  * Standalone: execução por script ou manual de um cluster com uma interface web para gerenciamento.
  * YARN: gerenciador nativo Hadoop
  * Kubernetes
  * Apache Mesos

* **Execution Tools (Ferramentas de Execução)**
  * **IDE/Notebooks**
  * **Spark Submit**

#### TABLES X DATAFRAMES

|---|Spark Table|Spark DataFrame|
|---|:---:|:---:|
|***Schema***|On-Write|On-Read|
|***Armazenamento do Schema***|Metadata Store|Runtime Catalog|
|***Persistência***|Tabelas e metadata são acessíveis por aplicações diversas|DataFrame e Catalog são objetos acessíveis somente pela aplicação, durante seu tempo de execução|
|***Acesso***|SQL Expressions, não utiliza APIs|APIs, não utiliza SQL Expressions|
||||

Tanto os DataFrames quanto as Tables são objetos que podem ser convertidos entre si. A seguir, alguns dos métodos mais comuns de DataFrames, os quais podem ser subdividos em 3 categorias, de acordo com seus efeitos dentro do fluxo de processamento:

* **Funções (Functions)** : métodos sem as especificidades dos demais, recebe um input e retorna um output sem modificar a entrada inicial.

|Spark Built-In|Somente PySpark|
|:---|---:|
|cache|corr|
|createGlobalTempView|cov|
|createOrReplaceGlobalTempView|freqItems|
|createOrReplaceTempView|mapInPandas|
|explain|replace|
|printSchema|sameSemantics|
|toDF|semanticHash|
|toJSON|to_koalas|
|writeTo|to_pandas_on_spark|

* **Transformações (Transformations)** : produzem um novo DataFrame transformado, podendo sofrer alterações no número de linhas e/ou colunas.

|Exemplos||
|:---|---:|
|agg|alias|
|coalesce|colRegex|

* **Ações (Actions)** : operações que lançam a execução de um Spark Job e retornam, depois, para o Spark Driver. É a última operação de um encadeamento de métodos.

|Exemplos|
|:---|
|collect|
|count|
|describe|
|first|
|foreach|
|head|
|show|
|summary|
|tail|
|take|

## INTRODUÇÃO AO AWS GLUE

*Voltar para **Seções*** [֍](#seções)

## RECAPITULANDO A ANÁLISE FINAL

*Voltar para **Seções*** [֍](#seções)

Até então, a análise atual  **Contra-hegemonia no Cinema: Novas Perspectivas Afetivas na Era Pós-streaming**, utiliza os seguintes recortes :

* Filmes de países fora do eixo Europa Ocidental Colonial-EUA
* Exclusão de produções originais em inglês
* Período de lançamento entre 2013-2025
* Produções do gênero Romance

Abaixo, as perguntas selecionadas anteriormente:

* Qual a quantidade de filmes lançados anualmente, por região?
* Quais os 5 países com maior quantidade de filmes lançados? Desses países, quais línguas são mais utilizadas?
* Quais as atrizes/atores com maior atuação e em qual(is) língua(s)?
* Quais as 5 línguas com maior quantidade de títulos?
* Dentre os 100 títulos melhores votados, quais as nacionalidades das produções?
* Quais os tópicos mais recorrentes nas narrativas dos títulos selecionados?


### REFORMULAÇÃO DA ANÁLISE FINAL

*Voltar para **Seções*** [֍](#seções)

No entanto, o enfoque sofreu uma leve reformulação, na qual o elenco mais popular seria uma forma de representações do *ethos* dos novos referenciais afetivos, ao

### VISÃO GERAL DOS DADOS APÓS REINGESTÃO DO TMDB

*Voltar para **Seções*** [֍](#seções)

## DATA LAKE E TRUSTED ZONE

*Voltar para **Seções*** [֍](#seções)

### PROCESSAMENTO DE DADOS: ETAPA DE TRANSFORMAÇÃO PT. 1

*Voltar para **Seções*** [֍](#seções)

### VISÃO GERAL DA RAW ZONE

*Voltar para **Seções*** [֍](#seções)

### PREPARAÇÃO DO GLUE

*Voltar para **Seções*** [֍](#seções)

#### CRIAÇÃO DO ROLE

*Voltar para **Seções*** [֍](#seções)

Para a criação do IAM Role, foram mantidas as mesmas permissões utilizadas em outra tarefa.

![Role Glue Service](../evidencias/desafio/2-glue-role.png)

#### CRIAÇÃO DO CRAWLER E DATABASE

*Voltar para **Seções*** [֍](#seções)

### ANÁLISE DO SCRIPT DO GLUE JOB

*Voltar para **Seções*** [֍](#seções)

### EXECUÇÃO DO GLUE JOB

*Voltar para **Seções*** [֍](#seções)

## VISÃO GERAL DA TRUSTED ZONE

*Voltar para **Seções*** [֍](#seções)

## CONSIDERAÇÕES FINAIS

*Voltar para **Seções*** [֍](#seções)

## REFERÊNCIAS

*Voltar para **Seções*** [֍](#seções)

[^1]: CHAMBERS, ZAHARIA; 2018, p. 13

[^2]: DEAN, GHEMAWAT; 2008, p. 107
