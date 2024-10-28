#

||
|---|
|![Banner](/assets/banner-sprint1-desafio.png)|
||

Para embasar algumas motivações no desenlvovimento do desafio, quando oportuno, serão trazidas referências da literatura; citações indicadas na seção [REFERÊNCIAS](https://github.com/jqln-vc/compass-academy/blob/main/sprint1/desafio/README.md#refer%C3%AAncias), e publicações indicadas na seção [BIBLIOGRAFIA](https://github.com/jqln-vc/compass-academy/blob/main/sprint1/README.md#bibliografia) no diretório `sprint1`.  

## PREPARAÇÃO DO AMBIENTE ECOMMERCE

Em ambiente Linux Ubuntu, foi realizado o download do arquivo `dados_de_vendas.csv` na pasta `/home`, a criação da pasta `ecommerce` e envio do arquivo para lá.

> :exclamation: A pasta `ecommerce` foi criada diretamente no repositório da trilha de aprendizado, já trackeada pelo Git, na subpasta `desafio`. No momento da execução da preparação do print abaixo, já haviam sido criados alguns arquivos.

| |
|---|
|![PreparaçãoParte1](../evidencias/1-preparacao.png)|
| |

Como o caminho completo até para a criação da pasta `ecommerce` é longo, e ele seria utilizado algumas vezes, foi criada uma variável para facilitar o processo.

```bash
    export repo_dir="/workspaces/compass-academy/sprint1/desafio"
```

Abaixo os comandos para criação da pasta `ecommerce` e movimentação da planilha para lá.

```bash
    # Uso de sudo para evitar quaisquer erros de permissão relacionados a outros (sub)diretórios.
    sudo mkdir -p "${repo_dir}/ecommerce"
    sudo mv dados_de_vendas.csv ${repo_dir}/ecommerce
```

### BÔNUS: preparacao_ecommerce.sh

Complementarmente, foi feita a automatização do procedimento acima no script `preparacao_ecommerce.sh`.

| |
|---|
|![Função de Preparaçao](../evidencias/3-ecommercefunc.png)|
| |

Confirmação de existência da pasta /ecommerce, antes da sua criação, caso a pasta já exista, a mensagem de confirmação é printada.

```bash
    [[ ! -d ${ECOMMERCE} ]] && mkdir ecommerce && echo ${ITEM1} || echo ${ITEM1}
```

Localização da planilha a partir do repositório atual, o output é direcionado com `xargs` para o deslocamento do arquivo para `/ecommerce` com `mv`.

> *Ao combinar `find` e `xargs`, utilize `xargs -0` [...] para proteção contra caracteres especiais nas strings de input. [...] Normalmente, `xargs` espera que as strings de input sejam separadas por espaços em branco, como caracteres de nova linha. Este é um problema quando as strings de input contém espaços, como arquivos com espaços no nome.*[^1]

```bash
    # Flag -0: muda os separadores de inputs, em vez de espaço, são utilizados valores null. Assim, um arquivo com espaço no nome não é tratado com 2 arquivos diferentes.

    # Flag -I <string>: controla onde o input será inserido no próximo comando, <string> funciona como um placeholder.

    find ${SELF_PATH} -name ${PLANILHA} 2> ${DESCARTE} | xargs -0 -I {} mv {} $ECOMMERCE/ 2> ${DESCARTE} \
    && echo -e "${ITEM2}\n" 
```

#### FLUXO DE LÓGICA

[//]: # (Caso não possua suporte para mermaid, sugiro abrir no site do GitHub para visualizar o grafo a seguir ou instalar extensão compatível)

```mermaid
graph LR
    A(/ecommerce) --> B{existe ?}
    B -- não --> C[mkdir ecommerce]
    B -- sim --> D(?/dados_de_vendas)
    C --> D
    D -- find | mv --> E[ecommerce/]
```

## PROCESSAMENTO DE VENDAS

A seguir serão comentadas as funções do script `processamento_de_vendas.sh`.

### FUNÇÃO vendas_backup

A função cria as pastas `vendas` e `/vendas/backup` dentro da pasta `/ecommerce`. Após a criação, copia a planilha de vendas para essas pastas, renomeando aquela referente ao backup.

| |
|---|
|![Vendas-Backup](../evidencias/8-vendas-backup.png)|
| |

Verificação da existência da pasta `/backup`, antes da criação e confirmação. Caso já exista, a confirmação de criação é enviada, sem nenhuma alteração.

```bash
    # ! -d: retorna True se o diretório não existir
    [[ ! -d $BACKUP ]] && mkdir -p ${BACKUP} && echo ${ITEM1} || echo ${ITEM1}
```

A seguir o passo a passo solicitado a cópia da planilha dentro dos diretórios `/vendas` e `/vendas/backup`. Seguida da renomeação para o padrão `backup-dados-YYYYMMDD.csv`.

```bash
    cp "${ECOMMERCE}/${PLANILHA}" "${VENDAS}" \
    && cp "${ECOMMERCE}/${PLANILHA}" "${BACKUP}/dados-${DATA}.csv" \
    && echo ${ITEM2} \
    && mv "${BACKUP}/dados-${DATA}.csv" "${BACKUP}/backup-dados-${DATA}.csv" 2> ${DESCARTE} \
    && echo -e "${ITEM3}\nBackup concluído com sucesso!\n"
```

#### FLUXO DE LÓGICA

[//]: # (Caso não possua suporte para mermaid, sugiro abrir no site do GitHub para visualizar o grafo a seguir ou instalar extensão compatível)

```mermaid
graph LR
    A((/ecommerce)) --> B(./vendas/backup)
    B --> C{existe ?}
    C -- não --> D[mkdir -p ./vendas/backup]
    B -- sim --> E(copiar e renomear dados_de_vendas)
    D -- && --> E
    E -- cp --> F[para /vendas]
    E -- cp --> G[para /backup/dados-DATA]
    G -- mv --> I[dados-DATA para backup-dados-DATA]
```

### FUNÇÃO relatorio

A função faz o processamento da planilha de vendas, extraindo alguns dados, e inserindo-os em um relatório em formato `txt`.

| |
|---|
|![Relatorio](../evidencias/9-relatorio.png)|
| |

Na pasta `/backup`, o relatório é criado e identificado com a data atual, no formato `YYYYMMDD`.

- **1ª inserção**: data e hora atual são inseridas no relatório, no formato `YYYY/MM/DD HH:MM`.

```bash
    # >  : direciona e insere, sobrescrevendo, um output ao local-alvo
    # >> : direciona e adiciona um output ao local-alvo  
    cd ${BACKUP} \
    && touch "relatorio-${DATA}.txt" \
    && echo ${DATA_HORA} >> "relatorio-${DATA}.txt" \
```

- **2ª inserção**: data da venda do 1º item

```bash
    # cut: corta a string em "campos" ou "seções"
        # -d ',': indica o delimitador a considerar no corte
        # - f 5: após cortado, indica o campo de interesse, neste caso, corresponde à 5ª coluna
    # sed: edita um streaming de strings
        # -n: indica quais linhas serão consideradas
        # '2p': imprime a 2ª linha (p --> print)
    cut -d ',' -f 5 backup*.csv | sed -n '2p' >> "relatorio-${DATA}.txt" 2> ${DESCARTE}
```

- **3ª inserção**: data da venda do último item

```bash
    # tail: retorna, por padrão, as 10 últimas linhas
        # -n '1': retorna somente 1 linha, a última
    cut -d ',' -f 5 backup*.csv | tail -n 1 >> "relatorio-${DATA}.txt" 2> ${DESCARTE}
```

- **4ª inserção**: contagem de itens distintos vendidos

```bash
    # cut: seleção da 2ª coluna
    # sed '1d': deleta a 1ª linha, de colunas
    # sort: ordena os itens (necessários pois uniq conta somente itens distintos adjacentes)
    # uniq -c: contagem de itens distintos
    cut -d ',' -f 2 backup*.csv | sed '1d' | sort | uniq -c | wc -l >> "relatorio-${DATA}.txt" 2> ${DESCARTE}
```

- **5ª inserção**: listagem dos 10 primeiros itens (desconsiderando a linha de colunas)

```bash
    sed '1d' backup*.csv | head -n 10 >> "relatorio-${DATA}.txt" \
    && echo >> "relatorio-${DATA}.txt" \
    && echo -e "${ITEM4}\n"
```

#### FLUXO DE LÓGICA

[//]: # (Caso não possua suporte para mermaid, sugiro abrir no site do GitHub para visualizar o grafo a seguir ou instalar extensão compatível)

```mermaid
graph LR
    A((/backup)) --touch--> B(relatório)
    B -- echo --> C[DATAHORA >> relatório]
    C -- && --> D
    D(backup-dados) -- cut | sed --> E[1ª data >> relatório]
    D -- cut | tail --> F[última data >> relatório]
    D -- cut | sed | sort | uniq | wc --> G[qtd itens distintos >> relatório]
    D -- sed | heac --> H[10 itens >> relatório]    
```

### FUNÇÃO compressao

A função é executada no diretório `/backup`, comprimindo o arquivo de backup do dia em um arquivo compactado `.zip`.

| |
|---|
|![Compressão](../evidencias/10-compressao.png)|
| |

```bash
    # A variável DATA contém a data atual do momento de execução, no formato YYYYMMDD
    cd ${BACKUP} \
    && zip "backup-dados-${DATA}.zip" "backup-dados-${DATA}.csv" \
    && echo -e "${ITEM5}\n"
```

#### FLUXO DE LÓGICA

[//]: # (Caso não possua suporte para mermaid, sugiro abrir no site do GitHub para visualizar o grafo a seguir ou instalar extensão compatível)

```mermaid
graph LR
    A((/backup))--> B(backup-dados)
    B -- zip --> C[compressão de backup-dados]

```

### FUNÇÃO limpeza_arquivos

A função faz a remoção dos arquivos `.csv` da pasta `/vendas` e `/backup`, após seu processamento em um relatório `.txt` e backup compactado em `.zip`.

| |
|---|
|![Limpeza Arquivos](../evidencias/11-limpeza-arquivos.png)|
| |

```bash
    # Uso de wildcard (*) para considerar arquivos com quaisquer datas no nome, e a extensão para garantir que não sejam removidos os arquivos compactados.
    rm -f ${BACKUP}/backup*.csv \
    && rm -f ${VENDAS}/dados*.csv \
    && echo -e "${ITEM6}\n"
```

#### FLUXO DE LÓGICA

[//]: # (Caso não possua suporte para mermaid, sugiro abrir no site do GitHub para visualizar o grafo a seguir ou instalar extensão compatível)

```mermaid
graph LR
    A((/backup))-- rm --> B(backup-dados)
    C((/vendas))-- rm --> D(dados)
    A -- && --> C
```

## CONSOLIDAÇÃO DO PROCESSAMENTO DE VENDAS

O script `consolidador_de_processamento_de_vendas.sh` une todos os relatórios gerados, em ordem cronológica, em um único relatório final.

### FUNÇÃO consolidacao 

A função é executada dentro do diretório `/backup`, primeiramente localiza todos os arquivos de relatório que tenham o nome dentro do padrão `relatorio-YYYYMMDD.txt`, organiza os arquivos em ordem crescente, e copia seu conteúdo para um arquivo `relatório-final.txt`. 

Para garantir que o próprio relatório final não fosse passado pelo pipeline (isso estava acontecendo), foi usado RegEx para garantir o padrão.

| |
|---|
|![Consolidação](../evidencias/13-consolidador.png)|
| |

```bash
    # grep -E: utiliza extended regex
    # [0-9]{8}: aceita somente 8 dígitos
    find . -name "relatorio*.txt" | grep -E 'relatorio-[0-9]{8}\.txt' | sort | xargs -0 -I {} cat {} >> relatorio-final.txt 2> ${DESCARTE}
```

#### FLUXO DE LÓGICA

[//]: # (Caso não possua suporte para mermaid, sugiro abrir no site do GitHub para visualizar o grafo a seguir ou instalar extensão compatível)

```mermaid
graph LR
    A((/backup))-- find --> B(relatorio*.txt)
    B-- xargs cat --> C(relatorio-final.txt)
```

#### EXECUÇÃO

| |
|---|
|![Execução Consolidação](../evidencias/16-execucao-consolidador.gif)|
| |

> :exclamation: O relatório gerado durante a gravação do vídeo foi mantido na pasta `backup`, porém não foi considerado na execução do script de consolidação.

## AGENDAMENTO DE ROTINAS: CRONTAB

O agendamento da rotina de execução do script de processamento foi feito por meio do programa `crontab`, com a configuração do arquivo feita com o editor de texto Nano.

| |
|---|
|![CronTab](../evidencias/4-crontab.png)|
| |

> :exclamation: O script foi executado nos dias 22, 24, 25 e 26 de outubro. No dia 23, não foi possível executá-lo por motivos de força maior (desatenção ao estar em horário de reunião), portanto, o agendamento abrange os dias necessários para geração dos 4 relatórios.

Antes de utilizar o programa, foi necessário fazer sua instalação e alterar o horário do sistema, que estava com o fuso UTC. Abaixo os comandos utilizados no terminal para esta etapa.

```bash
    # Configuração do fuso horário do sistema
    sudo ln -sf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

    # Configuração dos agendamento, abre o editor de texto
    crontab -e

    # Ativação do programa
    sudo cron service start
```

### EXECUÇÃO DE CRON JOB

---

![AI-Dataset](../evidencias/15-execucao-cron.gif)

---

## GERAÇÃO DE DATASET PARA RELATÓRIOS SUBSQUENTES

Segue abaixo o prompt utilizado com o modelo Claude 3.5 Sonnet para gerar linhas adicionais, buscando manter a sequência de ids e ordem cronológica, produtos dentro da mesma temática e repetições ocasionais de itens, para testar a função `relatorio` nestas situações.

---

| |
|---|
|![AI-Dataset](../evidencias/5-geracao-dataset.png)|
| |

> ! O arquivo com os dados gerados foi mantido na pasta `/ecommerce`, nomeado `dados_adicionais.csv`.

---

## METODOLOGIA UTILIZADA

Os scripts foram desenvolvidos priorizando a modularização dos processos em funções, adotando boas práticas de documentação, legibilidade, reusabilidade e tratamento de erros.

### CABEÇALHO E SECCIONAMENTO

> *Para a organização e legibilidade do código, quebre ações em seções*.[^2]

No cabeçalho, além da linha de chamada do interpretador ***bash***, encontram-se informações de identificação, autoria e data, e descrição sobre a utilidade do script.

| |
|---|
|![Cabeçalho](../evidencias/6-cabecalho.png)|
| |

Seção inicial do script, com definição de variáveis globais.

| |
|---|
|![Variáveis](../evidencias/7-variaveis.png)|
| |

### VARIÁVEIS SEMÂNTICAS

O exemplo acima, a seção de definição de variáveis globais, incorpora escolhas semânticas que otimizam a leitura e compreensão do código.

> *Nomear é importante [...] reduzindo erros no código, e no futuro ao reler, debugar e aprimorar.*[^3]

### CONTROLE DE FLUXO

Para os controles de fluxo, foi priorizada a escrita simplificada, sem a utilização explícita de `if` e `then`, para otimizar a legilibilidade do código.

> *[...] para situações de teste e checagem de ações simples, usar **&&** e **||** pode ser muito conveniente e não desviará a atenção do fluxo de lógica principal.*[^4]

| |
|---|
|![Pipeline](../evidencias/12-main.png)|
| |

O encadeamento lógico de comandos foi utilizado com a técnica de ***piping***, utilizando o output de um comando para ser o input da função seguinte. Além disso, também foi aplicado com condicionais encadeadas `&&`, assegurando a **atomicidade** das execuções, ou seja, ou todos os comandos de determinado bloco lógico são executados em conjunto, ou nenhum será.

Já a utilização de quebras de linha com `\` é uma adoção inspirada em estilos utilizados atualmente pela comunidade, também uma contribuição para legibilidade em linhas mais extensas.

### TRATATIVAS DE ERRO

> *Mensagens de erro devem ir para STDERR, como echo "Algo ruim aconteceu" 1>&2.*[^5]

Nos comandos suscetíveis à geração de erros, foi feita a tratativa com a abordagem a seguir:

```bash
DESCARTE="/dev/null"
2> $DESCARTE
```

## MELHORIAS A FAZER

- [x] **Remover dependência dos scripts ao caminho absoluto do ambiente virtual de execução**  
Devido à execução do crontab a partir da raíz, inicialmente foram utilizados caminhos absolutos para contornar criações errôneas de pastas e arquivos durante os cron jobs.  
Com uma alteração no agendamento no cron, foi possível adotar o caminho `SELF_PATH` partindo do diretório atual, assegurando assim a portabilidade do código.

```bash
    # agendamento no crontab
    27 15 * * * 1-6 cd /workspaces/compass-academy/sprint1/desafio && ./processamento_de_vendas.sh

    # declaração de variável global de caminho
    SELF_PATH=$(pwd)
```

- [ ] **Adicionar função que recebe argumento `help` para printar instruções de utilização da funções do(s) script(s)**.

- [ ] **Receber nome da planilha de vendas (ex. "dados_de_vendas.csv") como argumento na linha de comando.**
Alteração já realizada no script `preparacao_ecommerce`.

- [ ] **Execução de funções separadamente a partir de chamada por argumento na linha de comando.**

---

## REFERÊNCIAS

[^1]: BARRETT, 2022, p. 122
[^2]: ALBING, VOSSEN, 2022, p. 27
[^3]: Ibid., p.127
[^4]: Ibid., p. 7
[^5]: Ibid., p. 132
