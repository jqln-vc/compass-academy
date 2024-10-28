#

| |
|---|
|![Banner](../assets/banner-guide02.png)|
| |

## Configuração do Git

Informações de usuário relacionadas a todas as operações realizadas localmente, também aparecem nos commits no GitHub.

Configurar um nome para identificar autoria no histórico de versões:

```bash
    git config --global user.name “[nome sobrenome]”
```

Desconfigurar todos os nomes:

```bash
    git config --global --unset-all user.name
```

Configurar email que será associado ao seu idenficador do histórico:

```bash
    git config --global user.email “[email-valido]”
```

Desconfigurar todos os emails:

```bash
    git config --global --unset-all user.email
```

Configurar coloração automática Git na linha de comando Git:

```bash
    git config --global color.ui auto
```

## Ambiente local x ambiente remoto

![Estados Git](/assets/guide-git01.png)

## Preparando o ambiente Git

Preparando o ambiente local e criando um novo repositório Git (um diretório local trackeado pelo sistema de versionamento).

### Partindo do diretório local

Criar diretório do projeto e, dentro dele, rodar os comandos para inicializar o repositório e conectá-lo ao ambiente remoto no GitHub:

```bash
    # Cria o diretório .git/
    git init

    # Criar um arquivo README.md e adicioná-lo ao stage (add)
    # Um repositório não pode estar vazio
    echo "# teste" >> README.md
    git add README.md

    # Adicionando o arquivo ao .git/
    git commit -m "first commit"

    # Nomear a branch local principal como main (ou master)
    git branch -M main

    # Adicionar a origem remota à branch main local, o endereço é um repositório já criado no site GitHub

    git remote add origin git@github.com:jqln-vc/teste.git # SSH
    git remote add origin https://github.com/jqln-vc/teste.git # HTTPS

    # Fazer o push da criação local com a main na origem
    git push -u origin main
```

### Partindo do GitHub

Também é possível clonar um repositório já existente no GitHub diretamente no ambiente local, no diretório atual:

```bash
    git clone [url]
```

## Comandos Rotineiros

```bash

    # Atualizar o repo local com a branch master
git pull

    # Atualizar branch atual com dados de branchX, se omitir a branch, puxa da origin
    git fetch [branchX]

    # Criar uma ramificação isolada da master e mudar para ela
    git checkout -b [branch-isolada]

    # Checar arquivos modificados, comitados e/ou não trackeados
    git status

    # Adicionar arquivos modificados para o stage (próximo commit)
    git add .

    # Remover arquivos do trackeamento
    git rm [arquivo]

    # Enviar arquivos adicionados ao stage, já alterados, para serem adicionados à master 
    git commit -a -m “feitas alterações em XYZ”

    # "Empurrar" as alterações já comitadas na branch local para a master
    git push
```

## Ramificando com ***branches***

Trabalhar em *branches* é importante para isolar as modificações sendo desenvolvidas, sem afetar o bom funcionamento da `branch master` de produção.

Sempre que criar uma `branch` para começar a desenvolver algo, certificar-se de **ANTES** dar `git pull` puxando sempre o código mais atualizado da `master`, antes de mudar de `branch`.

> **HEAD**  
> *Em qualquer momento, você estará observando uma versão específica do seu projeto. Logo, você estará em uma branch específica [...] HEAD é simplesmente um ponteiro que te indica em qual branch você está.*  
> SKOULIKARI, 2023, p. 55

---

```bash
    # Listar as branches, um * aparecerá ao lado da branch ativa
    git branch

    # Criar uma nova branch no commit atual
    git branch [nome-da-branch]

    # Mudar para outra branch e carregá-la no seu diretório de trabalho
    git checkout [nome-da-branch]

    # Criar branch e mudar para ela, carregando-a no seu diretório de trabalho
    git checkout -b [nome-da-branch]

    # Fazer a união do histórico da branch especificada com a branch atual
    git merge [branch-alteracoes]
```

Resetar todas as configurações feitas, todas as alterações, commitadas ou não, serão removidas:

```bash
    # Resetar e retomar o estado inicial de acordo com a master
    git reset --hard origin/master
```

