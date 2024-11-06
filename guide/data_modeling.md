#

||
|---|
|![Banner](../assets/banner-guide06.png)|
||

## Caracterizando o *Data Model*

- principais tópicos ou temas ou entidades
- atributos (dos tópicos ou temas ou entidades)
- relações entre tópicos
- regras de negócio para os dados

## Tipos de Chave

- **chave-primária**: identificador único para cada linha da tabela, pode ser representada por 1 ou mais colunas
  - **chave-natural**: são valores gerados juntamente com o restante dos dados pelo sistema-fonte
    - podem ser compreensíveis ou não (valores codificados)
    - ideal serem substituídas por chaves-naturais para uso de chave-primária
    - mantidas (somente) nas tabelas dimensão como contexto agregado
  - **chave-surrogate (*substituta, suplente, delegada*)**: sem valor de negócio, gerada pelo sistema de banco de dados ou sistema gerenciador de chaves
    - string de dígitos aleatórios
    - para integração de sistemas-fonte, é ideal optar por seu uso, ao invés de chaves naturais
- **chave-estrangeira**: "chave-primária de outra tabela"
  - utilizada para indicar relacionamentos lógicos
  - auxilia na otimização de performance

## OLTP x OLAP

- OLTP | *Online Transaction Processing*


- OLAP | *Online Analytical Processing*

## Normalização

The principle of normalization is the application of logical rigor to the assemblage of itemsof data—which may then become structured information. (p. 4)

Data inconsistency, the difficulty of coding data-entry controls, anderror management in what become bloated application programs are real risks, as well aspoor performance and the inability to make the model evolve. These risks have a very highprobability of occurring if we don’t adhere to normal form, and I will soon show why. (p. 5)

### 1NF: Atomicidade e Identificação

- 1º passo: destrinchando valores e mantendo a atomicidade
  
  First of all, we must ensure that the characteristics, or attributes, we are dealing with areatomic. (p. 5)

    Deciding whether data can be considered atomic or not is chieflya question of scale. For example, a regiment may be an atomic fighting unit to a general-in-chief, but it will be very far from atomic to the colonel in command of that regiment,who deals at the more granular level of battalions or squadrons. In the same way, a carmay be an atomic item of information to a car dealer, but to a garage mechanic, it is veryfar from atomic and consists of a whole host of further components that form themechanic’s perception of atomic data items. (p. 5)

    From a purely practical point of view, we shall define anatomic attribute as an attributethat, in awhere clause, can always be referred to in full. You can split and chop anattribute as much as you want in the select list (where it is returned); but if you need torefer to parts of the attribute inside thewhere clause, the attribute lacks the level ofatomicity you need. (p. 6)

  - otimização de buscas: regular indexes require atomic (in the sense just defined)values as keys. (p. 6)

- 2º passo: caracterizando chaves primárias

Once all atomic data items have been identified, and their mutual interrelationshipsresolved, distinct relations emerge. The next step is to identify what uniquely characterizesa row—the primary key. At this stage, it is very likely that this key will be a compound one,consisting of two or more individual attributes. (p. 7)

As a general rule, you should, whenever possible, use a unique identifier that hasmeaning rather than some obscure sequential integer. I must stress that the primary keyis what characterizes the data—which is not the case with some sequential identifierassociated with each new row. (p. 8)

Once all the attributesare atomic and keys are identified, our data is infirst normal form (1NF). (p.8)

### 2NF: Resolvendo Dependências

To remove dependencies on a part of the key, we must create tables (such ascar_model).The keys of those new tables will each be a part of the key for our original table (in ourexample, make, model, version, and style). Then we must move all the attributes thatdepend on those new keys to the new tables, and retain only make, model, version, andstyle in the original table. We may have to repeat this process, since the engine and itscharacteristics will not depend on the style. Once we have completed the removal ofattributes that depend on only a part of the key, our tables are insecond normal form (2NF). (p. 9)

- redundância de dados
There are two issues with the storage ofredundant data. First, redundant data increases the odds of encountering contra-dictory information because of input errors (and it makes correction more time-consuming). Second, redundant data is an obvious storage waste. It is custom-ary to hear that nowadays storage is so cheap that one no longer needs to beobsessed with space. True enough, except that such an argument overlooks thefact that there is also more and more data to store in today’s world. (p. 8)

Besidesthe mere cost of storage, sometimes—more importantly—there is also the issueof recovery. There are cases when one experiences “unplanned downtime,” avery severe crash for which the only solution is to restore the database from abackup. All other things being equal, a database that is twice as big as necessarywill take twice the time to restore than would otherwise be needed. There areenvironments in which a long time to restore can cost a lot of money. In a hos-pital, it can even cost lives. (p. 9)

- performance de queries
A table that contains a lot of information (with a large number of columns)takes much longer to scan than a table with a reduced set of columns. (p.9)

