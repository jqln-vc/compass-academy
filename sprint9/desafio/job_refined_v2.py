"""
Sprint 9 - Desafio Final - Etapa 4: transformação na Refined Zone.

Transformação, refinamento e modelagem dimensional de dados da 
camada Trusted Zone para a Refined Zone, utilizando Spark no
AWS Glue. 

Autoria: Jaqueline Costa
Data: Fev/25
job_refined.py: script com pipeline de transformação 

    Outputs / Uploads:
        - Arquivos Parquet na Refined Zone
        - log-transform-refined-{ano}{mes}{dia}.txt
"""

################################################################################
# IMPORTAÇÕES E DOWNLOAD ADICIONAL DE MODELO

# AWS/Glue
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext

# Ferramentas Gerais
from collections import Counter
from datetime import datetime
import sys
import subprocess

# Instalação do modelo spaCy
try:
    subprocess.check_call([sys.executable,
                           "-m", "spacy", "download", "en_core_web_trf"])
except Exception as e:
    print(f"Erro de instalação do modelo SpaCy: {e}")

# AWS
import boto3

# Spark
import pyspark.sql.functions as F
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, StringType

# NLP
import re
from transformers import pipeline
import spacy
import torch

################################################################################
# MODELOS

print("Carregando modelos de língua")

# Lematização e Sintaxe _________________________________________

nlp = spacy.load("en_core_web_trf")

# Classificação de Texto ________________________________________

modelo_conteudo_sexual = "uget/sexual_content_dection"
modelo_sexismo = "annahaz/xlm-roberta-base-misogyny-sexism-indomain-mix-bal"

class_sexual = pipeline("text-classification",
                        model=modelo_conteudo_sexual)

class_sexismo = pipeline("text-classification",
                         model=modelo_sexismo)


################################################################################
# CLASSES E FUNÇÕES AUXILIARES


# Log de Execução ______________________________________________________________

class LogPrinter:
    """Classe de redirecionamento do stdout para log."""

    def __init__(self, nome_arquivo: str):
        """Construtor: obtém o arquivo log e conecta-se ao stdout."""
        self.arq_log = open(nome_arquivo, "a")
        self.stdout = sys.stdout
        sys.stdout = self

    def write(self, dados: str):
        """Escrita de dados com timestamp no stdout e log."""
        if dados.strip():
            timestamp = datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
            registro = f"{timestamp} {dados.strip()}\n"
            self.arq_log.write(registro)
            self.stdout.write(registro)

    def flush(self):
        """Escrita imediata com flush do buffer."""
        self.arq_log.flush()
        self.stdout.flush()

    def close(self):
        """Fechamento do arquivo log."""
        if not self.arq_log.closed:
            self.arq_log.close()
            sys.stdout = self.stdout

# Categorização de Regiões _____________________________________________________

