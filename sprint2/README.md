#

||
|---|
|![Banner](/assets/banner-sprint2.png)|
||

## RELATOS DE APRENDIZADO

### SQL & Dados Relacionais

[![Data Warehouse](https://img.shields.io/badge/Guia-Data_Warehouse-ED751A)](/guide/data_warehouse.md)  
[![Data Modeling](https://img.shields.io/badge/Guia-Data_Modeling-ED751A)](/guide/data_modeling.md)

Tinha familiaridade anterior com SQL e experiência em utilizar DQL para tarefas mais simples. No entanto, apesar de estar estudando arquitetura e modelagem de dados, ainda não havia tido a experiência de pensar e implementar algo na prática.

Foi uma experiência enriquecedora, sinto que consegui compreender e entrelaçar diversos conceitos que ainda estavam vagos no meu entendimento, como Data Warehouse e Modelagem de Dados, tanto em sistemas OLTP quanto OLAP. Também pude trabalhar com DDL, algo que ainda não havia feito.

Porém ainda sinto que preciso praticar mais o processo de normalização, sinto dificuldade em distinguir entre as 3 formas normais, e só consegui localizar uma oportunidade de melhoria no último dia, após ter me familiarizado melhor com o banco.

---

### AWS Partner: Sales Accreditation

[![AWS Arquitetura](https://img.shields.io/badge/Guia-Arquitetura_AWS-ED751A)](/guide/aws_arquitetura.md)

Tenho estudado e me preparado para o exame CLF-C02 da AWS há alguns meses, então já tinha familiaridade com a maioria dos conceitos abordados.

No entanto, ainda não conhecia o programa de partnership e relações comerciais da AWS, e sinto que o curso trouxe esse conhecimento valioso para minha preparação para o exame.

> ❗ *Optei por realizar os cursos da AWS no Skill Builder em inglês, pois me sinto mais segura em consumir os conteúdos na língua original. E, se possível, também pretendo realizar o exame do certificado CLF-C02 em inglês.*

## EXERCÍCIOS

- **Banco de Dados: Biblioteca**

  - [Exercício 1](./exercicios/exercicio1.sql)
  - [Exercício 2](./exercicios/exercicio2.sql)
  - [Exercício 3](./exercicios/exercicio3.sql)
  - [Exercício 4](./exercicios/exercicio4.sql)
  - [Exercício 5](./exercicios/exercicio5.sql)
  - [Exercício 6](./exercicios/exercicio6.sql)
  - [Exercício 7](./exercicios/exercicio7.sql)
  
- **Banco de Dados: Loja**
  - [Exercício 8](./exercicios/exercicio8.sql)
  - [Exercício 9](./exercicios/exercicio9.sql)
  - [Exercício 10](./exercicios/exercicio10.sql)
  - [Exercício 11](./exercicios/exercicio11.sql)
  - [Exercício 12](./exercicios/exercicio12.sql)
  - [Exercício 13](./exercicios/exercicio13.sql)
  - [Exercício 14](./exercicios/exercicio14.sql)
  - [Exercício 15](./exercicios/exercicio15.sql)
  - [Exercício 16](./exercicios/exercicio16.sql)

- **Exportação de Dados**
  - [Exportação 1](./exercicios/exportacao1.sql) | [Planilha CSV](./exercicios/exportacao1.csv)
  - [Exportação 2](./exercicios/exportacao2.sql) | [Planilha CSV](./exercicios/exportacao2.csv)

## DESAFIO

- [Normalização](./desafio/concessionaria_normalizacao.sql): normalização de tabelas até a 3ª forma normal, otimizada para sistemas OLTP, de acordo com as diretrizes e motivações de Codd. Este processo também foi contextualizado no projeto de data warehouse, aplicado na camada CIF (*Corporate Information Factory*) que serve de repositório consolidado de informações do negócio, bem como fonte de retroalimentação dos sistemas-fonte por meio de ETL Reverso.

- [Modelagem Dimensional - Star Schema](./desafio/concessionaria_star_schema.sql): modelagem dimensional em star schema, otimizando o banco de dados para sistemas OLAP e implementando tabela-fato de tipo snapshot acumulativo, contextualizando o processo a partir de um design de data warehouse híbrido, inspirados nas metodologias de Kimball e Inmon.

- **Bônus:** [Modelagem Dimensional - Snowflake Schema](./desafio/concessionaria_snowflake_schema.sql): exemplificação alternativa de modelagem dimensional em snowflake schema, com a normalização de hierarquias dimensionais.
  
- **Bônus:** [Modelagem Dimensional - Cubos](./desafio/concessionaria_cubos.sql): implementação de cubos por meio de views para exemplificar a aplicação do projeto, bem como alguns outros tipos de análise bidimensionais ("planos"), contextualizando o processo na etapa de distribuição da arquitetura de data warehouse planejada, com motivações inspiradas nas metodologias de Kimball e Inmon.

## EVIDÊNCIAS

Na pasta `evidencias`, encontram-se prints referentes a momentos de execução do código, exemplificando abordagens adotadas para a conclusão do desafio.  
No passo a passo explicativo, encontrado na pasta `desafio`, serão comentados outros prints de pontos específicos.

### NORMALIZAÇÃO

![Normalização](./evidencias/4-concessionaria_normalizado.png)

### MODELAGEM STAR SCHEMA

![Star Schema](./evidencias/5-star-schema.png)

### MODELAGEM SNOWFLAKE SCHEMA

![Star Schema](./evidencias/12-snowflake-schema.png)

## CERTIFICADOS AWS SKILL BUILDER

### AWS Partner: Sales Accreditation (Business)

| |
|---|
|![Certificado-Comp-](certificados/certificado-aws-parter-sales-business.jpg)|
||

## CERTIFICADOS COMPLEMENTARES

Para absorver melhor o conteúdo desta sprint e me aprofundar em pontos de interesse, concluí em paralelo os cursos abaixo, externos à Udemy.

### AWS Cloud Practitioner Essentials

| |
|---|
|![Certificado-Comp-](certificados/certificado-comp-cloud-practitioner-essentials.jpg)|
||

### AWS Security Fundamentals - Second Edition

| |
|---|
|![Certificado-Comp-](certificados/certificado-comp-security-fundamentals.jpg)|
||

### AWS Compute Services Overview

| |
|---|
|![Certificado-Comp-](certificados/certificado-comp-compute-services.jpg)|
||

### AWS Getting Started With CloudFormation

| |
|---|
|![Certificado-Comp-](certificados/certificado-comp-cloudformation.jpg)|
||

## BIBLIOGRAFIA

- CODD, F. Edgar. **Further Normalization of the Database Relational Model**. San Jose: IBM Research Laboratory, 1971. Disponível em: <[forum.thethirdmanifesto.com](https://forum.thethirdmanifesto.com/wp-content/uploads/asgarosforum/987737/00-efc-further-normalization.pdf)>.  
- FAROULT, Stephane; ROBSON, Peter. **The Art of SQL**. Sebastopol: O'Reilly, 2006.  
- KIMBALL, Ralph; ROSS, Margy. **The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling**, 3 ed. Indianapolis: Wiley, 2013.  
- SERRA, James. **Deciphering Data Architectures: Choosing Betweeen a Modern Warehouse, Data Fabric, Data Lakehouse, and Data Mesh**. Sebastopol: O'Reilly, 2024.
