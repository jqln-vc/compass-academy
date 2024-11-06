----------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------

-- Sprint 2: Normalização de Banco Relacional - Concessionária
-- Autoria: Jaqueline Costa
-- Data: Nov / 2024
-- concessionaria_normalizacao.sql: Criação de tabelas normalizadas e inserção dos dados a partir da tabela
-- original.

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

----------------------------------------------------------------------------------------------------------------

-- Estrutura da tabela 'locacao'

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
	hora_entrega TIME DEFAULT '0:00' NOT NULL,
	km_carro INT NOT NULL,
	FOREIGN KEY(cliente_id) REFERENCES cliente(cliente_id),
	FOREIGN KEY(carro_id) REFERENCES carro(carro_id),
	FOREIGN KEY(vendedor_id) REFERENCES vendedor(vendedor_id)
);

-- Estrutura da tabela 'cliente'

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

-- Estrutura da tabela 'vendedor'

CREATE TABLE vendedor (
	vendedor_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(100) NOT NULL,
	sexo SMALLINT NOT NULL,
	estado_id INTEGER NOT NULL,
	FOREIGN KEY (estado_id) REFERENCES estado(estado_id)
);

-- Estrutura da tabela 'carro'

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


-- Estrutura da tabela 'marca'

CREATE TABLE marca (
	marca_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(80) UNIQUE NOT NULL
);

-- Estrutura da tabela 'combustivel'

CREATE TABLE combustivel (
	combustivel_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	tipo VARCHAR(20) UNIQUE NOT NULL
);

-- Estrutura da tabela 'cidade'

CREATE TABLE cidade (
	cidade_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(40) UNIQUE NOT NULL
);

-- Estrutura da tabela 'estado'

CREATE TABLE estado (
	estado_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(40) UNIQUE NOT NULL
);

-- Estrutura da tabela 'pais'

CREATE TABLE pais (
	pais_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	nome VARCHAR(40) UNIQUE NOT NULL
);

----------------------------------------------------------------------------------------------------------------
---------------------------------- INSERÇÃO DE DADOS NAS TABELAS NORMALIZADAS ----------------------------------
----------------------------------------------------------------------------------------------------------------

-- Inserção de valores na tabela 'estado'

INSERT OR IGNORE INTO estado (nome)
SELECT DISTINCT estadoCliente
FROM tb_locacao
ORDER BY estadoCliente ASC;

INSERT OR IGNORE INTO estado (nome)
SELECT DISTINCT estadoVendedor
FROM tb_locacao
ORDER BY estadoVendedor ASC;

-- Inserção de valores na tabela 'cidade'

INSERT OR IGNORE INTO cidade (nome)
SELECT DISTINCT cidadeCliente
FROM tb_locacao
ORDER BY cidadeCliente ASC;

-- Inserção de valores na tabela 'pais'

INSERT OR IGNORE INTO pais (nome)
SELECT DISTINCT paisCliente
FROM tb_locacao
ORDER BY paisCliente ASC;

-- Inserção de valores na tabela 'marca'

INSERT OR IGNORE INTO marca (nome)
SELECT DISTINCT marcaCarro
FROM tb_locacao
ORDER BY marcaCarro ASC;

-- Inserção de valores na tabela 'combustivel'

INSERT OR IGNORE INTO combustivel (tipo)
SELECT DISTINCT tipoCombustivel
FROM tb_locacao
ORDER BY tipoCombustivel ASC;

-- Inserção de valores na tabela 'carro'

INSERT OR IGNORE INTO carro (carro_id, classi, modelo, marca_id, ano, combustivel_id)
SELECT DISTINCT tl.idCarro, tl.classiCarro, tl.modeloCarro, marca.marca_id, anoCarro, comb.combustivel_id
FROM tb_locacao tl
JOIN marca
	ON tl.marcaCarro = marca.nome 
JOIN combustivel comb
	ON tl.tipoCombustivel = comb.tipo
ORDER BY tl.idCarro ASC;

-- Inserção de valores na tabela 'vendedor'

INSERT OR IGNORE INTO vendedor (vendedor_id, nome, sexo, estado_id)
SELECT DISTINCT tl.idVendedor, tl.nomeVendedor, tl.sexoVendedor, est.estado_id
FROM tb_locacao tl
JOIN estado est
	ON tl.estadoVendedor = est.nome
ORDER BY tl.idVendedor ASC;

-- Inserção de valores na tabela 'cliente'

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

-- Inserção de valores na tabela 'locacao'

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
                dataLocacao, 
                horaLocacao, 
		        qtdDiaria,
		        vlrDiaria,
                dataEntrega, 
                horaEntrega, 
		        kmCarro
FROM tb_locacao
ORDER BY idLocacao ASC;
