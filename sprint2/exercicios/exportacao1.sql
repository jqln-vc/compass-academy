-- Exportação de Dados 1
-- Exportar o resultado da query que obtém os 10 livros mais caros para um arquivo CSV. 
-- Utilizar o caractere ; (ponto e vírgula) como separador. 
-- Lembre-se que o conteúdo do seu arquivo deverá respeitar a sequência de colunas e 
-- seus respectivos nomes de cabeçalho que listamos abaixo:

-- Colunas:

-- CodLivro
-- Titulo
-- CodAutor
-- NomeAutor
-- Valor
-- CodEditora
-- NomeEditora

-- Observação: O arquivo exportado, conforme as especificações acima, deve ser disponibilizado no GitHub.
-------------------------------------------------------------------------------------------------------------------

SELECT livro.cod AS CodLivro,
       livro.titulo AS Titulo,
       livro.autor AS CodAutor,
       autor.nome AS NomeAutor,
       livro.valor AS Valor,
       livro.editora AS CodEditora,
       editora.nome AS NomeEditora
FROM livro
JOIN autor
    ON livro.autor = autor.codautor
JOIN editora
    ON livro.editora = editora.codeditora
ORDER BY livro.valor DESC
LIMIT 10;