Sempre que estiver trabalhando em uma `branch`, certificar-se de fazer o `commit` de **TODAS** as alterações nesta `branch`, antes de fazer o checkout para a `master` (caso seja necessário).  

Assim elas continuam isoladas na `branch` de desenvolvimento. Se o `commit` não for feito na `branch`, todas as alterações serão levadas junto durante o `commit` para a `master`, podendo quebrar o código-fonte do ambiente de produção. 💀:coffin:

[//]: # (Inserir seção de MERGES, p. 64, explicar tipos de merges)

[//]: # (Na seção de MERGES, subção de tratativa de conflitos, p. 182)

## Salvando em ***stashes***

Salvar modificações atuais em um "depósito pessoal", e resetar o estado atual atualizando com a `branch master`.

```bash
    # Salvar modificações e limpar o estado atual
    git stash

    # Listar stashes
    git stash list

    # Recuperar stash
    git stash apply [numero-stash]

    # Mostrar as alterações feitas na stash
    git stash show -p [numero-stash]

    # Limpar todas as stashes na branch atual
    git stash clear

    # Remover uma stash específica
    git stash drop [numero-stash]

```

## Checkpoints semânticos com ***tags***

As *tags* são utilizadas para demarcar pontos-chave ou versões (ex. v1.0, v.1.2, etc) no desenvolvimento de alguma `branch`. Assim, podemos avançar/retroceder em etapas dentro uma `branch`.

```bash
    # Criando uma tag
    git tag -a [nome-tag] -m "mensagem"

    # Listar tags
    git tag

    # Verificar uma tag
    git tag show [nome-tag]

    # Trocar e retomar o estado de uma tag
    git checkout [nome-tag]

    # Enviar tags para o repo remoto
    git push origin [nome-tag]

    # Enviar todas as tags para o repo remoto
    git push origin --tags

```

[//]: # (Inserir seção sobre rebase, p. 195)

## Controle de versões

Comandos úteis para lidar com pontos de alteração no projeto.

## Arquivos

```bash
    # Mostrar as diffs (comparações) do que está no arquivoA mas não está no arquivoB
    git diff [arquivoA] [arquivoB]

    # Mostrar os commits que alteraram um arquivo, incluindo renomeações
    git log --follow [arquivo]
```

### Staging area

```bash
    # Diferenças do que foi alterado, mas não está no stage
    git diff

    # Diferenças em alterações do que está no stage, mas ainda não foi comitado
    git diff --staged

    # Limpar arquivos não trackeados do stage, melhorando a visualização
    git clean -f
```

### Branch atual

```bash
    # Mostrar todos os commits no histórico da branch, em ordem cronológica reversa
    git log

    # Mostrar os commits da branchA que não estão na branchB
    git log [branchB] [branchA]

    # Mostrar as diffs (comparações) do que está na branchA mas não está na branchB
    git diff [branchB] [branchA]

    # Verificar uma tag
    git tag show [nome]
```

### Projeto

```bash
    # Lista alterações do projeto, com os commits identificados por autoria
    git shortlog

    # Lista todos seus passos no repositório, incluindo mudanças entre branches
    git reflog

    # Lista todos os commits no histórico do projeto, em ordem cronológica reversa
    git log --all
```

## Boas práticas

- Não criar *commits* levianamente, adotar uma boa semântica, mensagens claras e alterações relevantes para o histórico do projeto.

```bash
    # Utilizando título + descrição
    Desktop@User /c/repo-teste (main)
    $ git commit -a -m "Esta é uma mensagem com descrição
> Deixe as aspas abertas para pular uma linha e inserir maiores detalhes sobre as alterações feitas
> Até que as aspas sejam fechadas, novas linhas podem ser inseridas
> 
> Fim."
```

* Otimizar periodicamente a performance do repositório com ***garbage collector***  removendo arquivos não necessários.

```bash
    git gc
```

* Checar periodicamente a integridade dos arquivos com ***filesystem check***, comando que identifica possíveis corrupções em arquivos.

```bash
    git fsck
```

[//]: # (Incluir técnica de branch privada)

---

## Bibliografia

SKOULIKARI, Anna. **Learning Git: A Hands-On and Visual Guide to the Basics of Git**. Sebastopol: O'Reilly, 2023.
