----------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------

-- Sprint 2: Modelagem Dimensional de Banco Relacional - Cubos - Concessionária
-- Autoria: Jaqueline Costa
-- Data: Nov / 2024
-- concessionaria_cubos.sql: Modelagem de dados para a camada de distribuição de sistemas OLAP em cubos, 
-- por meio de views; ingestão de dados a partir das tabelas modeladas dimensionalmente em star schema com  
-- o script 'concessionaria_star_schema.sql'.

----------------------------------------------------------------------------------------------------------------
------------------------------ CRIAÇÃO DE CUBOS PARA ANÁLISE MULTIDIMENSIONAL ----------------------------------
----------------------------------------------------------------------------------------------------------------

-- "Plano": análise de veículos da base, incluindo kilometragem atual e quantidade de dias locados

CREATE VIEW base_veiculos (
	carro_id,
	classi,
	modelo,
	ano,
	dias_locado,
	km_atual
)
AS
SELECT car.carro_id,
       car.classi,
       car.modelo,
       car.ano,
       SUM(loc.qtd_diaria) AS dias_locado,
       MAX(loc.km_carro) as km_atual
FROM carro car
JOIN locacao loc
	ON car.carro_id = loc.carro_id
GROUP BY car.carro_id, car.modelo
ORDER BY 1, 3 DESC;

-- SELECT * FROM base_veiculos;

----------------------------------------------------------------------------------------------------------------------

-- Cubo: análise de dias locados e lucro total de cada veículo, por dia da semana

CREATE VIEW lucro_locacao_veiculos (
	carro_key,
	modelo,
	dia_semana,
	dias_locado,
	lucro_total
)
AS
SELECT loc.carro_key,
	   car.modelo,
	   dt.dia_semana,
	   SUM(loc.qtd_diaria) AS dias_locado,
	   SUM(loc.valor_total) AS lucro_total
FROM locacao_fact loc
JOIN carro_dim car
	ON loc.carro_key = car.carro_key 
JOIN data_dim dt 
    ON loc.data_locacao_key = dt.data_key
GROUP BY loc.carro_key, dt.dia_semana
ORDER BY 1 ASC;

-- SELECT * FROM lucro_locacao_veiculos;

----------------------------------------------------------------------------------------------------------------------

-- Cubo: análise de locações vendidas de cada vendedor, por modelo e dias da semana

CREATE VIEW lucro_vendedores (
	vendedor_key,
	nome,
	modelo,
	dia_semana,
	dias_locados,
	lucro_total
)
AS
SELECT vend.vendedor_key,
	   vend.nome,
	   car.modelo,
	   dt.dia_semana,
	   SUM(loc.qtd_diaria) AS dias_locado,
	   SUM(loc.valor_total) AS lucro_total
FROM vendedor_dim vend
JOIN locacao_fact loc
	ON vend.vendedor_key = loc.vendedor_key
JOIN carro_dim car
	ON loc.carro_key = car.carro_key 
JOIN data_dim dt 
    ON loc.data_locacao_key = dt.data_key
GROUP BY vend.vendedor_key, car.modelo, dt.dia_semana
ORDER BY lucro_total DESC;

-- SELECT * FROM lucro_vendedores;

----------------------------------------------------------------------------------------------------------------------

-- Cubo: análise de modelos locados por cliente, incluindo quantidade de dias locados e gasto total, por dia da semana

CREATE VIEW gasto_veiculo_clientes (
	cliente_key,
	nome,
	modelo,
	dia_semana,
	dias_locados,
	gasto_total
)
AS
SELECT cli.cliente_key,
	   cli.nome,
	   car.modelo,
	   dt.dia_semana,
	   SUM(loc.qtd_diaria) AS dias_locado,
	   SUM(loc.valor_total) AS gasto_total
FROM cliente_dim cli
JOIN locacao_fact loc
	ON cli.cliente_key = loc.cliente_key
JOIN carro_dim car
	ON loc.carro_key = car.carro_key 
JOIN data_dim dt 
    ON loc.data_locacao_key = dt.data_key
GROUP BY cli.cliente_key, car.modelo, dt.dia_semana
ORDER BY gasto_total DESC;

-- SELECT * FROM gasto_veiculo_clientes;