WITH nome_por_decada AS (
    SELECT 
        (CAST(ano AS INTEGER) - (CAST(ano AS INTEGER) % 10)) AS decada,
        nome,
        sexo,
        SUM(total) AS total_registros
    FROM meubanco.nomes
    WHERE CAST(ano AS INTEGER) >= 1950
    GROUP BY 
        (CAST(ano AS INTEGER) - (CAST(ano AS INTEGER) % 10)),
        nome,
        sexo
),
nomes_ranqueados AS (
    SELECT 
        decada,
        nome,
        sexo,
        total_registros,
        DENSE_RANK() OVER (
            PARTITION BY decada 
            ORDER BY total_registros DESC
        ) AS rank
    FROM nome_por_decada
)
SELECT 
    decada,
    nome,
    sexo,
    total_registros
FROM nomes_ranqueados
WHERE rank <= 3
ORDER BY decada, total_registros DESC; 