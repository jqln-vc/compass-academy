-- Exportação de Dados 2
-- Exportar o resultado da query que obtém as 5 editoras com maior quantidade de livros na biblioteca 
-- para um arquivo CSV. Utilizar o caractere | (pipe) como separador. 
-- Lembre-se que o conteúdo do seu arquivo deverá respeitar a sequência de colunas 
-- e seus respectivos nomes de cabeçalho que listamos abaixo:

-- Colunas:

-- CodEditora
-- NomeEditora
-- QuantidadeLivros

-- Observação: O arquivo exportado, conforme as especificações acima, deve ser disponibilizado no GitHub.
-------------------------------------------------------------------------------------------------------------------

SELECT editora.codeditora AS CodEditora,
       editora.nome AS NomeEditora,
       COUNT(livro.cod) AS QuantidadeLivros
FROM livro
JOIN editora
    ON livro.editora = editora.codeditora
JOIN endereco
    ON editora.endereco = endereco.codendereco
GROUP BY NomeEditora
ORDER BY QuantidadeLivros DESC;