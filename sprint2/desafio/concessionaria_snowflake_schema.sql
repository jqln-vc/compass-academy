----------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------

-- Sprint 2: Modelagem Dimensional de Banco Relacional em Snowflake Schema - Concessionária
-- Autoria: Jaqueline Costa
-- Data: Nov / 2024
-- concessionaria_snowflake_schema.sql: Modelagem de dados para sistemas OLAP no padrão de schema snowflake;
-- ingestão de dados a partir das tabelas normalizadas com o script 'concessionaria_normalizacao.sql'.

----------------------------------------------------------------------------------------------------------------
-------------------------- CRIAÇÃO DAS TABELAS DE DIMENSÃO E FATO: SNOWFLAKE SCHEMA ----------------------------
----------------------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS locacao_fact;
DROP TABLE IF EXISTS cliente_dim;
DROP TABLE IF EXISTS vendedor_dim;
DROP TABLE IF EXISTS carro_dim;
DROP TABLE IF EXISTS data_dim;
DROP TABLE IF EXISTS cidade_dim;
DROP TABLE IF EXISTS estado_dim;
DROP TABLE IF EXISTS pais_dim;
DROP TABLE IF EXISTS marca_dim;
DROP TABLE IF EXISTS combustivel_dim;

PRAGMA foreign_keys = ON;

----------------------------------------------------------------------------------------------------------------

-------------------------- Criação da Tabela Dimensão (Normalizada): Cliente -----------------------------------

CREATE TABLE cliente_dim (
	cliente_key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	cliente_id INTEGER NOT NULL,
	nome VARCHAR(100) NOT NULL,
	cidade_key INTEGER NOT NULL,
	estado_key INTEGER NOT NULL,
	pais_key INTEGER NOT NULL,
	FOREIGN KEY (cidade_key) REFERENCES cidade_dim(cidade_key),
	FOREIGN KEY (estado_key) REFERENCES estado_dim(estado_key),
	FOREIGN KEY (pais_key) REFERENCES pais_dim(pais_key) 
);

-------------------------- Criação da Tabela Dimensão (Normalizada): Vendedor ----------------------------------

CREATE TABLE vendedor_dim (
	vendedor_key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	vendedor_id INTEGER NOT NULL,
	nome VARCHAR(100) NOT NULL,
	estado_key INTEGER NOT NULL,
	FOREIGN KEY (estado_key) REFERENCES estado_dim(estado_key)
);

-------------------------- Criação da Tabela Dimensão (Normalizada): Cidade ------------------------------------

CREATE TABLE cidade_dim (
	cidade_key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	cidade_id INTEGER NOT NULL,
	nome VARCHAR(40) UNIQUE NOT NULL
);

-------------------------- Criação da Tabela Dimensão (Normalizada): Estado ------------------------------------

CREATE TABLE estado_dim (
	estado_key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	estado_id INTEGER NOT NULL,
	nome VARCHAR(40) UNIQUE NOT NULL
);

-------------------------- Criação da Tabela Dimensão (Normalizada): País --------------------------------------

CREATE TABLE pais_dim (
	pais_key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	pais_id INTEGER NOT NULL,
	nome VARCHAR(40) UNIQUE NOT NULL
);

-------------------------- Criação da Tabela Dimensão (Normalizada): Carro -------------------------------------

CREATE TABLE carro_dim (
	carro_key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	carro_id INTEGER NOT NULL,
	classi VARCHAR(50) UNIQUE NOT NULL,
	modelo VARCHAR(80) NOT NULL,
	marca_key INTEGER NOT NULL,
	ano INTEGER NOT NULL,
	combustivel_key INTEGER NOT NULL,
	FOREIGN KEY (marca_key) REFERENCES marca_dim(marca_key),
	FOREIGN KEY (combustivel_key) REFERENCES combustivel_dim(combustivel_key) 
);

-------------------------- Criação da Tabela Dimensão (Normalizada): Marca -------------------------------------

CREATE TABLE marca_dim (
	marca_key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	marca_id INTEGER NOT NULL,
	nome VARCHAR(80) UNIQUE NOT NULL
);

-------------------------- Criação da Tabela Dimensão (Normalizada): Combustível -------------------------------

