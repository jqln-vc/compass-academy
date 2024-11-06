-- E12
-- Apresente a query para listar código, nome e data de nascimento dos dependentes do vendedor com 
-- menor valor total bruto em vendas (não sendo zero). 
-- As colunas presentes no resultado devem ser cddep, nmdep, dtnasc e valor_total_vendas.
-- Observação: Apenas vendas com status concluído.
-------------------------------------------------------------------------------------------------------------------

SELECT dependente.cddep AS cddep,
       dependente.nmdep AS nmdep,
       dependente.dtnasc AS dtnasc,
       SUM(vendas.qtd * vendas.vrunt) AS valor_total_vendas
FROM tbvendas AS vendas
LEFT JOIN tbdependente AS dependente
    ON vendas.cdvdd = dependente.cdvdd
WHERE vendas.status = 'Concluído'
GROUP BY dependente.cdvdd
HAVING valor_total_vendas > 0
ORDER BY valor_total_vendas 
LIMIT 1;