DROP VIEW IF EXISTS locacao_fact;
DROP VIEW IF EXISTS cliente_dim;
DROP VIEW IF EXISTS vendedor_dim;
DROP VIEW IF EXISTS carro_dim;

-- Criando view da tabela 'locacao_fact'

CREATE VIEW locacao_fact AS
SELECT *
FROM locacao
ORDER BY locacao_id ASC;

-- Criando view da tabela 'cliente_dim'

CREATE VIEW cliente_dim AS
SELECT DISTINCT loc.cliente_id, cli.nome AS nome, cid.nome AS cidade, est.nome AS estado, pais.nome AS pais
FROM locacao loc
JOIN cliente cli
	ON loc.cliente_id = cli.cliente_id
JOIN cidade cid
	ON cli.cidade_id = cid.cidade_id
JOIN estado est
	ON cli.estado_id = est.estado_id
JOIN pais
	ON cli.pais_id = pais.pais_id
ORDER BY loc.cliente_id ASC;

--SELECT * FROM cliente_dim;

-- Criando view da tabela 'vendedor_dim'

CREATE VIEW vendedor_dim AS
SELECT DISTINCT loc.vendedor_id, vend.nome AS nome, vend.sexo AS sexo, est.nome AS estado
FROM locacao loc
JOIN vendedor vend
	ON loc.vendedor_id = vend.vendedor_id
JOIN estado est
	ON vend.estado_id = est.estado_id
ORDER BY loc.vendedor_id ASC;

SELECT * FROM vendedor_dim;