CREATE TABLE combustivel_dim (
	combustivel_key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	combustivel_id INTEGER NOT NULL,
	tipo VARCHAR(20) UNIQUE NOT NULL
);

------------------------------------ Criação da Tabela Dimensão: Data ------------------------------------------

CREATE TABLE data_dim (
	data_key INTEGER PRIMARY KEY NOT NULL,
	'data' DATE UNIQUE NOT NULL,
	data_formatada TEXT NOT NULL,
	dia_semana VARCHAR(20) NOT NULL,
	semana_ano INTEGER NOT NULL,
	dia_mes INTEGER NOT NULL,
	dia_ano INTEGER NOT NULL,
	mes_num INTEGER NOT NULL,
	mes_nome VARCHAR(20) NOT NULL,
	ano INTEGER NOT NULL
);

---------------------------------- Criação da Tabela Fato: Locação ----------------------------------------------

CREATE TABLE locacao_fact (
	locacao_key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	locacao_id INTEGER NOT NULL,
	cliente_key INTEGER NOT NULL,
	vendedor_key INTEGER NOT NULL,
	carro_key INTEGER NOT NULL,
	vlr_diaria DECIMAL NOT NULL,
	data_locacao_key INTEGER NOT NULL,
	hora_locacao TIME NOT NULL,
	qtd_diaria INTEGER DEFAULT -1 NOT NULL,
	data_entrega_key INTEGER DEFAULT 29990101 NOT NULL,
	hora_entrega TIME DEFAULT '00:00' NOT NULL,
	valor_total DECIMAL DEFAULT -1 NOT NULL,
	km_carro INTEGER NOT NULL,
	FOREIGN KEY(data_locacao_key) REFERENCES data_dim(data_key),
	FOREIGN KEY(data_entrega_key) REFERENCES data_dim(data_key),
	FOREIGN KEY(cliente_key) REFERENCES cliente_dim(cliente_key),
	FOREIGN KEY(vendedor_key) REFERENCES vendedor_dim(vendedor_key),
	FOREIGN KEY(carro_key) REFERENCES carro_dim(carro_key)
);

----------------------------------------------------------------------------------------------------------------
------------------------- INSERÇÃO DE DADOS NAS TABELAS DIMENSÃO E FATO: SNOWFLAKE SCHEMA ----------------------
----------------------------------------------------------------------------------------------------------------

-------------------------- Ingestão de Valores na Tabela Dimensão (Normalizada): Estado ------------------------

INSERT OR IGNORE INTO estado_dim (
	estado_id,
	nome
)
SELECT DISTINCT estado_id,
				nome
FROM estado
ORDER BY 1 ASC;

-------------------------- Ingestão de Valores na Tabela Dimensão (Normalizada): Cidade ------------------------

INSERT OR IGNORE INTO cidade_dim (
	cidade_id,
	nome
)
SELECT DISTINCT cidade_id,
				nome
FROM cidade
ORDER BY 1 ASC;

-------------------------- Ingestão de Valores na Tabela Dimensão (Normalizada): País --------------------------

INSERT OR IGNORE INTO pais_dim (
	pais_id,
	nome
)
SELECT DISTINCT pais_id,
				nome
FROM pais
ORDER BY 1 ASC;

-------------------------- Ingestão de Valores na Tabela Dimensão (Normalizada): Marca --------------------------

INSERT OR IGNORE INTO marca_dim (
	marca_id,
	nome
)
SELECT DISTINCT marca_id,
				nome
FROM marca
ORDER BY 1 ASC;

----------------------- Ingestão de Valores na Tabela Dimensão (Normalizada): Combustível -----------------------

INSERT OR IGNORE INTO combustivel_dim (
	combustivel_id,
	tipo
)
SELECT DISTINCT combustivel_id,
				tipo
FROM combustivel
ORDER BY 1 ASC;


-------------------------- Ingestão de Valores na Tabela Dimensão (Normalizada): Cliente ------------------------

INSERT OR IGNORE INTO cliente_dim (
	cliente_id,
	nome,
	cidade_key,
	estado_key,
	pais_key
)
SELECT DISTINCT cli.cliente_id,
				cli.nome,
				cidim.cidade_key,
				estdim.estado_key,
				paisdim.pais_key