regioes = {
    "North America": ["CA", "US", "GL", "UM"],
    
    "Western Europe": ["AD", "AT", "BE", "CH", "DE", "DK",
                       "ES", "FI", "FO", "FR", "GB", "GI",
                       "IE", "IS", "IT", "LI", "LU", "MC", 
                       "NL", "NO", "PT", "SE", "SM", "VA"],
    
    "Middle East": ["AE", "BH", "IL", "IQ", "IR", "JO",
                    "KW", "LB", "OM", "PS", "QA", "SA",
                    "SY", "TR", "YE"],
    
    "Latin America": ["AR", "BO", "BR", "CL", "CO", "EC",
                      "GF", "GY", "PE", "PY", "SR", "UY", "VE"],
    
    "Asia": ["AF", "AM", "AZ", "BD", "BN", "BT", "BU",
             "CN", "GE", "HK", "ID", "IN", "JP", "KG", 
             "KH", "KP", "KR", "KZ", "LA", "LK", "MM",
             "MN", "MO", "MY", "NP", "PH", "PK", 
             "SG", "TH", "TJ", "TM", "TW", "UZ", "VN"],
    
    "Polynesia": ["AS", "AU", "CC", "CK", "CX", "FJ",
                  "FM", "GU", "HM", "KI", "MH", "MP",
                  "NC", "NF", "NR", "NU", "NZ", "PF",
                  "PG", "PN", "PW", "SB", "TK", "TO",
                  "TV", "VU", "WF", "WS"],
    
    "Africa": ["AO", "BF", "BI", "BJ", "BW", "CD",
               "CF", "CG", "CI", "CM", "CV", "DJ",
               "DZ", "EG", "EH", "ER", "ET", "GA",
               "GH", "GM", "GN", "GQ", "GW", "KE",
               "KM", "LR", "LS", "LY", "MA", "MG",
               "ML", "MR", "MW", "MZ", "NA", "NE",
               "NG", "RW", "SC", "SD", "SL", "SN", 
               "SO", "SS", "ST", "SZ", "TD", "TG",
               "TN", "TZ", "UG", "ZA", "ZM", "ZR", "ZW"],
    
    "Eastern Europe": ["AL", "BA", "BG", "BY", "CS",
                       "CZ", "EE", "GR", "HR", "HU",
                       "LT", "LV", "MD", "ME", "MK",
                       "PL", "RO", "RS", "RU", "SI",
                       "SK", "SU", "UA", "XC", "XG", "XK", "YU"],
    
    "Caribbean / Central America": ["AG", "AI", "AN", "AW", "BB",
                                    "BM", "BS", "BZ", "CR", "CU",
                                    "DM", "DO", "GD", "GP", "GT",
                                    "HN", "HT", "JM", "KN", "KY",
                                    "LC", "MQ", "MS", "MX", "NI",
                                    "PA", "PR", "SV", "TC", "TT",
                                    "VC", "VG", "VI"]
}

@udf(returnType=StringType())
def obter_regiao(iso_cod: str) -> str:
    for regiao, paises in regioes.items():
        if iso_cod in paises:
            return regiao
    return "Unknown" 


# Classificação de Conteúdo Sexual _____________________________________________

@udf(returnType=IntegerType())
def detector_conteudo_sexual(texto: str) -> int:
    return int(class_sexual(str(texto))[0]["label"][-1])


# Classificação de Sexismo _____________________________________________________

@udf(returnType=IntegerType())
def detector_sexismo(texto: str) -> int:
    return int(class_sexismo(str(texto))[0]["label"][-1])


# Extração Classe Morfossintática ______________________________________________

@udf(returnType=StringType())
def extracao_pos(doc: str, pos: str) -> list[str]:
    texto = nlp(doc)
    return [str(token.lemma_)
            for token in texto
            if token.pos_ == pos
            and not token.is_stop and token.is_alpha]

# Termo Mais Comum _____________________________________________________________

@udf(returnType=StringType())
def termo_mais_comum(lista: list[str]) -> str:
    if not lista:
        return None
    freq_termos = Counter(lista)
    return max(freq_termos, key=freq_termos.get)

# Tratamento de Palavras para Vocabulário _______________________________________

padrao_process = "\\[|\\]"
padrao_add_vocab = "^\\s+|\\s+$"

def split_palavras_vocab(df: object,
                         coluna_palavras: str,
                         padrao_process: str,
                         sep: str,
                         padrao_add_vocab: str,
                         coluna_extra: str) -> object:
    return df.select(
        coluna_extra,
        F.explode(
            F.split(  # Aplicação Padrão de Split de Termos
                F.regexp_replace(coluna_palavras, padrao_process, ""),
                sep
            )
        ).alias("palavra")
    ).select(
        coluna_extra,  # Aplicação Padrão de Limpeza de Termos para Inserção
        F.regexp_replace("palavra", padrao_add_vocab, "").alias("palavra")
)
    

################################################################################
# VARIÁVEIS

# Argumentos do Sistema
args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME",
     "S3_TMDB_INPUT_PATH",
     "S3_LOCAL_INPUT_PATH",
     "S3_BUCKET"
    ]
)

