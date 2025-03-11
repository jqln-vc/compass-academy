#

||
|---|
|![Banner](/assets/banner-sprint4.png)|
||

## EXERCÍCIOS

Todos os códigos dos exercícios foram implementados seguindo os Python Enhancement Proposal, especificamente as recomendações de estilo do PEP8 e convenções de docstrings do PEP257, indicados na seção [Bibliografia](#bibliografia), com validação no [*CodeWOF: Python 3 Style Checker*](https://www.codewof.co.nz/style/python3/) online.

Na pasta `evidencias`, estão localizadas as imagens com a validação de cada exercício.

- [Exercício 1](./exercicios/exercicio1.py)
- [Exercício 2](./exercicios/exercicio2.py)
- [Exercício 3](./exercicios/exercicio3.py)
- [Exercício 4](./exercicios/exercicio4.py)
- [Exercício 5](./exercicios/exercicio5.py)
- [Exercício 6](./exercicios/exercicio6.py)
- [Exercício 7](./exercicios/exercicio7.py)

## DESAFIO

- **Carguru: Imagem e Contêiner**
  - [carguru.py](./desafio/carguru/carguru.py): script de randomização de veículos.
  - [Dockerfile](./desafio/carguru/Dockerfile): template para imagem do contêiner Docker.
- **Mascarar Dados: Imagem e Contêiner**
  - [mascarador.py](./desafio/mascarador/mascarador.py): script de criptografia de dados com SHA-1.
  - [Dockerfile](./desafio/mascarador/Dockerfile): template para imagem do contêiner Docker.
- **Reutilização de Contêineres**
  - [Seção: Reutilização de Contêineres](./desafio/README.md#reutilização-de-contêineres): Documentação sobre reutilização de contêineres no contexto de desenvolvimento de software e arquitetura de microsserviços.

## EVIDÊNCIAS

Na pasta `evidencias`, encontram-se prints referentes a momentos de execução do código, exemplificando abordagens adotadas para a conclusão do desafio.  
No passo a passo explicativo, encontrado na pasta `desafio`, serão comentados outros prints de pontos específicos.

### Build de Imagens com Dockerfile

![Imagens Docker](./evidencias/desafio/9-docker-images.png)

### Instanciação e Execução de Contêineres

![Contêineres Docker](./evidencias/desafio/8-docker-containers.png)

### Sequência de Comandos para Reutilização de Contêiner

![Reutilização de Contêiner](./evidencias/desafio/10-reutilizacao.gif)

## BIBLIOGRAFIA

SCHOLL, Boris; SWANSON,  Trent; JAUSOVEC, Peter. **Cloud Native: Using Containers, Functions, and Data to Build Next-Generation Applications**. Sebastopol: O'Reilly, 2019.

KANE, Sean P.; MATTHIAS, Karl. **Docker Up & Running: Shipping Reliable Containers in Production**. Sebastopol: O'Reilly, 2023.

NADAREISHVILI, Irakli et al. **Microservice Architecture: Aligning Principles, Practices and Culture**. Sebastopol: O'Reilly, 2016.

RICE, Liz. **Container Security: Fundamental Technology Concepts That Protect Containerized Applications**. Sebastolpol: O'Reilly, 2020.

VAN ROSSUM, Guido; WARSAW, Barry; COGHLAN, Alyssa. **PEP 8 – Style Guide for Python Code**. Última atualização: 2013. Disponível em: <[peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)>.  

VAN ROSSUM, Guido; GOODGER, David. **PEP 257 – Docstring Conventions**. Última atualização: 2001. Disponível em: <[peps.python.org/pep-0257/](https://peps.python.org/pep-0257/)>.