FROM cliente cli
JOIN cidade_dim cidim
	ON cli.cidade_id = cidim.cidade_id
JOIN estado_dim estdim
	ON cli.estado_id = estdim.estado_id
JOIN pais_dim paisdim
	ON cli.pais_id = paisdim.pais_id
ORDER BY 1 ASC;

-------------------------- Ingestão de Valores na Tabela Dimensão (Normalizada): Vendedor ----------------------

INSERT OR IGNORE INTO vendedor_dim (
	vendedor_id,
	nome,
	estado_key
)
SELECT DISTINCT vend.vendedor_id,
				vend.nome,
				estdim.estado_key
FROM vendedor vend
JOIN estado_dim estdim
	ON vend.estado_id = estdim.estado_id
ORDER BY 1 ASC;

-------------------------- Ingestão de Valores na Tabela Dimensão (Normalizada): Carro -------------------------

INSERT OR IGNORE INTO carro_dim (
	carro_id,
	classi,
	modelo,
	marca_key,
	ano,
	combustivel_key
)
SELECT DISTINCT car.carro_id,
				car.classi,
				car.modelo,
				mardim.marca_key,
				car.ano,
				combdim.combustivel_key
FROM carro car
JOIN marca_dim mardim
	ON car.marca_id = mardim.marca_id
JOIN combustivel_dim combdim
	ON car.combustivel_id = combdim.combustivel_id
ORDER BY 1 ASC;

------------------------------ Ingestão de Valores na Tabela Dimensão: Data ------------------------------------

INSERT OR IGNORE INTO data_dim (
	data_key,
	'data',
	data_formatada,
	dia_semana,
	semana_ano,
	dia_mes,
	dia_ano,
	mes_num,
	mes_nome,
	ano	
)
SELECT DISTINCT CAST(
	SUBSTR(data_locacao, 1, 4) || 
    SUBSTR(data_locacao, 6, 2) ||
    SUBSTR(data_locacao, 9, 2) AS INTEGER
    ) AS data_key,
    data_locacao AS 'data',
    SUBSTR(data_locacao, 9, 2) || '/' ||
    SUBSTR(data_locacao, 6, 2) || '/' ||
    SUBSTR(data_locacao, 1, 4) AS 'data_formatada',
    CASE STRFTIME('%w', data_locacao)
           WHEN '0' THEN 'Domingo'
           WHEN '1' THEN 'Segunda-feira'
           WHEN '2' THEN 'Terça-feira'
           WHEN '3' THEN 'Quarta-feira'
           WHEN '4' THEN 'Quinta-feira'
           WHEN '5' THEN 'Sexta-feira'
           WHEN '6' THEN 'Sábado'
    END AS dia_semana,
    CAST(STRFTIME('%W', data_locacao) AS INTEGER) AS semana_ano,
    CAST(STRFTIME('%d', data_locacao) AS INTEGER) AS dia_mes,
    CAST(STRFTIME('%j', data_locacao) AS INTEGER) AS dia_ano,
    CAST(STRFTIME('%m', data_locacao) AS INTEGER) AS mes_num,
    CASE STRFTIME('%m', data_locacao)
           WHEN '01' THEN 'Janeiro'
           WHEN '02' THEN 'Fevereiro'
           WHEN '03' THEN 'Março'
           WHEN '04' THEN 'Abril'
           WHEN '05' THEN 'Maio'
           WHEN '06' THEN 'Junho'
           WHEN '07' THEN 'Julho'
           WHEN '08' THEN 'Agosto'
           WHEN '09' THEN 'Setembro'
           WHEN '10' THEN 'Outubro'
           WHEN '11' THEN 'Novembro'
           WHEN '12' THEN 'Dezembro'
    END AS mes_nome,
    CAST(STRFTIME('%Y', data_locacao) AS INTEGER) AS ano
FROM locacao
ORDER BY 1 ASC;