# Ambiente Spark & Glue
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

# Data Atual
ano, mes, dia = datetime.now().year,\
    f"{datetime.now().month:02}", f"{datetime.now().day:02}"

# Caminhos de Input
s3_tmdb_input = args["S3_TMDB_INPUT_PATH"]
s3_local_input = args["S3_LOCAL_INPUT_PATH"]

# Caminhos de Output
nome_bucket = args["S3_BUCKET"]
s3_refined_output = f"s3://{nome_bucket}/Refined"
log = f"log-transform-refined-{ano}{mes}{dia}"

# Integração AWS
s3 = boto3.resource("s3")
bucket = s3.Bucket(nome_bucket)

# Reconfiguração do stdout
sys.stdout.reconfigure(encoding="utf-8")
logger = LogPrinter(log)


################################################################################
# CRIAÇÃO DOS SPARK DATAFRAMES

# DataFrames ___________________________________________________________________

print("Iniciando upload dos datasets em DataFrames")

filmes_tmdb_df = spark.read.parquet(f"{s3_tmdb_input}/titulos/*").alias("tmdb")
filmes_local_df = spark.read.parquet(f"{s3_local_input}/*").alias("local")
paises_df = spark.read.parquet(f"{s3_tmdb_input}/paises/*")
linguas_df = spark.read.parquet(f"{s3_tmdb_input}/linguas/*")

# Join entre Filmes: Local + TMDB _____________________________________________

print("Iniciando o JOIN entre datasets Local e TMDB")

filmes_local_total = filmes_local_df.join(
    filmes_tmdb_df,
    filmes_tmdb_df.imdb_id == filmes_local_df.imdb_id
).select(
    "tmdb.tmdb_id",
    "local.imdb_id",
    "local.titulo_comercial",
    "tmdb.titulo_original",
    "local.ano_lancamento",
    "tmdb.lingua_original",
    "tmdb.pais_origem",
    "tmdb.popularidade",
    "local.media_avaliacao",
    "tmdb.qtd_avaliacoes",
    "tmdb.sinopse")\
.distinct()

filmes_df = filmes_local_total.union(filmes_tmdb_df.select(
    "tmdb_id",
    "imdb_id",
    "titulo_comercial",
    "titulo_original",
    "ano_lancamento",
    "lingua_original",
    "pais_origem",
    "popularidade",
    "media_avaliacao",
    "qtd_avaliacoes",
    "sinopse").distinct()
).filter("ano_lancamento >= 2013").drop_duplicates(["tmdb_id"])\
.orderBy("ano_lancamento")

print("JOIN realizado com sucesso")

################################################################################
# EXTRAÇÃO DE VALORES PARA ATRIBUTOS

# Coluna: Texto Total __________________________________________________________

print("Gerando coluna texto_total com textos de título e sinopse concatenados")

filmes_df = filmes_df.withColumn(
    "texto_total", 
    F.concat(
        F.col("titulo_comercial"), 
        F.lit(" "), 
        F.col("sinopse")
    )
).alias("filmes")

# Coluna: Região _______________________________________________________________

print("Gerando coluna de classificação de países em regiões")

paises_df = paises_df.withColumn(
    "regiao",
    obter_regiao(F.col("iso_cod"))
).orderBy("regiao", "pais")

# Coluna: Conteúdo Sexual _______________________________________________________

print("Gerando coluna de classificação de conteúdo sexual")

analise_textual_df = filmes_df.select(
    "tmdb_id", "sinopse", "texto_total"
    ).withColumn(
        "conteudo_sexual",
        detector_conteudo_sexual(F.col("texto_total"))
)

# Coluna: Sexismo _______________________________________________________________

print("Gerando coluna de classificação de sexismo")

analise_textual_df = analise_textual_df.withColumn(
        "sexismo",
        detector_sexismo(F.col("texto_total"))
)

# Colunas: Classes Sintáticas (POS) _____________________________________________

