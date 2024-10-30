-- E10
-- A comissão de um vendedor é definida a partir de um percentual sobre o total de vendas 
-- (quantidade * valor unitário) por ele realizado. 
-- O percentual de comissão de cada vendedor está armazenado na coluna perccomissao, tabela tbvendedor.
-- Com base em tais informações, calcule a comissão de todos os vendedores, considerando todas as vendas armazenadas 
-- na base de dados com status concluído.
-- As colunas presentes no resultado devem ser vendedor, valor_total_vendas e comissao. 
-- O valor de comissão deve ser apresentado em ordem decrescente arredondado na segunda casa decimal.
-------------------------------------------------------------------------------------------------------------------

WITH total_vendas AS (
    SELECT vendedor.nmvdd AS vendedor,
    SUM(vendas.qtd * vendas.vrunt) AS valor_total_vendas,
    SUM((vendas.qtd * vendas.vrunt) * vendedor.perccomissao)/100 AS comissao
    FROM tbvendedor AS vendedor
    LEFT JOIN tbvendas AS vendas
        ON vendas.cdvdd = vendedor.cdvdd
    WHERE vendas.status = 'Concluído'
    GROUP BY vendedor
)

SELECT vendedor,
       valor_total_vendas,
       ROUND(comissao, 2) AS comissao
FROM total_vendas
ORDER BY comissao DESC