INSERT OR IGNORE INTO data_dim (
	data_key,
	'data',
	data_formatada,
	dia_semana,
	semana_ano,
	dia_mes,
	dia_ano,
	mes_num,
	mes_nome,
	ano	
)
SELECT DISTINCT CAST(
	SUBSTR(data_entrega, 1, 4) || 
    SUBSTR(data_entrega, 6, 2) ||
    SUBSTR(data_entrega, 9, 2) AS INTEGER
    ) AS data_key,
    data_entrega AS 'data',
    SUBSTR(data_entrega, 9, 2) || '/' ||
    SUBSTR(data_entrega, 6, 2) || '/' ||
    SUBSTR(data_entrega, 1, 4) AS data_formatada,
    CASE STRFTIME('%w', data_entrega)
           WHEN '0' THEN 'Domingo'
           WHEN '1' THEN 'Segunda-feira'
           WHEN '2' THEN 'Terça-feira'
           WHEN '3' THEN 'Quarta-feira'
           WHEN '4' THEN 'Quinta-feira'
           WHEN '5' THEN 'Sexta-feira'
           WHEN '6' THEN 'Sábado'
    END AS dia_semana,
    CAST(STRFTIME('%W', data_entrega) AS INTEGER) AS semana_ano,
    CAST(STRFTIME('%d', data_entrega) AS INTEGER) AS dia_mes,
    CAST(STRFTIME('%j', data_entrega) AS INTEGER) AS dia_ano,
    CAST(STRFTIME('%m', data_entrega) AS INTEGER) AS mes_num,
    CASE STRFTIME('%m', data_entrega)
           WHEN '01' THEN 'Janeiro'
           WHEN '02' THEN 'Fevereiro'
           WHEN '03' THEN 'Março'
           WHEN '04' THEN 'Abril'
           WHEN '05' THEN 'Maio'
           WHEN '06' THEN 'Junho'
           WHEN '07' THEN 'Julho'
           WHEN '08' THEN 'Agosto'
           WHEN '09' THEN 'Setembro'
           WHEN '10' THEN 'Outubro'
           WHEN '11' THEN 'Novembro'
           WHEN '12' THEN 'Dezembro'
    END AS mes_nome,
    CAST(STRFTIME('%Y', data_entrega) AS INTEGER) AS ano
FROM locacao
ORDER BY 1 ASC;

------------------------------ Ingestão de Valores na Tabela Fato: Locação -------------------------------------

INSERT OR IGNORE INTO locacao_fact (
	locacao_id,
	cliente_key,
	vendedor_key,
	carro_key,
	vlr_diaria,
	data_locacao_key,
	hora_locacao,
	qtd_diaria,
	data_entrega_key,
	hora_entrega,
	valor_total,
	km_carro
)
SELECT DISTINCT loc.locacao_id,
				clidim.cliente_key,
				vendim.vendedor_key,
				cardim.carro_key,
				loc.vlr_diaria,
				dtloc.data_key AS data_locacao_key,
				loc.hora_locacao,
				loc.qtd_diaria,
				dtent.data_key AS data_entrega_key,
				loc.hora_entrega,
				(loc.vlr_diaria * loc.qtd_diaria) AS valor_total,
				loc.km_carro
FROM locacao loc
JOIN cliente_dim clidim
	ON loc.cliente_id = clidim.cliente_id
JOIN vendedor_dim vendim
	ON loc.vendedor_id = vendim.vendedor_id
JOIN carro_dim cardim
	ON loc.carro_id = cardim.carro_id
JOIN data_dim dtloc
	ON loc.data_locacao = dtloc.'data'
JOIN data_dim dtent
	ON loc.data_entrega = dtent.'data'
ORDER BY 1 ASC;

----------------------------------------------------------------------------------------------------------------
-------------------------------------- ANÁLISE DE TABELAS FATO E DIMENSÃO --------------------------------------
----------------------------------------------------------------------------------------------------------------

-- SELECT * FROM locacao_fact;
-- SELECT * FROM cliente_dim;
-- SELECT * FROM vendedor_dim;
-- SELECT * FROM carro_dim;
-- SELECT * FROM data_dim;
-- SELECT * FROM cidade_dim;
-- SELECT * FROM estado_dim;
-- SELECT * FROM pais_dim;
-- SELECT * FROM marca_dim;
-- SELECT * FROM combustivel_dim;