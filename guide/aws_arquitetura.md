#

||
|---|
|![Banner](../assets/banner-guide03.png)|
||

## Conceitos de Cloud e AWS

**Computação em Nuvem** é a entrega sob demanda de recursos de TI através da Internet, com custos de acordo com sua utilização, ou seja, sem custos prévios de aquisição.

- Flexibilidade
- Elasticidade
- Agilidade
- Otimização de Custos
- Otimização de Performance

How does the scale of cloud computing help you to save costs?
The aggregated cloud usage from a large number of customers results in lower pay-as-you-go prices.





### Níveis de Abstração
https://aws.amazon.com/blogs/architecture/compute-abstractions-on-aws-a-visual-story/

- Máquinas Físicas
  - investimento pesado
  - vive por anos in loco

- Máquinas Virtuais
  - recursos elásticos
  - provisionamento rápido

- Contêineres
  - independente de plataformas
  - deploys mais rápidos e objetivos

- Serverless (*sem servidor*)
  - event-driven
  - pagamento por utilização

### Modos de Deploy (*implantação*)

- Cloud
Run all parts of the application in the cloud.
Migrate existing applications to the cloud.
Design and build new applications in the cloud.
- On Premises
On-premises deployment is also known as a private cloud deployment. In this model, resources are deployed on premises by using virtualization and resource management tools.
- Híbrido
Connect cloud-based resources to on-premises infrastructure.
Integrate cloud-based resources with legacy IT applications.
In a hybrid deployment, cloud-based resources are connected to on-premises infrastructure. You might want to use this approach in a number of situations. For example, you have legacy applications that are better maintained on premises, or government regulations require your business to keep certain records on premises.


### Soluções em Cloud

- SaaS: Software como Serviço
- PaaS: Plataforma como Serviço
- IaaS: Infraestrutura como Serviço
- CaaS: Computação como Serviço
  - EC2

## Infraestrutura Global
https://aws.amazon.com/about-aws/global-infrastructure/
- Alta disponibilidade
- Redundância
- Durabilidade

### Regiões

### Zonas de Disponibilidade (*AZ - Availability Zones*)

### Pontos de Presença (*PoP - Points of Presence*)

## Categorias de Serviços
https://aws.amazon.com/products/storage/
https://aws.amazon.com/types-of-cloud-computing/
https://aws.amazon.com/free/database/
https://aws.amazon.com/security/
https://aws.amazon.com/products/management-and-governance/
https://aws.amazon.com/products/networking/


- Computação
- Armazenamento
  - object
  - file
  - block
- Banco de Dados
- Segurança
  - Amazon Macie: uses ML to help customers prevent data loss by automatically discovering, classifying, and protecting sensitive data stored with AWS. This fully managed service continuously monitors data access activity for anomalies. It generates detailed alerts when it detects a risk of unauthorized access or inadvertent data leaks, such as sensitive data that a customer has accidentally made externally available.
- Governança
  - AWS Cost Explorer
  - AWS Security Hub
  - Amazon CloudWatch
  - AWS Config
  - AWS Organizations
  - AWS CloudTrail: log, continuously monitor, and retain account activity across their AWS infrastructure. This simplifies security analysis, resource change tracking, and troubleshooting. 
- Redes

## Aplicações Monoliticas X Microsserviços
https://aws.amazon.com/microservices/

Microservices are minimal-function services that are deployed separately but can interact together to achieve a broader use case. These applications then become more straightforward to build and maintain because they are smaller and more manageable. 

### Desvantagens de Estruturas Monolíticas

- difíceis de escalar
- não lidam bem com falhas em componentes
- possuem um processo de implantação lento
- possuem opções limitadas

## AWS Cloud Value Framework
https://docs.aws.amazon.com/pdfs/whitepapers/latest/overview-aws-cloud-adoption-framework/overview-aws-cloud-adoption-framework.pdf

Estrutura conceitual utilizada para compreender os processos e o desenvolvimento de empresas com a adoção de serviços de Cloud. Utiliza os 4 pilares de valor:

- Redução de Custos
  - benefício de impacto mais rápido
  - eliminação de custos de manutenção e reparo de recursos
  - redução de custos de implantação
  - tende a diminuir progressivamente conforme o tempo de adoção se estende
- Produtividade dos Colaboradores
  - redução ou eliminação de administração de recursos de hardware e software
  - aumento nas atividades de maior valor agregado para a empresa
- Resiliência Operacional
  - melhoria nos SLAs
  - diminuição de impactos resultantes de falhas de sistema
  - melhoria em segurança
  - aumento na disponibilidade de serviços
  - redução na latência
- Agilidade nos Negócios
  - redução no tempo e erros de deploy
  - aumento da criatividade (*"fail fast and cheaply, learn and improve faster"*)
  - diminuição no tempo de resposta às mudanças no mercado

## Modelo de Responsabilidade Compartilhada
https://aws.amazon.com/compliance/shared-responsibility-model/
- Segurança DA Nuvem
- Segurança NA Nuvem

## Referências

REFERRE, Massimo. Compute Abstractions on AWS: A Visual Story. [link](https://aws.amazon.com/blogs/architecture/compute-abstractions-on-aws-a-visual-story/)

https://d0.awsstatic.com/whitepapers/aws-overview.pdf
