# Uso de imagem pypy slim (mais ágil e eficiente)
FROM pypy:3-slim

# Criação de usuário para a aplicação, flag -m para criação de /home
RUN useradd -m carguru

# Definição do diretório de trabalho
WORKDIR /carguru

# Cópia dos arquivos da aplicação para o WORKDIR
COPY . .

# Alteração da propriedade da pasta e conteúdo para o usuário "carguru"
RUN chown -R carguru /carguru

# Definição do usuário atual como "carguru"
USER carguru

# Fornecimento de permissão de execução para os arquivos da aplicação
RUN chmod +x *.py

# Comando de execução da aplicação
CMD [ "pypy3", "carguru.py" ]
