#

||
|---|
|![Banner](/assets/banner-sprint10-desafio.png)|
||

## SEÇÕES

* **Revisitando o Projeto Dramance** [֍]()
  * **Questões Norteadoras para a Análise** [֍]()
  * **Revisão Crítica das Implementações Atuais** [֍]()
    * **Testes de Modelos e Processamentos em GPU** [֍]()
    * **Ineficácia do Uso de UDFs para Pipelines de LLMs** [֍]()
* **Arquitetura de Transformers** [֍]()
* **Considerações Finais** [֍](#considerações-finais)
* **Referências** [֍](#referências)

## REVISITANDO O PROJETO DRAMANCE

*Voltar para **Seções*** [֍](#seções)

> *A **Análise do Discurso** visa fazer compreender como os objetos simbólicos produzem sentidos, analisando assim os próprios gestos de interpretação que ela considera como atos no domínio simbólico, pois eles intervêm no real do sentido. A **Análise do Discurso** não estaciona na interpretação, trabalha seus limites, seus mecanismos, como parte dos processos de significação. [...] Não há uma verdade oculta atrás do texto. Há gestos de interpretação que o constituem e que o analista, com seu dispositivo, deve ser capaz de compreender.* (ORLANDI, 2015, p. 26)

> *Em suma, a **Análise do Discurso** visa a compreensão de como um objeto simbólico produz sentidos, como ele está investido de significância para e por sujeitos*. (ORLANDI, 2015, p. 26)

> *Gostaríamos de acrescentar que como a pergunta é de responsabilidade do pesquisador, é essa responsabilidade que organiza sua relação com o discurso, levando-o à construção de "seu" dispositivo analítico, optando pela mobilização desses ou aqueles conceitos, esse ou aquele procedimento, com os quais ele se compromete na resolução de sua questão.* (ORLANDI, 2015, p. 27)

> *O que são pois as condições de produção? Elas compreendem fundamentalmente os sujeitos e a situação. Também a memória faz parte da produção do discurso. [...] Podemos considerar as condições de produção em sentido estrito e temos as circunstâncias da enunciação: é o contexto imediato. E se as considerarmos em sentido amplo, as condições de produção incluem o contexto sócio-histórico, ideológico.** (ORLANDI, 2015, p. 30)



### QUESTÕES NORTEADORAS PARA A ANÁLISE

### REVISÃO CRÍTICA DAS IMPLEMENTAÇÕES ATUAIS

*Voltar para **Seções*** [֍](#seções)

Em vista das dificuldades de implementação das inferências de LLMs na análise passada, com tempos de execução elevados para os Glue Jobs, uma das prioridades foi identificar pontos de melhoria no pipeline de dados, detalhados a seguir.

#### TESTES DE MODELOS E PROCESSAMENTOS EM GPU

#### INEFICÁCIA DO USO DE UDFs PARA PIPELINES DE LLMs

* Os modelos são carregados separadamente para cada *worker*
* UDFs são inicializados a cada linha, não utilizando processamentos em batch
* UDFs não utilizam GPUs de maneira eficaz

## REVISÃO DO CICLO DE VIDA DA ENGENHARIA DE DADOS

*Voltar para **Seções*** [֍](#seções)

![Visão Geral Engenharia de Dados](../evidencias/17-visao-geral-engenharia-dados.png)

## PROCESSAMENTO DE DADOS: PREPARO DOS DATASETS PARA ANALYTICS

*Voltar para **Seções*** [֍](#seções)

### INTRODUÇÃO AO AMAZON QUICKSIGHT

*Voltar para **Seções*** [֍](#seções)

Para o consumo dos dados processados nas etapas anteriores do fluxo do data lake, foi utilizado o serviço de BI (Business Intelligence) *serverless* Amazon QuickSight. O serviço permite a integração de datasets provenientes de diversas fontes de dados, possibilitando a relação entre tabelas e a criação de dashboards interativos e compartilhados entre diversos usuários, com atualização em tempo real e capacidade de utilização de modelos de aprendizado de máquina para inferências até mesmo em linguagem natural.

A integração com os dados foi realizada a partir das tabelas identificadas com o Glue Crawler e mapeadas no Glue Data Catalog, assim o acesso com o QuickSight teve o Athena como *data source*. Abaixo a configuração do dataset `dramance_data` :

![Data Source Athena](../evidencias/8-dataset-dramance-qs.png)

### RELAÇÕES ENTRE TABELAS: FATO, DIMENSÃO E BRIDGE

*Voltar para **Seções*** [֍](#seções)

![Join de Tabelas Dimensão, Bridge e Fato](../evidencias/2-joins-tabelas-qs.png)

### COMPREENSÃO DOS DADOS UTILIZADOS

*Voltar para **Seções*** [֍](#seções)

### TRATAMENTO DE DADOS DO DATASET: CONVERSÃO DE BOOLEANOS

*Voltar para **Seções*** [֍](#seções)

Nas colunas `conteudo_sexual` e `sexismo`, os valores booleanos estavam representados como inteiros, sendo `1` para "sim" e `0` para "não". Tais valores podem ser utilizados nesse formato, no entanto, não incorporam a semântica necessária para a compreensão imediata em legendas e nos gráficos.

Para facilitar, foi utilizada um estrutura condicional para converter tais valores para `Yes` e `No` (como o dataset já possuía seus valores originais em inglês, foi mantido o padrão).

![Conversão Booleanos por Condicional](../evidencias/7-edicao-colunas-subst-booleanos.png)

Após a criação das novas colunas modificadas, estas tiveram seu nome alterado para o anterior, `conteudo_sexual` e `sexismo` , e as antigas foram renomeadas e removidas do dataset.

## FLUXO DOWNSTREAM DO DATA LAKE: CONSUMO DOS DADOS

*Voltar para **Seções*** [֍](#seções)

Nesta etapa, após a preparação inicial do dataset e a integração de tabelas com seus devidos relacionamentos, foi desenvolvido o dashboard final que consolida a análise proposta em um relatório visualmente enriquecido com os padrões identificados nos dados.

Buscando responder às perguntas iniciais, encontrando respostas não esperadas, esta etapa de visualização de dados se aproxima ao design, à redação criativa e à pesquisa.

É preciso entender o tema que se estuda, é preciso entender as motivações iniciais da pesquisa e, mais importante, é preciso entender quem não estava presente durante o processo e estará vendo tudo pela primeira vez.

### CONTRA-HEGEMONIA NO CINEMA: SEMÂNTICAS AFETIVAS NA ERA PÓS-STREAMING

*Voltar para **Seções*** [֍](#seções)

A pesquisa desenvolvida no projeto Dramance de Data Lake e Engenharia de Dados foi baseada na análise norteadora intitulada **Contra-Hegemonia no Cinema: Semânticas Afetivas na Era Pós-Streaming**. Antes de prosseguir com a apresentação dos dados no dashboard, é essencial destrinchar as intenções evidenciadas no título e as perguntas às quais buscou-se responder.

> *[...] a elocução (lexis), que não diz respeito à palavra oral, mas à redação escrita do discurso, ao estilo.* (REBOUL, 2004, p. 43)

> *O **ethos** é o caráter que o orador deve assumir para inspirar confiança no auditório, pois, sejam quais forem seus argumentos lógicos, eles nada obtêm sem essa confiança.* (REBOUL, 2004, p. 48)

> *O **pathos** é o conjunto de emoções, paixões e sentimentos que o orador deve suscitar no auditório com seu discurso. [...] Aqui o **ethos** já não é o caráter (moral) que o orador deve assumir, mas o caráter (psicológico) dos diferentes públicos, aos quais o orador deve adaptar-se.* (REBOUL, 2004, p. 48)

> *A linguagem é um fenômeno extremamente complexo, que pode ser estudado de múltiplos pontos de vista, pois pertence a diferentes domínios. É, ao mesmo tempo, individual e social, física, fisiológica e psíquica.* (FIORIN, 1998, p. 8)

> *O campo das determinações inconscientes é a semântica discursiva, pois o conjunto de elementos semânticos habitualmente usado nos discursos de uma dada época constitui a maneira de ver o mundo numa dada formação social. Esses elementos surgem a partir de outros discursos já construídos, cristalizados e cujas condições de produção foram apagadas. [...] A semântica discursiva é o campo da determinação ideológica propriamente dita. Embora esta seja inconsciente, também pode ser consciente.* (FIORIN, 1998, p. 19)

> *[...] dois discursos podem trabalhar com os mesmos elementos semânticos e revelar duas visões de mundo completamente diferentes, porque o falante pode dar valores distintos aos elementos semânticos que utiliza. Alguns são considerados eufóricos, isto é, são valorizados positivamente; outros, disfóricos, ou seja são valorizados negativamente.* (FIORIN, 1998, p. 21)

> *Tema é o elemento semântico que designa um elemento não-presente no mundo natural, mas que exerce o papel de categoria ordenadora dos fatos observáveis. São temas, por exemplo, amor, paixão, lealdade, alegria. Figura é o elemento semântico que remete a um elemento do mundo natural: casa, mesa, mulher, rosa, etc. A distinção entre ambos é, pois, de maior ou menor grau de concretude [...] concreto e abstrato são dois pólos de uma escala que comporta toda espécie de gradação. [...] O discurso figurativo é a concretização de um discurso temático. Para entender um discurso figurativo é preciso, pois, antes de mais nada, apreender o discurso temático que subjaz a ele.* (FIORIN, 1998, p. 24)

> *A esse conjunto de ideias, a essas representações que servem para justificar e explicar a ordem social, as condições de vida do homem e as relações que ele mantém com os outros homens é o que comumente se chama **ideologia**.* (FIORIN, 1998, p. 28)

> *Podemos então afirmar que não há um conhecimento neutro, pois ele sempre expressa o ponto de vista de uma classe a respeito da realidade. Todo conhecimento está comprometido com os interesses sociais. Esse fato dá uma dimensão mais ampla ao conceito de ideologia; ela é uma "visão de mundo", ou seja, o ponto de vista de uma classe social a respeito da realidade, a maneira como uma classe ordena, justifica e explica a ordem social.*  (FIORIN, 1998, p. 29)

> *Há, portanto, dois momentos essenciais na passagem da semântica fundamental à semântica narrativa: a seleção dos valores, articulados nos quadrados semióticos, e a relação com os sujeitos. A escolha de valores corresponde a uma primeira decisão do sujeito da enunciação, quanto ao discurso que será produzido. A atualização dos valores ocorre, como visto, no enunciado de estado, em que o valor é investido no objeto e relacionado, por disjunção ou conjunção, com o sujeito.* (BARROS, 2001, p. 45)

> *Na análise do discurso, procura-se compreender a língua fazendo sentido, enquanto trabalho simbólico, parte do trabalho social geral, constitutivo do homem e da sua história.* (ORLANDI, 2015, p. 15)

> *[...] podemos dizer que o sentido não existe em si mas é determinado pelas posições ideológicas colocadas em jogo no processo sócio-histórico em que as palavras são produzidas. As palavras mudam de sentido segundo as posições daqueles que as empregam.* (ORLANDI, 2015, p. 42)

> *O que interessa primordialmente ao analista são as propriedades internas ao processo discursivo: condições, remissão a formações discursivas, modo de funcionamento. [...] Discursos, a priori, não tidos como políticos, podem estar funcionando como tal.* (ORLANDI, 2015, p. 86)

#### RECORTES DE CLASSIFICAÇÃO TEXTUAL: CONTEÚDO SEXUAL E SEXISMO

*Voltar para **Seções*** [֍](#seções)

|||
|---|---|
|![Gráficos Donuts Conteúdo Sexual/Sexismo](../evidencias/5-inferencias-conteudo-sexual-sexismo-graphs.png)|![Config Conteúdo Sexual/Sexismo](../evidencias/6-inferencias-conteudo-sexual-sexismo-configs.png)|
|||

#### RECORTES GEOGRÁFICOS

*Voltar para **Seções*** [֍](#seções)

Dentre os filmes do dataset, é possível visualizar a localização no mapa das regiões--

|||
|---|---|
|![Gráfico Geográfico Pontos Mapa](../evidencias/3-points-on-map-graph.png)|![Config Geográfico Pontos Mapa](../evidencias/4-points-on-map-config.png)|
|||

#### RECORTES TEMPORAIS

*Voltar para **Seções*** [֍](#seções)

|||
|---|---|
|![Gráfico Funnel Lançamentos por Ano](../evidencias/12-lancamentos-anuais-graph.png)|![Config Funnel Lançamentos por Ano](../evidencias/13-lancamentos-anuais-config.png)|
|||

#### RECORTES POR MÉTRICAS DE AVALIAÇÕES E POPULARIDADE

*Voltar para **Seções*** [֍](#seções)

|||
|---|---|
|![Gráfico Gauge Média Avaliações](../evidencias/14-gauge-media-avaliacoes-graph.png)|![Config Gauge Média Avaliações](../evidencias/15-gauge-media-avaliacoes-config.png)|
|||

|||
|---|---|
|![Gráfico KPI Popularidade](../evidencias/10-popularidade-media-graph.png)|![Config KPI Popularidade](../evidencias/11-popularidade-media-config.png)|
|||

#### RECORTES LINGUÍSTICOS

## VISÃO PANORÂMICA DA ARQUITETURA E COMPONENTES DO DATA LAKE

*Voltar para **Seções*** [֍](#seções)

![Arquitetura final do Data Lake](../evidencias/)

## CONSIDERAÇÕES FINAIS

*Voltar para **Seções*** [֍](#seções)

Para uma compreensão de especificidades discursivas relativas às diferentes culturas, seria preciso buscar um comparativo nos discursos dos filmes excluídos no recorte inicial. Seriam os termos lexicais recorrentes um reflexo de simbologias afetivas inerentemente humanas, desejos e referentes partilhados por todos independentemente da cultura? Ou existiriam novas formas de figurativizar os temas da dimensão emocional, do *pathos*, quando migramos para outras vivências sociais?

A globalização facilita o contato com outras culturas, assim podemos vislumbrar novos modos de criar a realidade, no entanto, essa é uma faca de dois gumes, pois com o passar do tempos, as diferenças também estão sujeitas à normalização, dando espaço a novos padrões globais e um apagamento cultural.

## REFERÊNCIAS

*Voltar para **Seções*** [֍](#seções)
