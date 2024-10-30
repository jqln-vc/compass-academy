-- E09
-- Apresente a query para listar o código e nome do produto mais vendido entre as datas de 2014-02-03 
-- até 2018-02-02, e que estas vendas estejam com o status concluída. 
-- As colunas presentes no resultado devem ser cdpro e nmpro.
-------------------------------------------------------------------------------------------------------------------

WITH mais_vendido AS (
    SELECT vendas.cdpro AS cdpro,
           vendas.nmpro AS nmpro,
           COUNT(vendas.cdven) AS quantidade
    FROM tbvendas AS vendas
    JOIN tbestoqueproduto AS produto
        ON vendas.cdpro = produto.cdpro
    WHERE vendas.status = 'Concluído'
        AND vendas.dtven BETWEEN '2014-02-03' AND '2018-02-02'
    GROUP BY vendas.cdpro
    ORDER BY quantidade DESC
)

SELECT cdpro,
       nmpro
FROM mais_vendido
LIMIT 1