print("Gerando colunas listas de termos por classe sintática")

analise_textual_df = analise_textual_df.withColumn(
    "substantivos",
    extracao_pos(F.col("texto_total"), F.lit("NOUN"))
    ).withColumn(
        "verbos",
        extracao_pos(F.col("texto_total"), F.lit("VERB"))
    ).withColumn(
        "adjetivos",
        extracao_pos(F.col("texto_total"), F.lit("ADJ"))
    ).withColumn(
        "adverbios",
        extracao_pos(F.col("texto_total"), F.lit("ADV"))
)
    
print("Gerando colunas de termos mais comuns")
    
analise_textual_df = analise_textual_df.withColumn(
        "subst_mais_comum",
        termo_mais_comum(F.col("substantivos"))
    ).withColumn(
        "verbo_mais_comum",
        termo_mais_comum(F.col("verbos"))
    ).withColumn(
        "adj_mais_comum",
        termo_mais_comum(F.col("adjetivos"))
    ).withColumn(
        "adv_mais_comum",
        termo_mais_comum(F.col("adverbios"))
)
    
# Coluna: Corpus _______________________________________________________________

print("Gerando coluna Corpus com concatenação de textos de análise")

# Concatenação de Textos da Análise
corpora_df = analise_textual_df.groupBy() \
    .agg(F.concat_ws(" ", F.collect_list("texto_total")).alias("corpus"))

# Coluna: Frequência ___________________________________________________________

print("Gerando coluna Frequência com ocorrência de termos para cada filme")

# Split de Listas de Termos Classificados Sintaticamente
palavras_df = split_palavras_vocab(
    analise_textual_df,
    "substantivos",
    padrao_process=padrao_process,
    sep=",",
    padrao_add_vocab=padrao_add_vocab,
    coluna_extra="tmdb_id"
).union(split_palavras_vocab(
    analise_textual_df,
    "verbos",
    padrao_process=padrao_process,
    sep=",",
    padrao_add_vocab=padrao_add_vocab,
    coluna_extra="tmdb_id"
)).union(split_palavras_vocab(
    analise_textual_df,
    "adjetivos",
    padrao_process=padrao_process,
    sep=",",
    padrao_add_vocab=padrao_add_vocab,
    coluna_extra="tmdb_id"
)).union(split_palavras_vocab(
    analise_textual_df,
    "adverbios",
    padrao_process=padrao_process,
    sep=",",
    padrao_add_vocab=padrao_add_vocab,
    coluna_extra="tmdb_id"
))

# Contagem de Ocorrências de Cada Palavra Normalizada
contagem_palavras = palavras_df.groupBy("tmdb_id", "palavra").agg(
    F.count("*").alias("frequencia")
)

################################################################################
# CRIAÇÃO DE TABELAS FATO E DIMENSÕES

# LÍNGUAS DIM __________________________________________________________________

print("Iniciando criação da tabela dimensional Línguas")

linguas_dim = (linguas_df.withColumn("lingua",
                F.regexp_replace(F.col("lingua"),
                                 "Ossetian; Ossetic", "Ossetian"))
    .withColumn("lingua",
                F.regexp_replace(F.col("lingua"),
                                 "Haitian; Haitian Creole", "Haitian"))
    .withColumn("lingua",
                F.regexp_replace(F.col("lingua"),
                                 "Chichewa; Nyanja", "Chichewa"))
    .orderBy("lingua")
)


linguas_dim = linguas_dim.withColumn(
    "lingua_key",
    F.monotonically_increasing_id() + F.lit(1)
    ).select("lingua_key", "iso_cod", "lingua").alias("linguas")

print("Tabela dimensional Línguas criada com sucesso")

# PAÍSES DIM __________________________________________________________________

print("Iniciando criação da tabela dimensional Países")

paises_dim = paises_df.withColumn(
    "pais_key",
    F.monotonically_increasing_id() + F.lit(1)
    ).select("pais_key", "iso_cod", "pais", "regiao").alias("paises")

