#

||
|---|
|![Banner](../assets/banner-guide04.png)|
||

## Optimizador SQL

O comando `EXPLAIN` antes de uma declaração mostra a sequência lógica utilizada pelo optimizador para rodar a query.

```sql
    EXPLAIN SELECT * FROM tabelinha WHERE valor = 'isto' LIMIT 10;
```

## Boas Práticas

- Nunca **NUNCA** rode um SELECT * sem especificar um LIMIT. Especialmente quando estiver na nuvem.

## Referências

FAROULT, Stephane; ROBSON, Peter. **The Art of SQL**. Sebastopol: O'Reilly, 2006.
