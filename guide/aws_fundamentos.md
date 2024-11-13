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
  - A larga escala da computação em nuvem, resultando em o uso agregado de uma imensa quantidade de clientes, resulta em diminuição de preços.
- Otimização de Performance

### Níveis de Abstração
https://aws.amazon.com/blogs/architecture/compute-abstractions-on-aws-a-visual-story/

- **Máquinas Físicas**
  - investimento pesado
  - vive por anos *in loco*

- **Máquinas Virtuais**
  - recursos elásticos
  - provisionamento rápido

- **Contêineres**
  - independente de plataformas
  - deploys mais rápidos e objetivos

- **Serverless (*"Sem Servidor"*)**
  - event-driven
  - pagamento por utilização

### Modos de Deploy (*Implantação*)

- **Cloud**
  - Execução de todas as partes da aplicação em nuvem.
  - Migração de aplicações existentes para a nuvem.
  - Design e desenvolvimento de novas aplicações em nuvem.

- **On Premises**
  - Também denominado **implantação de nuvem privada**.
  - Recursos implantados no local, através de virtualização e ferramentas de gerenciamento de recursos.

- **Híbrido**
  - Conexão de recursos de nuvem à infraestrutura *on-premise*.
  - Integração de recursos de nuvem a aplicações de TI legadas (*legacy*).
  - Recomendado em casos que a manutenção *on-premises* de aplicações legadas, ou a existência de regulamentos governamentais que requerem que certos registros/dados sejam mantidos *on-premises*.

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

Fatores na escolha entre Regiões:

- **Compliance**: requirimentos legais ou questões relacionadas à governança dos dados, os dados não saem de uma Região sem autorização.
- **Latência**: proximidade dos usuários finais.
- **Disponibilidade de Recursos**: nem todos os recursos estão disponíveis em todas as Regiões.
- **Preço**: devido às taxas locais, os preços variam de Região para Região.

### Zonas de Disponibilidade (*AZ - Availability Zones*)

- Composta de 1 ou mais data centers dentro de uma Região.
- São localizadas há dezenas de milhas de distância uma das outras. Contribuindo com a interconectividade para prover recursos aos serviçoes e aplicações dentro de uma Região.
  - Medida de distância ideal para garantir latência otimizada e, ao mesmo tempo, garantir a disponibilidade em casos de catástrofes físicas/naturais.

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

Microsserviços são serviços com funções mínimas, implementados separada e independentemente, mas que podem interagir em conjunto para alcançar uma funcionalidade maior. Essas aplicações são mais simples de desenvolver e manter pois são menores e mais gerenciáveis.

### Desvantagens das Estruturas Monolíticas

- difíceis de escalar
- não lidam bem com falhas em componentes
- possuem um processo de implantação lento
- possuem opções limitadas

## AWS Cloud Value Framework
https://docs.aws.amazon.com/pdfs/whitepapers/latest/overview-aws-cloud-adoption-framework/overview-aws-cloud-adoption-framework.pdf

Estrutura conceitual utilizada para compreender os processos e o desenvolvimento de empresas com a adoção de serviços de Cloud. Utiliza os pilares de valor:

- **Redução de Custos**
  - benefício de impacto mais rápido
  - eliminação de custos de manutenção e reparo de recursos
  - redução de custos de implantação
  - tende a diminuir progressivamente conforme o tempo de adoção se estende
- **Produtividade dos Colaboradores**
  - redução ou eliminação de administração de recursos de hardware e software
  - aumento nas atividades de maior valor agregado para a empresa
- **Resiliência Operacional**
  - melhoria nos SLAs
  - diminuição de impactos resultantes de falhas de sistema
  - melhoria em segurança
  - aumento na disponibilidade de serviços
  - redução na latência
- **Agilidade nos Negócios**
  - redução no tempo e erros de deploy
  - aumento da criatividade (*"fail fast and cheaply, learn and improve faster"*)
  - diminuição no tempo de resposta às mudanças no mercado
- **Sustentabilidade**
  - Minimização do impacto ambiental das operações

## Modelo de Responsabilidade Compartilhada
https://aws.amazon.com/compliance/shared-responsibility-model/
- Segurança DA Nuvem
- Segurança NA Nuvem

## Estratégias de Migração

- **Refactoring**: alteração de como uma aplicação é planejada e desenvolvida, tipicamente utilizando recursos nativos de cloud.
- **Repurchasing**: substituição de uma aplicação existente por outra baseada em nuvem, tal como os softwares encontrados no AWS Marketplace.
- **Rehosting**: deslocamento de uma aplicação para a nuvem com pouca ou nenhuma modificação na aplicação. Também conhecida como *lift and shift*.
- **Replatforming**: otimização seletiva de aspectos de uma aplicação para alcançar benefícios na nuvem, sem modificar o cerne da arquitetura da aplicação. Também conhecida como *lift, tinker and shift*.

---

## Referências

REFERRE, Massimo. Compute Abstractions on AWS: A Visual Story. [link](https://aws.amazon.com/blogs/architecture/compute-abstractions-on-aws-a-visual-story/)

https://d0.awsstatic.com/whitepapers/aws-overview.pdf
