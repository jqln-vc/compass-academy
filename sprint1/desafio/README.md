#

||
|---|
|![Banner](/assets/banner-sprint1-desafio.png)|
||

Para embasar algumas motivações no desenlvovimento do desafio, quando oportuno, serão trazidas referências da literatura; citações indicadas na seção [REFERÊNCIAS](https://github.com/jqln-vc/compass-academy/blob/main/sprint1/desafio/README.md#refer%C3%AAncias), e publicações indicadas na seção [BIBLIOGRAFIA](https://github.com/jqln-vc/compass-academy/blob/main/sprint1/README.md#bibliografia) no diretório `sprint1`.  

## PREPARAÇÃO DO AMBIENTE ECOMMERCE

Em ambiente Linux Ubuntu, foi realizado o download do arquivo `dados_de_vendas.csv` na pasta `/home`, a criação da pasta `ecommerce` e envio do arquivo para lá.

> [!NOTE]
> A pasta `ecommerce` foi criada diretamente no repositório da trilha de aprendizado, já trackeada pelo Git, na subpasta `desafio`. No momento da execução da preparação do print abaixo, já haviam sido criados alguns arquivos.

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
# uso de sudo para evitar quaisquer erros de permissão relacionados a outros (sub)diretórios
sudo mkdir -p "${repo_dir}/ecommerce"
sudo mv dados_de_vendas.csv ${repo_dir}/ecommerce
```

### BÔNUS: preparacao_ecommerce.sh
Complementarmente, foi feita a automatização do procedimento acima no script `preparacao_ecommerce.sh`.

| |
|---|
|![Função de Preparaçao](../evidencias/3-ecommercefunc.png)|
| |

#### FLUXO DA LÓGICA UTILIZADA

```mermaid
graph LR
    A(/ecommerce) --> B{existe ?}
    B -- não --> C[mkdir ecommerce]
    B -- sim --> D[echo ...sucesso!]
    C --> D
    E(?/dados_de_vendas) -- find | mv --> F[ecommerce/]
    D --> E
    F --> G[echo ...sucesso!]
```

## PROCESSAMENTO DE VENDAS
A seguir serão comentadas as funções do script `processamento_de_vendas.sh`.

### FUNÇÃO vendas_backup

#### FLUXO DA LÓGICA UTILIZADA

```mermaid
graph LR
    A[cd ecommerce] --> B(./vendas/backup)
    B --> C{existe ?}
    C -- não --> D[mkdir -p ./vendas/backup]
    B -- sim --> E[echo ...sucesso!]
    D --> E
    E --> F[cp dados_de_vendas ./vendas]
    F --> G[cp dados_de_vendas ./vendas/backup]
    G --> I[mv ./vendas/dados]

```

## AGENDAMENTO DE ROTINAS: CRONTAB

O agendamento da rotina de execução do script de processamento foi feito por meio do programa `crontab`, com a configuração do arquivo feita com o editor de texto Nano.

| |
|---|
|![CronTab](../evidencias/4-crontab.png)|
| |

> [!NOTE]
> O script foi executado nos dias 22, 24, 25 e 26 de outubro. No dia 23, não foi possível executá-lo por motivos de força maior (desatenção ao estar em horário de reunião), portanto, o agendamento abrange os dias necessários para geração dos 4 relatórios.

Antes de utilizar o programa, foi necessário fazer sua instalação e alterar o horário do sistema, que estava com o fuso UTC. Abaixo os comandos utilizados no terminal para esta etapa.

```bash
# Configuração do fuso horário do sistema
sudo ln -sf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

# Configuração dos agendamento, abre o editor de texto
crontab -e

# Ativação do programa
sudo cron service start
```

## METODOLOGIA UTILIZADA

Os scripts foram desenvolvidos priorizando a modularização dos processos em funções, adotando boas práticas de documentação, legibilidade, reusabilidade e tratamento de erros.

### CABEÇALHO E SECCIONAMENTO

> Para a organização e legibilidade do código, quebre ações em seções. [^X] 27

### CONTROLE DE FLUXO

Para os controles de fluxo, foi priorizada a escrita simplificada, sem a utilização explícita de `if` e `then`, para otimizar a legilibilidade do código.

IMAGEM DE IFS

> *[...] para situações de teste e checagem de ações simples, usar **&&** e **||** pode ser muito conveniente e não desviará a atenção do fluxo de lógica principal.*[^X] 7

Ademais, o encadeamento lógico de comandos com `&&` assegura a **atomicidade** das execuções, ou seja, ou todos os comandos de determinado bloco lógico são executados em conjunto, ou nenhum será. Já a utilização de quebras de linha com `\` é uma adoção inspirada em estilos utilizados atualmente pela comunidade.

### TRATATIVAS DE ERRO

IMAGEM DE STERR

> *Mensagens de erro devem ir para STDERR, como echo "Algo ruim aconteceu" 1>&2.* [^] 132

Nos comandos que poderiam gerar erros potenciais, foi feita a trativa com a abordagem a seguir:

```bash
DESCARTE="/dev/null"
2> $DESCARTE
```

## PONTOS DE MELHORIA NO CÓDIGO

* **Função de input para nome de arquivo e caminhos**  
O script está dependente das variáveis de caminho e nome de arquivo declaradas no próprio código, isso prejudica a portabilidade e sua utilização em outros ambientes.

---

## REFERÊNCIAS

[^X] ALBING, VOSSEN, 2022, p. 7
[^X] ALBING, VOSSEN, 2022, p. 27
