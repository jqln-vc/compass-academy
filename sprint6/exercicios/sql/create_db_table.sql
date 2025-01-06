CREATE DATABASE IF NOT EXISTS meubanco;

CREATE EXTERNAL TABLE IF NOT EXISTS meubanco.nomes (
  nome STRING,
  sexo CHAR(1),
  total INT,
  ano INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
 'serialization.format' = ',',
 'field.delim' = ','
)
LOCATION 's3://compass-sprint5-lab/dados/';