#

| |
|---|
|![Banner](../assets/banner-guide01.png)|
| |

## Estrutura de Diretórios da Raíz

- `/` raíz  
- `bin` arquivos binários, necessários para a execução de ações  
- `boot` arquivos que auxiliam na inicialização do sistema (pode estar vazia)  
- `dev` arquivos que representam os dispositivos de entrada/saída (E/S) do sistema (ex. usb, teclado, etc)  
- `etc` arquivos de configuração de instalações
- `home` arquivos pessoais dos usuários  
- `lib` arquivos de bibliotecas compartilhadas entre aplicativos  
- `media` diretórios dos dispositivos E/S montados (mounted) no PC (pode estar vazia)  
- `opt` arquivos das aplicações de terceiros  
- `sbin` (system binaries) arquivos binários de inicialização do sistema  
- `tmp` arquivos temporários, que podem ser deletados a qualquer momento (ex. instaladores)  
- `usr` arquivos utilizados somente no modo leitura, não podem ser editados (ex. comando man de manual do sistema)  
- `var` arquivos que “variam muito” (ex. arquivos de log)

## Manipulação de Strings

### sed | *stream editor*

Trata texto como um *stream* de dados, processando linha a linha, sem carregar o arquivo todo em memória. Tornando-o altamente eficiente ao trabalhar com arquivos grandes. É não-interativo, pois as edições não são manuais, pelo contrário, comandos são fornecidos para tratar automaticamente todos os dados conforme passam pelo fluxo.

#### Opções na linha de comando

`-n` impede o padrão default de impressão

```bash
    # imprime a 3ª linha
    sed -n '3p' file.txt 
```

`-e` adicionar múltiplos comandos

```bash
    # sed [options] sed-command [input-file]
    sed -e 'command1' -e 'command2' input-file
```

### grep

### awk

---

## Referências

ALBING, Carl; VOSSEN, JP. **Bash Cookbook: Solutions and Examples for Bash Users**. Sebastopol: O’Reilly, 2018.

ALBING, Carl; VOSSEN, JP. **Bash Idioms: Write Powerful, Flexible, Readable Shell Scripts**. Sebastopol: O’Reilly, 2022.

BARRETT, Daniel. **Efficient Linux at the Command Line.** Sebastopol: O’Reilly, 2022.

### CheatSheets

https://gist.github.com/ssstonebraker/6140154

https://au-bio-bootcamp.github.io/cheatsheet_sed.pdf

https://quickref.me/sed.html