### 3NF: Checando a Independência de Atributos

We now know that each attribute inthe current set is fully dependent on the unique key. 3NF is reached when we cannotinfer the value of an attribute from any attribute other than those in the unique key. Forexample, the question must be asked: “Given the value of attribute A, can the value ofattribute B be determined?” (p. 9)

- normalização minimiza duplicação de dados
As I have already pointed out, duplicate data is costly, both in terms of disk spaceand processing power, but it also introduces a much-increased possibility of databecoming corrupt. Corruption happens when one instance of a data value ismodified, but the same data held in another part of the database fails to be simul-taneously (and identically) modified. Losing information doesn’t only mean dataerasure: if one part of the database says “white” while another part says “black,”you have lost information. (p. 10)

## Modelagem Dimensional

- Relatórios básicos
- OLAP

There has beensomething of a religious war between the followers of Inmon, who advocates a clean 3NFdesign of enormous data repositories used by decision-support systems, and thesupporters of Kimball, who believes that data warehouses are a different world withdifferent needs, and that therefore the 3NF model, in spite of its qualities in theoperational world, is better replaced withdimensional modeling, in which reference data ishappily denormalized. (p. 265)

Understand that it isnot because one is using the SQLlanguage against “tables” that one is operating in the relational world. (p. 265)

The principle of dimensional modeling is to store measurement values, whether they arequantities, amounts, or whatever you can imagine into bigfact tables. Reference data isstored intodimension tables that mostly contain self-explanatory labels and that areheavily denormalized. There are typically 5 to 15 dimensions, each with a system-generated primary key, and the fact table contains all the foreign keys. Typically, the dateassociated with a series of measures (a row) in the fact table will not be stored as a datecolumn in the fact table, but as a system-generated number that will reference a row inthedate_dimension table in which the date will bedeclinedunder all possible forms. (p. 265)

**Dados Dimensionais:**

- **Fato**
  - numérico e mensurável
  - medidas e métricas
  - não é um fato lógico (booleano)
- **Tabela Fato: *nome_tabela_fact***
  - chave-primária: combinação de todas as chaves-estrangeiras (surrogates) relacionadas às tabelas dimensão (ainda que a tabela fato tenha uma chave natural)
- **Dimensão**
  - tipos variáveis, características quantitativas e qualitativas
  - confere contexto aos fatos
  - pode acomodar redundâncias (ex. a mesma data escrita de formas diferentes)
- **Tabela Dimensão: *nome_tabela_dim***
  - chave-primária (surrogate): nome_tabela_key

### Aditividade (*Additivity*) de Fatos

A capacidade de um fato de ser **somado** e resultar em uma informação com valor agregado.

- **Aditivo**: pode ser somado em todas as situações
  - salários
  - notas
  - durações
- **Não-aditivo**: sua soma não resulta em nenhum valor significativo (porém, outras funções de agregação são úteis, ex. média)
  - médias
  - percentagens
  - razões
- **Semi-aditivo**

### Tipos de Tabela Fato

- **Transacionais**: registros de transações
  - alta granularidade de detalhes
  - geralmente, é o cerne dos modelos dimensionais
  - permite agrupar mais de um fato, caso esteja dentro de 2 regras:
    - o nível de granularidade é o mesmo para os diferentes fatos (ex. quantidade de colunas deve ser igual)
    - os fatos ocorrem simultaneamente
- **Snapshot Períodico**: acompanhamento de uma medida específica em intervalos regulares
- **Snapshot Acumulativo**: acompanhamento do progresso de um processo de negócio através de estágios formalmente definidos
- **Factless**
  - registros de transação sem valores mensuráveis
  - registros de relacionamentos de cobertura e/ou elegibilidade (mesmo que nada tenha ocorrido no relacionamento)

### Star Schema

- todas as dimensões de uma hierarquia representadas em **uma tabela dimensional**
- um único nível de distância da **tabela fato**
- menor quantidade de joins necessários
- relações simples entre chave-primária->chave-estrangeira
- maior armazenamento necessário para dados dimensionais (maior duplicação)
- tabela dimensão "não-normalizada" (maior duplicação)

### Snowflake Schema

- cada dimensão de uma hierarquia representadas em **uma tabela dimensional**
- um ou mais níveis de distância da **tabela fato** ao longo de cada hierarquia
- menor quantidade de joins necessários
- relações complexas entre chave-primária->chave-estrangeira
- menor armazenamento necessário para dados dimensionais (menor duplicação)
- tabela dimensão "normalizada" (menor duplicação)

## Referências

FAROULT, Stephane; ROBSON, Peter. **The Art of SQL**. Sebastopol: O'Reilly, 2006.
SERRA, James. **Deciphering Data Architectures: Choosing Betweeen a Modern Warehouse, Data Fabric, Data Lakehouse, and Data Mesh**. Sebastopol: O'Reilly, 20024.
