#!/usr/bin/python3
#https://dados.gov.br/dados/conjuntos-dados/crt-obras-nao-publicitarias-registradas
import polars as pl
import chardet

with open("etnias.csv", "rb") as f:
    char = chardet.detect(f.read())

etnias = pl.read_csv('etnias.csv', encoding=char['encoding'])

print(etnias.glimpse())