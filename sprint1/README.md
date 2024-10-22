#

||
|---|
|![Banner](/assets/banner-sprint1.png)|
||

## RELATOS DE APRENDIZADO

| | | |
|:---|---|---:|
|**LINUX**|**NOTAS DE ESTUDO**|[![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white )](https://www.notion.so/Linux-Bash-11f0d30eb94d80e88db7df6abc848b61#1200d30eb94d8004b5f1db8f37bf2248)|
| | | |

Apesar de ter o Ubuntu instalado em meu PC pessoal, para tentar me habituar ao sistema por coerção, antes da sprint, eu tinha pouca familiaridade com o terminal. E confesso que uma certa curiosidade tingida de desconforto. Não o utilizava para nada além de instalações e atualizações de pacotes.  

Hoje, após experienciar o poder dos scripts e desmistificar o uso do terminal (não é tão difícil quanto parece!), sinto prazer em utilizá-lo, e tenho confiança em escrever rotinas mais básicas.  

Tenho interesse em continuar me aprofundando em Bash e melhorar meus códigos e habilidades com a linha de comando, interiorizando boas práticas e praticando com a automação de processos.  

Por meio de outros cursos complementares que fiz, aprendi que saber lidar com o terminal é essencial para uma utilização eficiente de muitos serviços de nuvem, nos quais o Linux se faz obíquo. Portanto, também procuro utilizar o AWS CLI em estudos pessoais para me ambientar e reforçar esse hábito.

No repositório [bash-playground](https://github.com/jqln-vc/bash-playground), comecei a compilar minhas práticas a partir de referências diversas.

| | | |
|:---|---|---:|
|**GIT & GITHUB**|**NOTAS DE ESTUDO**|[![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white )](https://www.notion.so/Git-1210d30eb94d80b296fafde3fbc00d20)|
| | | |

## DESAFIO

* [preparacao_ecommerce.sh](./desafio/preparacao_ecommerce.sh): script que cria o diretório `ecommerce`, localiza o arquivo `dados_de_vendas.csv` e o move para `ecommerce`
* [processamento_de_vendas.sh](./desafio/processamento_de_vendas.sh): script de tarefas de backup e geração de relatórios, possui as funções:
  * **vendas_backup**: criação dos diretórios `vendas` e `vendas/backup`, faz cópia de backup e nomeia os arquivos com data atual
  * **relatorio**: geração de relatórios
  * **compressao**: compressão de arquivo de backup
  * **limpeza_arquivos**: remoção de arquivos já processados
* [consolidador_de_processamento_de_vendas.sh](./desafio/consolidador_de_processamento_de_vendas.sh): script que consolida todos os relatórios gerados em um único relatório

## EVIDÊNCIAS

Na pasta `evidencias`, encontram-se prints referentes a momentos de execução do código, exemplificando abordagens adotadas para a conclusão do desafio.  
No passo a passo explicativo, encontrado na pasta `desafio`, serão comentados outros prints de pontos específicos.

### Etapa de Preparação em Ambiente Linux

Demonstração do ambiente utilizado, com o sistema Ubuntu. Na imagem abaixo, está sendo executada a preparação do ambiente `ecommerce`.

![Preparação](evidencias/1-preparacao.png)

### Fluxo de Atualizações de Código com Git

Demonstração das aplicações de versionamento de código aplicadas no projeto desta sprint. Na imagem abaixo, após o teste, foi feito o commit + push da versão do código com a função `vendas_backup` finalizada.

![Preparação](evidencias/2-commits.png)

## CERTIFICADOS

### Linux para Desenvolvedores (c/ Terminal, Shell, Apache e +)

*Ministrado por Matheus Battisti @ Udemy*

| |
|---|
|![Certificado-Linux](certificados/certificado-linux.jpg)|
||

### Git e GitHub do Básico ao Avançado (c/ Gist e GitHub Pages)

*Ministrado por Matheus Battisti @ Udemy*

| |
|---|
|![Certificado-Git](certificados/)|
||

## CERTIFICADOS COMPLEMENTARES

Para absorver melhor o conteúdo desta sprint e me aprofundar em pontos de interesse, concluí em paralelo os cursos abaixo.

### Git Going with Comparing, Branching and Merging

*Ministrado por Jason Taylor e John Myers @ Udemy*

| |
|---|
|![Certificado-Git](certificados/certificado-complementar-git.jpg)|
||

### Linux and Bash for Data Engineering

*Ministrado por Noah Gift, Alfredo Deza e Kennedy Behrman @ Coursera*

| |
|---|
|![Certificado-Comp-Bash](certificados/certificado-complementar-linux-bash.jpg)|
||

### Shell Scripting: Discover How to Automate Command Line Tasks

*Ministrado por Jason Cannon @ Udemy*

| |
|---|
|![Certificado-Comp-Bash](certificados/)|
||

## BIBLIOGRAFIA

* ALBING, Carl; VOSSEN, JP. **Bash Idioms: Write Powerful, Flexible, Readable Shell Scripts**. Sebastopol: O’Reilly, 2022.
* ALBING, Carl; VOSSEN, JP. **Bash Cookbook: Solutions and Examples for Bash Users**. Sebastopol: O’Reilly, 2018.
* BARRETT, Daniel. **Efficient Linux at the Command Line.** Sebastopol: O’Reilly, 2022.
