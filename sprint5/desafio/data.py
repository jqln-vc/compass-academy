#!/usr/bin/python3
import polars as pl
import chardet

with open("funai_etnias.csv", "rb") as f:
    result = chardet.detect(f.read())
    print(result)

etnias = pl.read_csv('funai_etnias.csv', encoding='ISO-8859-1')

print(etnias.glimpse())