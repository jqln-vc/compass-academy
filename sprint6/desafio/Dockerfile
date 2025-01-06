# Uso de imagem pypy slim (mais ágil e eficiente)
FROM pypy:3-slim

# Criação de usuário para a aplicação, flag -m para criação de /home
RUN useradd -m datalake

# Definição do diretório de trabalho
WORKDIR /datalake/raw

# Update de pip e instalação do boto3
RUN pypy3 -m ensurepip && \
    pypy3 -m pip install --upgrade pip && \
    pypy3 -m pip install boto3

# Cópia dos arquivos da aplicação para o WORKDIR
COPY . .

# Alteração da propriedade da pasta e conteúdo para o usuário "datalake"
RUN chown -R datalake /datalake

# Definição do usuário atual como "datalake"
USER datalake

# Fornecimento de permissão de execução para os arquivos da aplicação
RUN chmod +x *.py

# Comando de execução da aplicação
CMD [ "pypy3", "ingestao.py" ]