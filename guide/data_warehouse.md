#

||
|---|
|![Banner](../assets/banner-guide05.png)|
||

## Data Warehouse Relacional

É uma arquitetura específica de bancos relacionais, desenvolvido com o intuito de concentrar bancos de dados de diversas fontes em um único local, para a otimização de queries e análise de dados em larga escala.

Sua orientação de uso é *"write once, read many"*, ou seja, o trabalho de aplicação da estrutura é complexo e demorado, porém é feito somente uma vez, sua utilização é orientada para consumo analítico frequente.

- ideal para dados estruturados
- otimizado para rápida performance de queries complexas
- ideal para análisar dados históricos
- melhoria na qualidade dos dados, por meio de processos de limpeza e integração
- melhoria na tomada de decições ao consolidar múltiplas fontes em um único local.

## Estrutura Relacional

Em bancos de dados relacionais, onde a consistência e a integridade dos dados são de importância primária, os dados são geralmente organizados pela abordagem **schema-on-write** (p. 14). Ou seja, o schema é definido antes e aplicado durante a ingestão dos dados no data warehouse.

- ***schema***: estrutura formal que define a organização de tabelas, campos, tipos de dados e restrições, bem como os relacionamentos entre esses elementos. Serve como uma planta baixa do armazenamento e gerenciamento de dados, e assegura consistência, integridade, e uma organização eficiente dentro do banco de dados. (p. 14)

## Modelagem Dimensional

*Veja mais em **Guia: Data Modeling*** [֍](./data_modeling.md)

Provê a otimização do design para o processamento analítico, fornecendo contexto a medidas granulares por meio de tabelas de dimensão.

## Referências

SERRA, James. **Deciphering Data Architectures: Choosing Betweeen a Modern Warehouse, Data Fabric, Data Lakehouse, and Data Mesh**. Sebastopol: O'Reilly, 2024.
