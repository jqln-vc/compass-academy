#

||
|---|
|![Banner](/assets/banner-sprint1.png)|
||

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

## BIBLIOGRAFIA

ALBING, Carl; VOSSEN, JP. **Bash Idioms: Write Powerful, Flexible, Readable Shell Scripts**. Sebastopol: O’Reilly, 2022.

BARRETT, Daniel. **Efficient Linux at the Command Line.** Sebastopol: O’Reilly, 2022.
