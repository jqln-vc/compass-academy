#

||
|---|
|![Banner](../assets/banner-aws-fundamentos.png)|
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
  - pagamento por utilização/computação: You only pay for the compute time that you consume. There is also no need to over-provision capacity for things like compute and storage.
  - The developer doesn't have to provision or maintain any servers. There is no software or runtime to install, maintain, or administer.
  - Flexible scaling - The application can be scaled automatically or by adjusting its capacity through toggling the units of consumption, such as throughput or memory, rather than units of individual servers.
  - High availability - Serverless applications have built-in availability and fault tolerance. The developer doesn't need to architect for these capabilities because the services running the application provide them by default.
  - Serverless applications do not require you to provision or manage any servers. These applications have built-in service integrations, so you can focus on building your application instead of configuring it. Serverless technologies eliminate infrastructure management tasks like capacity provisioning and patching, so you can focus on writing code that serves your customers. These technologies feature automatic scaling, built-in high availability, and a pay-for-use billing model to increase agility and optimize costs.

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

## CAF: Cloud Adoption Framework

Auxiliar no desenvolvimento e implementação de um plano abrangente para a adoção de serviços e migração para a nuvem, utilizando os serviços AWS de forma otimizada e adaptada às necessidades específicas de cada negócio, por meio de boas práticas e aprendizados adquiridos com experiências de outros clientes.

- Identificar e priorizar oportunidades de transformação
- Avaliar e melhorar o preparo para a nuvem
- Evoluir iterativamente o percurso de adoção
- Acelerar os retornos e valores agregados ao negócio

### Possíveis problemas no percurso de adoção

- Piloto emperrado: o projeto de adoção não traz grandes resultados e valor agregado no início, isso pode causar uma perda do *momentum* na adoção, perdendo credibilidade para escalar para outros projetos.
- Congestionamento na nuvem: iniciativas de adoção ficam paradas em longas filas de prioridade, devido à densidade de processos de governança, falta de automação, blueprints e diretrizes que são necessários para utilizar a nuvem de uma maneira segura, escalável e confiável.
- Benefícios não conquistados: limitação dos benefícios potenciais e alcançados. Por exemplo, se as organizações tratarem a nuvem como só mais um *data center*, sem tirar vantagem de automações e otimizações, podem não conseguir reduzir custos ou melhorar a agilidade de processos de forma significativa.
- Caos na nuvem: se as lideranças não forem coerentes e concisas, priovendo orientação e perspectiva geral, partes diferentes da organização podem adotar a nuvem de formas diferentes. Isso pode resultar em uma proliferação descontrolada de abordagens e ferramentas/serviços, trazendo riscos potenciais à segurança, resiliência, custos e conformidades legais.

### Componentes


- **Desempenho do Negócio | *Business Outcomes***: resultados-chave alcançados com a adoção da nuvem
    - Redução de riscos de negócio
    - Melhoria em ESG (Environmental, Social, and Corporate Governance)
    - Aumento nos lucros
    - Melhoria da eficiência operacional
- **Domínios de Transformação | *Transformation Domains***: aplicações de mudanças organizacionais para uma aceleração nos resultados da adoção, representação uma sequência onde transformação tecnológica possibilita a transformação nos processos, que possibilita a transformação organizacional, que resulta na transformação de produtos.
    - Tecnologia: *como utilizar a nuvem para migrar e modernizar infraestruturas legadas, aplicações e plataformas de análise de dados.*
    - Processos: *digitalização, automação e otimização de operações de negócio. Pode incluir a utilização de novas plataformas de dados e análises, e machine learning; melhorando a eficiência operacional, reduzindo custos e melhorando a experiência dos clientes internos e externos.*
    - Organização: *reimaginação do modelo operacional, como os times de negócio e de tecnologia alinham seus esforços conjuntos para criar valor ao cliente e alcançar os objetivos estratégicos. Ao organizar os times em torno de produtos e fluxo de valores, utilizando métodos ágeis para iterar e evoluir rapidamente, irá auxiliar no redirecionamento para o foco em responsividade e atenção ao cliente.*
    - Produto: *reimaginação do modelo de negócio ao criar novas propostas de valor (produtos e serviços) e lucratividade. Assim, suprindo novas necessidades de clients, e estendendo o negócio para novos segmentos do mercado.*
- **Perspectivas | *Perspectives***: foundational capabilities that functionally related stakeholders own or manage in their cloud transformation journey. They help organizations identify gaps in skills and processes and assess the kind of impact that cloud transformation can have on a functional role and business.
    - Business: assegura que seus investimentos na nuvem acelerem suas metas de transformação digital e resultados de negócio. Stakeholders: Chief executive officer (CEO), chief financial officer (CFO), chief operations officer (COO), chief information officer (CIO), and chief technology officer (CTO).
    - Pessoas: serve como uma ponte entre a tecnologia e o negócio, acelerando a jornada à nuvem, auxiliando a organização a evoluir para uma cultura de crescimento e aprendizados contínuos, onde a mudança se torna parte do negócio. Além da cultura, o foco é a estrutura organizacional, liderança e força de trabalho. Stakeholders: CIO, COO, CTO, cloud director, and cross-functional and enterprise-wide leaders.
    - Governança: auxilia no alinhamento das iniciativas de adoção da nuvem, enquanto que maximiza os benefícios organizacionais e minimiza os riscos decorrentes das mudanças. Stakeholders: Chief transformation officer, CIO, CTO, CFO, chief data officer (CDO), and chief risk officer (CRO).
    - Plataforma: auxilia em acelerar a entrega de produtos e serviços, por meio de plataformas de nuvem em nível organizacional, escaláveis e híbridas. Stakeholders: CTO, technology leaders, architects, and engineers.
    - Segurança: auxilia no alcance de confidencialidade, integridade, e disponibilidade de dados e serviços. Stakeholders: Chief information security officer (CISO), chief compliance officer (CCO), internal audit leaders, and security architects and engineers.
    - Operações:   assegura que seus serviços na nuvem são entregues em um nível a altura das necessidades dos stakeholders. Ao automatizar e otimizar operações, é possível escalar ao mesmo tempo que melhora a confiabilidade de suas entregas. Stakeholders: Infrastructure and operations leaders, site reliability engineers, and information technology service managers.
- **Capacidades Fundamentais | *Foundational Capabilities***
- **Fases de Transformação na Nuvem | *Cloud Transformation Phases***


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
