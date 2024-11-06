-- E07
-- Apresente a query para listar o nome dos autores com nenhuma publicação.
-- Apresentá-los em ordem crescente.
-------------------------------------------------------------------------------------------------------------------

WITH qtd_publicacoes AS (
    SELECT autor.nome AS nome,
           COUNT(livro.cod) AS quantidade
    FROM autor
    LEFT JOIN livro
        ON autor.codautor = livro.autor
        GROUP BY autor.nome
)

SELECT nome
FROM qtd_publicacoes
WHERE quantidade = 0
ORDER BY nome;
