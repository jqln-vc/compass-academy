#

||
|---|
|![Banner](/assets/banner-sprint1-desafio.png)|
||

## ETAPAS

### PREPARAÇÃO
Download do arquivo `vendas.csv`, criação da pasta `ecommerce` e envio do arquivo para lá. 
Verifica-se na imagem que tive alguns problemas iniciais, relacionados a  

* **permissão de acesso:** *solucionada utilizando o comando `sudo` na linha abaixo*
```bash
sudo mv vendas.csv /workspaces/compass-academy/sprint1/desafio/ecommerce
```
* **uso incorreto do comando `mv` :** em vez de criar a pasta no caminho acima, movi o arquivo `vendas.csv` para a pasta `desafio` e renomeei o arquivo para `ecommerce`. :clown_face:  

   Percebi tinha errado, e que `ecommerce` não era um diretório, tanto com as mensagens de erro quanto com a verificação das permissões do arquivo `-rwxrwxrwx`, mas ainda não tinha entendido o que ocorreu, até fui verificar se vendas.csv (sei que não é uma boa prática habilitar todas as permissões para todos)

