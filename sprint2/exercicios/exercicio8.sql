-- E08
-- Apresente a query para listar o código e o nome do vendedor com maior número de vendas (contagem), 
-- e que estas vendas estejam com o status concluída.  
-- As colunas presentes no resultado devem ser, portanto, cdvdd e nmvdd.
-------------------------------------------------------------------------------------------------------------------

WITH vendas_vendedor AS (
    SELECT vendedor.cdvdd AS cdvdd,
           vendedor.nmvdd AS nmvdd,
           COUNT (vendas.cdvdd) AS quantidade
    FROM tbvendas AS vendas
    JOIN tbvendedor AS vendedor
        ON vendas.cdvdd = vendedor.cdvdd
    JOIN tbestoqueproduto AS produto
        ON vendas.cdpro = produto.cdpro
    WHERE produto.status <> 6
    GROUP BY vendedor.cdvdd
    ORDER BY quantidade DESC
)

SELECT cdvdd,
       nmvdd
FROM vendas_vendedor
LIMIT 1