print("Tabela dimensional Países criada com sucesso")

# TÍTULOS DIM _________________________________________________________________

print("Iniciando criação da tabela dimensional Títulos")

titulos_df = filmes_df.select(
    "titulo_comercial",
    "titulo_original",
    "tmdb_id"
).dropDuplicates(["tmdb_id"])\
.orderBy("titulo_comercial")

titulos_dim = titulos_df.withColumn(
    "titulo_key",
    F.monotonically_increasing_id() + F.lit(1)
).select("titulo_key",
         "titulo_comercial",
         "titulo_original",
         "tmdb_id").alias("titulos")

print("Tabela dimensional Títulos criada com sucesso")

# ANÁLISE TEXTUAL DIM _________________________________________________________

print("Iniciando criação da tabela dimensional Análise Textual")

analise_textual_dim = analise_textual_df.withColumn(
    "analise_key",
    F.monotonically_increasing_id() + F.lit(1)
).select("analise_key",
         "sinopse",
         "texto_total",
         "conteudo_sexual",
         "sexismo",
         "subst_mais_comum",
         "verbo_mais_comum",
         "adj_mais_comum",
         "adv_mais_comum",
         "tmdb_id").alias("analise")

print("Tabela dimensional Análise Textual criada com sucesso")

# CORPORA DIM _________________________________________________________________

print("Iniciando criação da tabela dimensional Corpora")

corpora_dim = corpora_df.withColumn(
    "data_registro",
    F.current_timestamp()
).withColumn(
    "corpus_key",
    F.monotonically_increasing_id() + F.lit(1)
).select("corpus_key", "corpus", "data_registro")

print("Tabela dimensional Corpora criada com sucesso")

# VOCAB DIM ___________________________________________________________________

print("Iniciando criação da tabela dimensional Vocabulário")

vocab_df = analise_textual_df.select(
    F.expr("""
            stack(4,
                substantivos, 'NOUN',
                verbos, 'VERB',
                adjetivos, 'ADJ',
                adverbios, 'ADV'
            ) as (palavra, pos_class)
        """)
)

vocab_df = split_palavras_vocab(vocab_df,
                                "palavra",
                                padrao_process=padrao_process,
                                sep=",",
                                padrao_add_vocab=padrao_add_vocab,
                                coluna_extra="pos_class")

vocab_dim = vocab_df.filter(F.col("palavra") != "").dropna().distinct().withColumn(
    "vocab_key",
    F.monotonically_increasing_id() + F.lit(1)
).select("vocab_key", "palavra", "pos_class")\
.orderBy("pos_class", "palavra").alias("vocab")

print("Tabela dimensional Vocabulário criada com sucesso")

# FILMES FACT ___________________________________________________________________

print("Iniciando criação da tabela fato Filmes")

filmes_fact = filmes_df.join(
    titulos_dim,
    filmes_df.tmdb_id == titulos_dim.tmdb_id
).join(
    linguas_dim,
    filmes_df.lingua_original == linguas_dim.iso_cod 
).join(
    paises_dim,
    filmes_df.pais_origem == paises_dim.iso_cod
).withColumn(
    "corpus_key",
    F.lit(1)
).withColumn(
    "filme_key",
    F.monotonically_increasing_id() + F.lit(1)
).select(
    "filme_key",
    "filmes.tmdb_id",
    "filmes.imdb_id",
    "titulos.titulo_key",
    "paises.pais_key",
    "linguas.lingua_key",
    "corpus_key",
    "filmes.ano_lancamento",
    "filmes.popularidade",
    "filmes.media_avaliacao",
    "filmes.qtd_avaliacoes").drop_duplicates(["tmdb_id"]).alias("fato")

filmes_fact = filmes_fact.join(
    analise_textual_dim,
    filmes_fact.tmdb_id == analise_textual_dim.tmdb_id
).select(
    "filme_key",
    "fato.tmdb_id",
    "imdb_id",
    "titulo_key",
    "pais_key",
    "lingua_key",
    "analise.analise_key",
    "corpus_key",
    "ano_lancamento",
    "popularidade",
    "media_avaliacao",
    "qtd_avaliacoes").drop_duplicates(["analise_key"]).orderBy("filme_key")

