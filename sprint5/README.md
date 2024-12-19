#

||
|---|
|![Banner](/assets/banner-sprint5.png)|
||

## RELATOS DE APRENDIZADO

### Fundamentos de Cloud & AWS S3

[![AWS Fundamentos](https://img.shields.io/badge/Guia-AWS_Fundamentos-ED751A)](/guide/aws_fundamentos.md)  
[![AWS Storage](https://img.shields.io/badge/Guia-AWS_Storage-ED751A)](/guide/aws_storage.md)

### Boto3 API

---

## EXERCÍCIOS

Todos os códigos dos exercícios foram implementados seguindo os Python Enhancement Proposal, especificamente as recomendações de estilo do PEP8 e convenções de docstrings do PEP257, indicados na seção [Bibliografia](#bibliografia), com validação no [*CodeWOF: Python 3 Style Checker*](https://www.codewof.co.nz/style/python3/) online.

Na pasta `evidencias/exercicios`, estão localizadas as imagens com a validação de cada exercício.

* **instancia_ec2.py** : criação de uma instância EC2 com especificações solicitadas:
  * **Tipo de Instância** | t2.micro
  * **Tags** | Instance e Volume
    * `Name` : compass-sprint5
    * `Project` : Programa de Bolsas
    * `CostCenter` : Data & Analytics
* **hospedagem_s3.py** : criação de bucket com configuração para hospedagem de website estático e upload de arquivos da aplicação.
  * Conteúdo do bucket:
    * `index.html`
    * `404.html`
    * `dados/nomes.csv`
  * Link para o website [֍](http://compass-sprint5-lab.s3-website-us-east-1.amazonaws.com/)

## DESAFIO

## EVIDÊNCIAS

Na pasta `evidencias`, encontram-se prints referentes a momentos de execução, exemplificando abordagens adotadas para o desenvolvimento dos exercícios e do desafio.  
No passo a passo explicativo, encontrado na pasta `desafio`, serão comentados outros prints de pontos específicos.

### CRIAÇÃO DE INSTÂNCIA EC2

Criação de instância EC2 para teste, tanto no console quanto a partir de script Python com a API Boto3.

#### EXECUÇÃO NO MANAGEMENT CONSOLE

![Execução EC2 Console](./evidencias/exercicios/1-ec2-instance.gif)

#### EXECUÇÃO COM SCRIPT PYTHON E BOTO3

![Execução EC2 Boto]()

### AWS LAB S3 BUCKET: HOSPEDAGEM DE SITE ESTÁTICO

#### EXECUÇÃO NO MANAGEMENT CONSOLE

![Execução Hospedagem Console](./evidencias/exercicios/2-lab-hospedagem.gif)

#### EXECUÇÃO COM SCRIPT PYTHON E BOTO3

![Execução Hospedagem Boto]()

## CERTIFICADOS AWS SKILL BUILDER

### AWS Curso-Padrão de Preparação para o Exame: CLF-C02 - Português

| |
|---|
|![Certificado](./certificados/cert-curso-prep-clf02.png) |
||

## CERTIFICADOS COMPLEMENTARES

Para absorver melhor o conteúdo desta sprint e me aprofundar em pontos de interesse, concluí em paralelo os cursos abaixo, externos à Udemy.

### AWS Fundamentals of Machine Learning and Artificial Intelligence

| |
|---|
|![Certificado](certificados/cert-comp-fundamentals-ml-ai.png)|
||

## BIBLIOGRAFIA

AMAZON WEB SERVICES. **Simple Storage Service: User Guide**. Última atualização: 2024. Disponível em: <[docs.aws.amazon.com/pdfs/AmazonS3](https://docs.aws.amazon.com/pdfs/AmazonS3/latest/userguide/s3-userguide.pdf)>.

VAN ROSSUM, Guido; WARSAW, Barry; COGHLAN, Alyssa. **PEP 8 – Style Guide for Python Code**. Última atualização: 2013. Disponível em: <[peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)>.  

VAN ROSSUM, Guido; GOODGER, David. **PEP 257 – Docstring Conventions**. Última atualização: 2001. Disponível em: <[peps.python.org/pep-0257/](https://peps.python.org/pep-0257/)>.
