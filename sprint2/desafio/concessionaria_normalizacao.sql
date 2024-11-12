----------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------

-- Sprint 2: Normalização de Banco Relacional - Concessionária
-- Autoria: Jaqueline Costa
-- Data: Nov / 2024
-- concessionaria_normalizacao.sql: Normalização de tabelas nas formas 1NF, 2NF e 3NF para sistemas OLTP;
-- ingestão de dados a partir da tabela original 'tb_locacao'.

----------------------------------------------------------------------------------------------------------------
---------------------------------- CRIAÇÃO DE TABELAS E RELAÇÕES NORMALIZADAS ----------------------------------
----------------------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS locacao;
DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS vendedor;
DROP TABLE IF EXISTS carro;
DROP TABLE IF EXISTS marca;
DROP TABLE IF EXISTS combustivel;
DROP TABLE IF EXISTS cidade;
DROP TABLE IF EXISTS estado;
DROP TABLE IF EXISTS pais;

PRAGMA foreign_keys = ON;

-- SELECT * FROM tb_locacao;
-- SELECT idCarro, vlrDiaria FROM tb_locacao tl ;
-- SELECT idCarro, idLocacao, kmCarro FROM tb_locacao ORDER BY idCarro ASC, kmCarro DESC;

----------------------------------------------------------------------------------------------------------------

--------------------------------- Criação da Tabela Normalizada: Locação ---------------------------------------

CREATE TABLE locacao (
	locacao_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	cliente_id INTEGER NOT NULL,
	carro_id INTEGER NOT NULL,
	vendedor_id INTEGER NOT NULL,
	data_locacao DATE NOT NULL,
	hora_locacao TIME NOT NULL,
	qtd_diaria INTEGER NOT NULL,
	vlr_diaria DECIMAL NOT NULL,
	data_entrega DATE DEFAULT '2999-01-01' NOT NULL,
	hora_entrega TIME DEFAULT '00:00' NOT NULL,
	km_carro INT NOT NULL,
	FOREIGN KEY(cliente_id) REFERENCES cliente(cliente_id),
	FOREIGN KEY(carro_id) REFERENCES carro(carro_id),
	FOREIGN KEY(vendedor_id) REFERENCES vendedor(vendedor_id)
);

--------------------------------- Criação da Tabela Normalizada: Cliente --------------------------------------

CREATE TABLE cliente (
	cliente_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(100) NOT NULL,
	cidade_id INTEGER NOT NULL,
	estado_id INTEGER NOT NULL,
	pais_id INTEGER NOT NULL,
	FOREIGN KEY (cidade_id) REFERENCES cidade(cidade_id),
	FOREIGN KEY (estado_id) REFERENCES estado(estado_id),
	FOREIGN KEY (pais_id) REFERENCES pais(pais_id)
);

--------------------------------- Criação da Tabela Normalizada: Vendedor --------------------------------------

CREATE TABLE vendedor (
	vendedor_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(100) NOT NULL,
	sexo SMALLINT NOT NULL,
	estado_id INTEGER NOT NULL,
	FOREIGN KEY (estado_id) REFERENCES estado(estado_id)
);

--------------------------------- Criação da Tabela Normalizada: Carro -----------------------------------------

CREATE TABLE carro (
	carro_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	classi VARCHAR(50) UNIQUE NOT NULL,
	modelo VARCHAR(80) NOT NULL,
	marca_id INTEGER NOT NULL,
	ano INTEGER NOT NULL,
	combustivel_id INTEGER NOT NULL,
	FOREIGN KEY (marca_id) REFERENCES marca(marca_id),
	FOREIGN KEY (combustivel_id) REFERENCES combustivel(combustivel_id)
);


--------------------------------- Criação da Tabela Normalizada: Marca -----------------------------------------

CREATE TABLE marca (
	marca_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(80) UNIQUE NOT NULL
);

--------------------------------- Criação da Tabela Normalizada: Combustível -----------------------------------

CREATE TABLE combustivel (
	combustivel_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tipo VARCHAR(20) UNIQUE NOT NULL
);

--------------------------------- Criação da Tabela Normalizada: Cidade ----------------------------------------

CREATE TABLE cidade (
	cidade_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(40) UNIQUE NOT NULL
);

--------------------------------- Criação da Tabela Normalizada: Estado ----------------------------------------

CREATE TABLE estado (
	estado_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(40) UNIQUE NOT NULL
);

--------------------------------- Criação da Tabela Normalizada: País ------------------------------------------

CREATE TABLE pais (
	pais_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(40) UNIQUE DEFAULT 'Brasil' NOT NULL
);

---------------------------------------------------------------------------------------------------------------
---------------------------------- INSERÇÃO DE DADOS NAS TABELAS NORMALIZADAS ---------------------------------
---------------------------------------------------------------------------------------------------------------

--------------------------------- Ingestão de Valores na Tabela: Estado ---------------------------------------

INSERT OR IGNORE INTO estado (nome)
SELECT DISTINCT estadoCliente
FROM tb_locacao
ORDER BY estadoCliente ASC;