print("Tabela fato Filmes criada com sucesso")

# FILMES-LÍNGUAS BRIDGE _________________________________________________________

print("Iniciando criação da tabela bridge Filmes-Vocab")

# JOIN Entre Fato Filmes e Dimensional Vocabulário
filmes_vocab_bridge = contagem_palavras.join(
    vocab_dim,
    contagem_palavras.palavra == vocab_dim.palavra,
    "inner"
).join(
    filmes_fact,
    filmes_fact.tmdb_id == contagem_palavras.tmdb_id,
    "inner"
).select(
    "fato.filme_key",
    "vocab.vocab_key",
    F.col("frequencia")
)

print("Tabela bridge Filmes-Vocab criada com sucesso")

# EXCLUSÃO DE COLUNAS AUXILIARES ________________________________________________

print("Excluindo colunas auxiliares para associação entre tabelas")

filmes_vocab_bridge = filmes_vocab_bridge.drop("tmdb_id")
titulos_dim = titulos_dim.drop("tmdb_id")
analise_textual_dim = analise_textual_dim.drop("tmdb_id")

################################################################################
# INGRESSÃO NA CAMADA REFINED DO BUCKET

print("Início da ingressão de tabelas em formato Parquet na Refined Zone")

# LÍNGUAS DIM __________________________________________________________________

print("Iniciando escrita da tabela dimensional Línguas")

linguas_dim.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_refined_output}/linguas_dim/")

print("Tabela dimensional Línguas enviada para a Refined Zone")
    
# PAÍSES DIM __________________________________________________________________

print("Iniciando escrita da tabela dimensional Países")

paises_dim.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_refined_output}/paises_dim/")

print("Tabela dimensional Países enviada para a Refined Zone")

# TÍTULOS DIM __________________________________________________________________

print("Iniciando escrita da tabela dimensional Títulos")

titulos_dim.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_refined_output}/titulos_dim/")
    
print("Tabela dimensional Títulos enviada para a Refined Zone")
    
# ANÁLISE TEXTUAL DIM __________________________________________________________

print("Iniciando escrita da tabela dimensional Análise Textual")

analise_textual_dim.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_refined_output}/analise_textual_dim/")

print("Tabela dimensional Análise Textual enviada para a Refined Zone")

# CORPORA DIM __________________________________________________________________

print("Iniciando escrita da tabela dimensional Corpora")

corpora_dim.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_refined_output}/corpora_dim/")

print("Tabela dimensional Corpora enviada para a Refined Zone")

# VOCAB DIM ____________________________________________________________________

print("Iniciando escrita da tabela dimensional Vocabulário")

vocab_dim.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_refined_output}/vocab_dim/")

print("Tabela dimensional Vocabulário enviada para a Refined Zone")

# FILMES FACT __________________________________________________________________

print("Iniciando escrita da tabela fato Filmes")

filmes_fact.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_refined_output}/filmes_fact/")

print("Tabela fato Filmes enviada para a Refined Zone")

# FILMES-VOCAB BRIDGE __________________________________________________________

print("Iniciando escrita da tabela bridge Filmes-Vocab")

filmes_vocab_bridge.coalesce(1).write \
    .mode("overwrite") \
    .format("parquet") \
    .save(f"{s3_refined_output}/filmes_vocab_bridge/")

print("Tabela bridge Filmes-Vocab enviada para a Refined Zone")

print(f"Concluindo a execução do script\n\
    Listagem de objetos no bucket {nome_bucket}")
[print(objeto) for objeto in bucket.objects.all()]

print("Modelagem e ingressão na Refined Zone realizada com sucesso")
logger.close()
bucket.upload_file(Filename=f"{log}", Key=f"Logs/{log}")

job.commit()