INSERT OR IGNORE INTO estado (nome)
SELECT DISTINCT estadoVendedor
FROM tb_locacao
ORDER BY estadoVendedor ASC;

--------------------------------- Ingestão de Valores na Tabela: Cidade ----------------------------------------

INSERT OR IGNORE INTO cidade (nome)
SELECT DISTINCT cidadeCliente
FROM tb_locacao
ORDER BY cidadeCliente ASC;

--------------------------------- Ingestão de Valores na Tabela: País ------------------------------------------

INSERT OR IGNORE INTO pais (nome)
SELECT DISTINCT paisCliente
FROM tb_locacao
ORDER BY paisCliente ASC;

--------------------------------- Ingestão de Valores na Tabela: Marca -----------------------------------------

INSERT OR IGNORE INTO marca (nome)
SELECT DISTINCT marcaCarro
FROM tb_locacao
ORDER BY marcaCarro ASC;

--------------------------------- Ingestão de Valores na Tabela: Combustível -----------------------------------

INSERT OR IGNORE INTO combustivel (tipo)
SELECT DISTINCT tipoCombustivel
FROM tb_locacao
ORDER BY tipoCombustivel ASC;

--------------------------------- Ingestão de Valores na Tabela: Carro -----------------------------------------

INSERT OR IGNORE INTO carro (carro_id, classi, modelo, marca_id, ano, combustivel_id)
SELECT DISTINCT tl.idCarro, tl.classiCarro, tl.modeloCarro, marca.marca_id, anoCarro, comb.combustivel_id
FROM tb_locacao tl
JOIN marca
	ON tl.marcaCarro = marca.nome 
JOIN combustivel comb
	ON tl.tipoCombustivel = comb.tipo
ORDER BY tl.idCarro ASC;

--------------------------------- Ingestão de Valores na Tabela: Vendedor --------------------------------------

INSERT OR IGNORE INTO vendedor (vendedor_id, nome, sexo, estado_id)
SELECT DISTINCT tl.idVendedor, tl.nomeVendedor, tl.sexoVendedor, est.estado_id
FROM tb_locacao tl
JOIN estado est
	ON tl.estadoVendedor = est.nome
ORDER BY tl.idVendedor ASC;

--------------------------------- Ingestão de Valores na Tabela: Cliente ---------------------------------------

INSERT OR IGNORE INTO cliente (cliente_id, nome, cidade_id, estado_id, pais_id)
SELECT DISTINCT tl.idCliente, tl.nomeCliente, cid.cidade_id, est.estado_id, pais.pais_id
FROM tb_locacao tl
JOIN cidade cid
	ON tl.cidadeCliente = cid.nome
JOIN estado est
	ON tl.estadoCliente = est.nome
JOIN pais
	ON tl.paisCliente = pais.nome 
ORDER BY tl.idCliente ASC;

--------------------------------- Ingestão de Valores na Tabela: Locação ---------------------------------------

INSERT OR IGNORE INTO locacao (
	locacao_id, 
	cliente_id, 
	carro_id, 
	vendedor_id, 
	data_locacao, 
	hora_locacao, 
	qtd_diaria, 
	vlr_diaria,
	data_entrega,
	hora_entrega,
	km_carro
)
SELECT DISTINCT idLocacao,
		        idCliente,
		        idCarro,
		        idVendedor,
                SUBSTR(dataLocacao, 1, 4) || '-' || 
                SUBSTR(dataLocacao, 5, 2) || '-' || 
                SUBSTR(dataLocacao, 7, 2) AS dataLocacao, 
                PRINTF('%02d:%02d', 
               		CAST(SUBSTR(horaLocacao, 1, INSTR(horaLocacao, ':') - 1) AS INTEGER),
               		CAST(SUBSTR(horaLocacao, INSTR(horaLocacao, ':') + 1) AS INTEGER)
    				) AS horaLocacao,
		        qtdDiaria,
		        vlrDiaria,
                SUBSTR(dataEntrega, 1, 4) || '-' || 
                SUBSTR(dataEntrega, 5, 2) || '-' || 
                SUBSTR(dataEntrega, 7, 2) AS dataEntrega, 
        		PRINTF('%02d:%02d', 
               		CAST(SUBSTR(horaEntrega, 1, INSTR(horaEntrega, ':') - 1) AS INTEGER),
               		CAST(SUBSTR(horaEntrega, INSTR(horaEntrega, ':') + 1) AS INTEGER)
    				) AS horaEntrega,
		        kmCarro
FROM tb_locacao
ORDER BY idLocacao ASC;

-- SELECT * FROM tb_locacao;
DROP TABLE tb_locacao;

----------------------------------------------------------------------------------------------------------------
---------------------------------- ANÁLISE DE TABELAS E RELAÇÕES NORMALIZADAS ----------------------------------
----------------------------------------------------------------------------------------------------------------

-- SELECT * FROM locacao;
-- SELECT * FROM cliente;
-- SELECT * FROM vendedor;
-- SELECT * FROM cidade;
-- SELECT * FROM estado;
-- SELECT * FROM pais;
-- SELECT * FROM carro;
-- SELECT * FROM marca;
-- SELECT * FROM combustivel;